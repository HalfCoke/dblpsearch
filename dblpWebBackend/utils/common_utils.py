import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from conf import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX, ELASTICSEARCH_RES_MAX_NUM


def check_category(category):
    return len(category) != 0


def check_year(yf, yt):
    return 0 < yf <= datetime.datetime.now().year and 0 < yt <= datetime.datetime.now().year


def check_key(keys):
    return keys is not None and len(keys) != 0


def construct_res_dict(paper_search_res):
    # paper_res_dict = {}
    paper_list = []
    for res in paper_search_res:
        # paper_list = paper_res_dict.setdefault(category, [])
        single_paper = {
            "title": res.meta.highlight.title[0],
            "year": res.year,
            "authors": list(res.authors) if hasattr(res, 'authors') else ['NULL'],
            "url": res.ee_url if hasattr(res, 'ee_url') else '#',
            "category": res.category,
            "abbreviation": res.abbreviation
        }
        paper_list.append(single_paper)
    return paper_list


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
    res = search[0:ELASTICSEARCH_RES_MAX_NUM].execute()
    return res
