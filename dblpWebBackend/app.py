import datetime
import logging
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource

from conf import HOME_PATH, MOST_SEARCH_WORD, SEARCH_DEFAULT_PAGE_SIZE
from utils.common_utils import check_key, check_category, check_year
from utils.search_data import RedisOP, increment_search_data
from utils.search_engine import search_papers, construct_res_dict, \
    normalize_sort, normalize_page, normalize_page_size

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filemode='w',
                    filename='/var/log/dblpWebBackend.log')

app = Flask(__name__)
api = Api(app)
search_word_redis = RedisOP(MOST_SEARCH_WORD)
# CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


class SearchPaper(Resource):
    def post(self):
        data = request.get_json()
        logging.info("收到查询：" + str(data))
        category = data.get('category')
        keys = data.get('keys')
        try:
            yf = int(data.get('yf'))
        except:
            logging.info("未设定起始年份, 自动设置为当前年份")
            yf = datetime.datetime.now().year
        try:
            yt = int(data.get('yt'))
        except:
            logging.info("未设定终止年份, 自动设置为当前年份")
            yt = datetime.datetime.now().year
        # 进行参数检查
        if check_key(keys) and check_category(category) and check_year(yf, yt):
            args = {
                'category': category,
                'yf': yf,
                'yt': yt,
                'keys': keys,
                'sort': normalize_sort(data.get('sort')),
                'page': normalize_page(data.get('page')),
                'page_size': normalize_page_size(data.get('page_size', SEARCH_DEFAULT_PAGE_SIZE))
            }
            threading.Thread(target=increment_search_data, args=(keys, search_word_redis),
                             daemon=True).start()
            # 获得检索结果
            papers, total = search_papers(**args)
            res = {
                'papers': construct_res_dict(papers),
                'total': total,
                'page': args['page'],
                'page_size': args['page_size'],
                'sort': args['sort']
            }
            return jsonify(res)
        else:
            return 'Nothing', 404


class GetSearchWord(Resource):
    def post(self):
        top_k = 100
        recent_k = 10
        data = request.get_json()
        try:
            top_k = data.get("top_k")
            logging.info(f"获取top k请求，k={top_k}")
        except:
            logging.info("获取top k参数失败，使用默认值k=100")
        try:
            recent_k = data.get("recent_k")
            logging.info(f"获取recent k请求，k={recent_k}")
        except:
            logging.info("获取recent k参数失败，使用默认值k=10")
        return jsonify({
            "most_search_word": search_word_redis.get_top_k_word(top_k),
            "recent_search_word": search_word_redis.get_recent_word(recent_k)
        })


class TestConnect(Resource):
    def get(self):
        return jsonify({'status': 'success'})


@app.errorhandler(404)
def miss(val):
    return 'Nothing', 404


api.add_resource(SearchPaper, '/api/v1/search')
api.add_resource(GetSearchWord, '/api/v1/getkeyword')
api.add_resource(TestConnect, '/')
# 开始执行后台任务
# 自动下载dblp数据，并将全部ABC会议、期刊，解析成文本文件，包含期刊名、年份、所发表的机构
logging.info("当前运行路径: " + HOME_PATH)
logging.info("后端服务开始运行...")
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5052
    )
