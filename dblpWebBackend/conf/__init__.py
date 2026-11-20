#########################################################################################################
# dblp_web_backend与dblp_data_process容器公共配置部分
#########################################################################################################
import os

HOME_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/conf')

# 论文检索库（SQLite + FTS5），数据进程写入，Web 后端只读查询
SQLITE_DB_PATH = os.environ.get('DBLP_DB_PATH', HOME_PATH + '/db/dblp.sqlite')

#########################################################################################################
# dblp_web_backend容器配置部分
#########################################################################################################
# 检索结果分页配置
SEARCH_DEFAULT_PAGE_SIZE = 20
SEARCH_MAX_PAGE_SIZE = 100

# Redis配置部分
REDIS_HOST = "search_data_storage"
REDIS_PORT = 6379
MOST_SEARCH_WORD = "most_search_word"
RECENT_WORD = "recent_search"
#########################################################################################################
# dblp_data_process容器配置部分
#########################################################################################################
# 单次批量写入SQLite的论文条数
DB_BATCH_SIZE = 20000

# xml文档中文章的标签
# PAPER_TAG = ['article', 'inproceedings', 'proceedings']
# 去掉proceedings是因为proceedings是会议论文集,这个版本暂时不链接论文集
PAPER_TAG = ['article', 'inproceedings']
# 期刊目录文件的路径
PAPER_CATALOGUE = HOME_PATH + '/resources/upload/中国计算机学会推荐国际学术会议和期刊目录.pdf'
