import datetime
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource

from conf import HOME_PATH
from utils.common_utils import check_key, check_category, check_year, construct_res_dict, get_search_res

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filemode='w',
                    filename='/var/log/dblpWebBackend.log')

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


class SearchPaper(Resource):
    def post(self):
        data = request.get_json()
        logging.info(data)
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
            args = {'category': category, 'yf': yf, 'yt': yt, 'keys': keys}
            # 获得检索结果
            paper_search_res = get_search_res(args)
            paper_res_dict = construct_res_dict(paper_search_res)
            res = {'papers': paper_res_dict}
            return jsonify(res)
        else:
            return 'Nothing', 404


class TestConnect(Resource):
    def get(self):
        return jsonify({'status': 'success'})


@app.errorhandler(404)
def miss(val):
    return 'Nothing', 404


api.add_resource(SearchPaper, '/api/v1/search')
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
