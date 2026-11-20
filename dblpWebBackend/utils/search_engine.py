import json
import logging
import os
import re
import sqlite3
import threading

from conf import SEARCH_RES_MAX_NUM, SQLITE_DB_PATH

# 标题高亮标签，与前端样式保持一致
HIGHLIGHT_PRE = '<span class="highlight">'
HIGHLIGHT_POST = '</span>'

# 从用户输入中提取检索词，过滤掉 FTS5 的查询语法字符，避免语法错误
_TOKEN_PATTERN = re.compile(r'[^\W_]+', re.UNICODE)

# 每个线程独享一个连接，uwsgi 多线程模式下避免跨线程复用
_local = threading.local()


def _get_connection():
    conn = getattr(_local, 'conn', None)
    if conn is None:
        if not os.path.exists(SQLITE_DB_PATH):
            logging.warning("检索库不存在: " + SQLITE_DB_PATH)
            return None
        conn = sqlite3.connect(SQLITE_DB_PATH, timeout=10)
        # Web 进程只读，WAL 模式下仍需要写权限打开 -shm 文件
        conn.execute("PRAGMA query_only = ON")
        _local.conn = conn
    return conn


def build_match_query(keys):
    """
    将用户输入转换为 FTS5 查询，检索词之间为 OR 关系，与原 ES match 查询语义一致
    """
    tokens = _TOKEN_PATTERN.findall(keys or '')
    if not tokens:
        return None
    return ' OR '.join('"%s"' % token for token in tokens)


def search_papers(keys, category, yf, yt, limit=SEARCH_RES_MAX_NUM):
    """
    按标题全文检索，并用类别、年份区间过滤，返回按 BM25 相关度排序的结果
    """
    conn = _get_connection()
    match_query = build_match_query(keys)
    if conn is None or match_query is None or not category:
        return []
    placeholders = ','.join(['?'] * len(category))
    sql = """
        SELECT year, authors, ee_url, category, abbreviation,
               highlight(papers, 0, ?, ?) AS title
        FROM papers
        WHERE papers MATCH ?
          AND category IN ({placeholders})
          AND year BETWEEN ? AND ?
        ORDER BY bm25(papers)
        LIMIT ?
    """.format(placeholders=placeholders)
    params = [HIGHLIGHT_PRE, HIGHLIGHT_POST, match_query]
    params += list(category)
    params += [str(min(yf, yt)), str(max(yf, yt)), limit]
    try:
        return conn.execute(sql, params).fetchall()
    except sqlite3.Error:
        logging.exception("检索失败, keys=" + str(keys))
        return []


def construct_res_dict(papers):
    return [{
        "title": title,
        "year": int(year),
        "authors": json.loads(authors) if authors else [],
        "url": ee_url,
        "category": category,
        "abbreviation": abbreviation
    } for year, authors, ee_url, category, abbreviation, title in papers]
