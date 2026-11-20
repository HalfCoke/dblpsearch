import json
import logging
import os
import sqlite3
from datetime import datetime

from conf import DB_BATCH_SIZE, SQLITE_DB_PATH

# 标题做全文索引，其余字段只存储不索引（UNINDEXED）
# porter 词干化 + unicode61 分词，对应原 ES 的 english analyzer
CREATE_TABLE_SQL = """
    CREATE VIRTUAL TABLE papers USING fts5(
        title,
        authors UNINDEXED,
        year UNINDEXED,
        abbreviation UNINDEXED,
        category UNINDEXED,
        ee_url UNINDEXED,
        tokenize = 'porter unicode61'
    )
"""

INSERT_SQL = "INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?)"


def open_db():
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA cache_size = -64000")
    conn.execute("PRAGMA temp_store = MEMORY")
    return conn


def save_docs_to_sqlite(papers, paper_category_link_dict):
    """
    首次运行全量写入，之后仅重建当年数据（增量更新）
    :param papers: parse_xml返回的生成器，遍历过程中才会填充paper_category_link_dict
    """
    conn = open_db()
    try:
        is_first_run = not _has_papers(conn)
        if is_first_run:
            logging.info("程序首次执行, 全量写入检索库...")
            conn.execute("DROP TABLE IF EXISTS papers")
            conn.execute(CREATE_TABLE_SQL)
            year_filter = None
        else:
            year_filter = datetime.now().year
            logging.info("程序非首次执行, 删除%d年数据后增量更新..." % year_filter)
            conn.execute("DELETE FROM papers WHERE year = ?", (str(year_filter),))
        count = _batch_insert(conn, papers, paper_category_link_dict, year_filter)
        conn.commit()
        conn.execute("PRAGMA optimize")
        logging.info("写入检索库完成, 共%d条" % count)
    finally:
        conn.close()


def _has_papers(conn):
    sql = "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'papers'"
    if conn.execute(sql).fetchone() is None:
        return False
    return conn.execute("SELECT 1 FROM papers LIMIT 1").fetchone() is not None


def _batch_insert(conn, papers, paper_category_link_dict, year_filter):
    batch = []
    total = 0
    paper_category_link = None
    for paper in papers:
        # 生成器遍历时parse_xml才会解析PDF并填充该字典
        if paper_category_link is None:
            paper_category_link = paper_category_link_dict["link"]
        row = get_paper_row(paper, paper_category_link)
        if row is None:
            continue
        if year_filter is not None and row[2] != str(year_filter):
            continue
        batch.append(row)
        if len(batch) >= DB_BATCH_SIZE:
            conn.executemany(INSERT_SQL, batch)
            total += len(batch)
            logging.info("已写入%d条" % total)
            batch.clear()
    if batch:
        conn.executemany(INSERT_SQL, batch)
        total += len(batch)
    return total


def get_paper_row(paper, paper_category):
    publish_name = paper.get('key').split('/')[1]
    if publish_name not in paper_category:
        return None
    year = paper.findtext('year')
    title = _find_title(paper)
    if not year or not title:
        return None
    return (
        title,
        json.dumps([author.text for author in paper.findall('author')], ensure_ascii=False),
        str(int(year)),
        publish_name,
        paper_category[publish_name],
        paper.findtext('ee', default='none')
    )


def _find_title(elem):
    title = ""
    title_elem = elem.find('title')
    title += _find_text(title_elem)
    if not title:
        return ""

    children = list(title_elem)
    if children:
        title += children[-1].tail if children[-1].tail else ""
    if title[-1] != ".":
        title += "."
    return title.strip()


def _find_text(title_elem):
    title = ""
    if title_elem is None:
        return title
    if title_elem.text:
        title += title_elem.text.strip()
    for child in title_elem:
        title += _find_text(child)
    return title
