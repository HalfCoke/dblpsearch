import logging
from concurrent import futures
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Search

from common import ELASTICSEARCH_INDEX, MAX_THREAD_SIZE, ELASTICSEARCH_HOST
from main_prog.background_utils_function import _find_title


def _del_black(string):
    """
删除字符串中的多余空格，比如单词之间多余的空格，字符串首尾多余的空格
将每个单词作为列表返回
    :param string:
    :return:
    """
    string_tmp = []
    for c in string.strip().split(" "):
        if len(c) != 0:
            string_tmp.append(c)
    return string_tmp


def parse_keys(keys):
    """
解析检索字符串
    :param keys:
    :return:
    """
    sin_word, com_word = [], []
    sin_tmp, com_tmp = '', ''
    is_sin = True
    for char in keys:
        if char == '"':
            if is_sin:
                sin_word += _del_black(sin_tmp)
                sin_tmp = ''
            else:
                com_word.append(" ".join(_del_black(com_tmp)))
                com_tmp = ''
            is_sin = not is_sin
            continue
        if is_sin:
            sin_tmp += char
        else:
            com_tmp += char
    sin_word += _del_black(sin_tmp)
    if len(com_tmp) != 0:
        com_word.append(" ".join(_del_black(com_tmp)))
    return sin_word + com_word


def _get_paper_from_file(file_path, key_list):
    # 从一个文件中获得包含关键字的标题，然后返回一个文章列表
    res_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            for key in key_list:
                if key.lower() in line.lower():
                    res_list.append(line.strip())
                    break
    return res_list


def get_search_res(args):
    es_client = Elasticsearch(ELASTICSEARCH_HOST)
    search = Search(using=es_client, index=ELASTICSEARCH_INDEX).highlight_options() \
        .query("match", title=args.get("keys")) \
        .filter("terms", category=args.get("category", ["A", "B", "C"])) \
        .filter('range',
                **{"year": {"from": min(args.get("yf"), args.get("yt")), "to": max(args.get("yf"), args.get("yt"))}}) \
        .highlight("title") \
        .highlight_options(pre_tags='<span class="highlight">', post_tags="</span>")
    # .sort("-year")
    res = search[0:1500].execute()
    return res


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


def _save_doc(paper, paper_category_link_dict, es_client):
    paper_doc = get_paper_doc(paper, paper_category_link_dict["link"])
    Document(**paper_doc).save(index=ELASTICSEARCH_INDEX, using=es_client)


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
