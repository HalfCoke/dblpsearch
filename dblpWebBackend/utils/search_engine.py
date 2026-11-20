import json
import logging
import os
import re
import sqlite3
import threading
import time

from conf import SEARCH_DEFAULT_PAGE_SIZE, SEARCH_MAX_PAGE_SIZE, SQLITE_DB_PATH

# 标题高亮标签，与前端样式保持一致
HIGHLIGHT_PRE = '<span class="highlight">'
HIGHLIGHT_POST = '</span>'

# 从用户输入中提取检索词，过滤掉 FTS5 的查询语法字符，避免语法错误
_TOKEN_PATTERN = re.compile(r'[^\W_]+', re.UNICODE)

# 每个线程独享一个连接，uwsgi 多线程模式下避免跨线程复用
_local = threading.local()

# 命中总数缓存：翻页时同一检索条件避免重复统计
_total_cache = {}
_TOTAL_CACHE_TTL = 300
_TOTAL_CACHE_MAX = 512


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
    将用户输入转换为 FTS5 查询，多个检索词之间为 AND 关系，
    即结果必须同时包含全部关键词，保证相关性排序真实有效
    """
    tokens = _TOKEN_PATTERN.findall(keys or '')
    if not tokens:
        return None
    return ' AND '.join('"%s"' % token for token in tokens)


def normalize_sort(sort):
    return 'relevance' if sort == 'relevance' else 'time'


def normalize_page(page):
    try:
        page = int(page)
    except (TypeError, ValueError):
        return 1
    return max(page, 1)


def normalize_page_size(page_size):
    try:
        page_size = int(page_size)
    except (TypeError, ValueError):
        return SEARCH_DEFAULT_PAGE_SIZE
    return min(max(page_size, 1), SEARCH_MAX_PAGE_SIZE)


def _count_matches(conn, match_query, category, yf, yt):
    cache_key = (match_query, tuple(sorted(category)), yf, yt)
    cached = _total_cache.get(cache_key)
    if cached and time.time() - cached[0] < _TOTAL_CACHE_TTL:
        return cached[1]
    placeholders = ','.join(['?'] * len(category))
    sql = """
        SELECT count(*)
        FROM papers
        WHERE papers MATCH ?
          AND category IN ({placeholders})
          AND year BETWEEN ? AND ?
    """.format(placeholders=placeholders)
    params = [match_query] + list(category) + [str(yf), str(yt)]
    total = conn.execute(sql, params).fetchone()[0]
    if len(_total_cache) >= _TOTAL_CACHE_MAX:
        _total_cache.clear()
    _total_cache[cache_key] = (time.time(), total)
    return total


def search_papers(keys, category, yf, yt, sort='time', page=1, page_size=SEARCH_DEFAULT_PAGE_SIZE):
    """
    按标题全文检索，类别与年份过滤后分页返回
    :param sort: time 按发表年份倒序，relevance 按 BM25 相关度
    :return: (当前页论文列表, 命中总数)
    """
    conn = _get_connection()
    match_query = build_match_query(keys)
    if conn is None or match_query is None or not category:
        return [], 0
    sort = normalize_sort(sort)
    page = normalize_page(page)
    page_size = normalize_page_size(page_size)
    yf, yt = min(yf, yt), max(yf, yt)
    try:
        total = _count_matches(conn, match_query, category, yf, yt)
        offset = (page - 1) * page_size
        if total == 0 or offset >= total:
            return [], total
        order = 'bm25(papers), year DESC, rowid DESC' if sort == 'relevance' else 'year DESC, rowid DESC'
        placeholders = ','.join(['?'] * len(category))
        sql = """
            SELECT year, authors, ee_url, category, abbreviation,
                   highlight(papers, 0, ?, ?) AS title
            FROM papers
            WHERE papers MATCH ?
              AND category IN ({placeholders})
              AND year BETWEEN ? AND ?
            ORDER BY {order}
            LIMIT ? OFFSET ?
        """.format(placeholders=placeholders, order=order)
        params = [HIGHLIGHT_PRE, HIGHLIGHT_POST, match_query]
        params += list(category)
        params += [str(yf), str(yt), page_size, offset]
        return conn.execute(sql, params).fetchall(), total
    except sqlite3.Error:
        logging.exception("检索失败, keys=" + str(keys))
        return [], 0


def construct_res_dict(papers):
    return [{
        "title": title,
        "year": int(year),
        "authors": json.loads(authors) if authors else [],
        "url": ee_url,
        "category": category,
        "abbreviation": abbreviation
    } for year, authors, ee_url, category, abbreviation, title in papers]
