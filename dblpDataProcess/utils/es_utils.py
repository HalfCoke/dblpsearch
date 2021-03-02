import logging
from concurrent import futures
from datetime import datetime
from elasticsearch_dsl import Document, Search

from conf import ELASTICSEARCH_INDEX, MAX_THREAD_SIZE


def init_elasticsearch():
    """
    这里之所以是采用这种初始化方式,是因为需要考虑增量更新的问题
    @:returns: 返回es客户端,以及判断是否是首次部署该软件
    """
    from elasticsearch import Elasticsearch
    from conf import ELASTICSEARCH_HOST
    es_client = Elasticsearch(ELASTICSEARCH_HOST, maxsize=MAX_THREAD_SIZE + 5)
    is_first_run = not es_client.indices.exists(ELASTICSEARCH_INDEX)
    # 程序第一次运行
    if is_first_run:
        from elasticsearch_dsl import Mapping, Text, Long, Keyword, Index
        dblp_paper_mapping = Mapping()
        # 添加字段及其类型
        # 文章标题字段, 两种检索模式
        dblp_paper_mapping.field("title", Text(analyzer="english", fields={'raw': Keyword()}))
        # 文章作者
        dblp_paper_mapping.field("authors", Text(analyzer="english", fields={'raw': Keyword()}))
        # 文章发表年份
        dblp_paper_mapping.field("year", Long())
        # 文章所在的会议/期刊的简称
        dblp_paper_mapping.field("abbreviation", Keyword())
        # 文章所在的会议/期刊的类别A B C
        dblp_paper_mapping.field("category", Keyword())
        # 文章所在会议(用来内部使用的key)
        dblp_paper_mapping.field("crossref", Keyword())
        # 文章的链接(指向IEEE, ACM等官方发布的地址)
        dblp_paper_mapping.field("ee_url", Keyword())
        # 将该映射存入索引dblp_cata_paper_elastic中
        dblp_paper_index = Index("dblp_cata_paper_elastic", using=es_client)
        dblp_paper_index.mapping(dblp_paper_mapping)
        dblp_paper_index.settings(auto_expand_replicas="0-1")
        dblp_paper_index.save()
    return es_client, is_first_run


def save_doc_to_elastic(is_first_run, papers, paper_category_link_dict, es_client):
    if is_first_run:
        logging.info("程序首次执行...")
        with futures.ThreadPoolExecutor(max_workers=MAX_THREAD_SIZE) as executor:
            # 用来防止提交任务时直接全部遍历迭代器,造成内存溢出
            job_list = []
            for paper in papers:
                job_list.append(executor.submit(_save_doc, paper, paper_category_link_dict, es_client))
                if len(job_list) == MAX_THREAD_SIZE:
                    for job in futures.as_completed(job_list):
                        job_list.remove(job)
                        break

    else:
        logging.info("程序非首次执行, 进行增量更新...")
        # 先删除当前年份
        cu_year = datetime.now().year
        search = Search(using=es_client, index=ELASTICSEARCH_INDEX) \
            .query("match", year=cu_year)
        search.delete()
        with futures.ThreadPoolExecutor(max_workers=MAX_THREAD_SIZE) as executor:
            job_list = []
            for paper in papers:
                # 增量更新,只使用最新一年的
                if int(paper.find('year').text) == cu_year:
                    job_list.append(executor.submit(_save_doc, paper, paper_category_link_dict, es_client))
                    if len(job_list) == MAX_THREAD_SIZE:
                        for job in futures.as_completed(job_list):
                            job_list.remove(job)
                            break


def _save_doc(paper, paper_category_link_dict, es_client):
    paper_doc = get_paper_doc(paper, paper_category_link_dict["link"])
    Document(**paper_doc).save(index=ELASTICSEARCH_INDEX, using=es_client)


def get_paper_doc(paper, paper_category):
    publish_name = paper.get('key').split('/')[1]
    paper_doc = {
        "title": _find_title(paper),
        "authors": [author.text for author in paper.findall('author')],
        "year": int(paper.findtext('year')),
        "abbreviation": publish_name,
        "crossref": paper.findtext("crossref"),
        "category": paper_category[publish_name],
        "ee_url": paper.findtext('ee', default='none')
    }
    return paper_doc


def _find_title(elem):
    title = ""
    title_elem = elem.find('title')
    title += _find_text(title_elem)

    children = title_elem.getchildren()
    if children:
        title += children[-1].tail if children[-1].tail else ""
    if title[-1] != ".":
        title += "."
    return title.strip()


def _find_text(title_elem):
    title = ""
    if title_elem.text:
        title += title_elem.text.strip()
    children = title_elem.getchildren()
    for child in children:
        title += _find_text(child)
    return title
