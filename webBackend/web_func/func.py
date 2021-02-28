import datetime


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
            "authors": list(res.authors),
            "url": res.ee_url,
            "category": res.category,
            "abbreviation": res.abbreviation
        }
        paper_list.append(single_paper)
    return paper_list
