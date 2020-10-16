from common import ELASTICSEARCH_INDEX, MAX_THREAD_SIZE


def init_elasticsearch():
    """
    这里之所以是采用这种初始化方式,是因为需要考虑增量更新的问题
    @:returns: 返回es客户端,以及判断是否是首次部署该软件
    """
    from elasticsearch import Elasticsearch
    from common import ELASTICSEARCH_HOST
    es_client = Elasticsearch(ELASTICSEARCH_HOST, maxsize=MAX_THREAD_SIZE+5)
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
