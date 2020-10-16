# 可能在后续有变化的一些变量

import os

HOME_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/common')

# xml文档中文章的标签
# PAPER_TAG = ['article', 'inproceedings', 'proceedings']
# 去掉proceedings是因为proceedings是会议论文集,这个版本暂时不链接论文集
PAPER_TAG = ['article', 'inproceedings']
# 期刊目录文件的路径
PAPER_CATALOGUE = HOME_PATH + '/resources/upload/中国计算机学会推荐国际学术会议和期刊目录-2019.pdf'

# elasticsearch地址
ELASTICSEARCH_HOST = ["localhost:19200"]
ELASTICSEARCH_INDEX = "dblp_cata_paper_elastic"
# 并发写入elasticsearch的线程数量
MAX_THREAD_SIZE = 30
