#########################################################################################################
# dblp_web_backend与dblp_data_process容器公共配置部分
#########################################################################################################
import os

HOME_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/conf')

# elasticsearch地址
ELASTICSEARCH_HOST = ["es:9200"]
ELASTICSEARCH_INDEX = "dblp_cata_paper_elastic"

#########################################################################################################
# dblp_web_backend容器配置部分
#########################################################################################################
# 需要elasticsearch一次性返回的最大数据条数
ELASTICSEARCH_RES_MAX_NUM = 1500

# Redis配置部分
REDIS_HOST = "search_data_storage"
REDIS_PORT = 6379
MOST_SEARCH_WORD = "most_search_word"
RECENT_WORD = "recent_search"
#########################################################################################################
# dblp_data_process容器配置部分
#########################################################################################################
# 并发写入elasticsearch的线程数量
MAX_THREAD_SIZE = 30

# 初始化函数等待运行的时间，其他服务虽然已经启动，但是也其他服务也需要初始化的过程，
# 因此设置此等待时间可以确保ES已经启动，再进行数据写入
INIT_WAIT_TIME = 30

# xml文档中文章的标签
# PAPER_TAG = ['article', 'inproceedings', 'proceedings']
# 去掉proceedings是因为proceedings是会议论文集,这个版本暂时不链接论文集
PAPER_TAG = ['article', 'inproceedings']
# 期刊目录文件的路径
PAPER_CATALOGUE = HOME_PATH + '/resources/upload/中国计算机学会推荐国际学术会议和期刊目录.pdf'
