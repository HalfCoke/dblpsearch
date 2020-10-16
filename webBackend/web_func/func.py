import datetime


def check_category(category):
    return len(category) != 0


def check_year(yf, yt):
    return 0 < yf <= datetime.datetime.now().year and 0 < yt <= datetime.datetime.now().year


def check_key(keys):
    return keys is not None and len(keys) != 0


def construct_res_dict(paper_search_res):
    paper_res_dict = {}
    for res in paper_search_res:
        category = res.category
        paper_list = paper_res_dict.setdefault(category, [])
        paper_list.append(res.meta.highlight.title[0] + " " + str(res.year) + " " + res.abbreviation)
    return paper_res_dict
