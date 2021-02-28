import logging
import time

import pytz
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from common import HOME_PATH
from main_prog import init_elasticsearch
from main_prog.background_utils_function import parse_xml, read_gz_file
# 后台程序调度器
from main_prog.utils_function import save_doc_to_elastic

background_program = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))


@background_program.scheduled_job('cron', day_of_week=0,
                                  args=["https://dblp.org/xml/dblp.xml.gz", HOME_PATH + "/resources/dblp.xml.gz"])
@background_program.scheduled_job('cron', day_of_week=0,
                                  args=["https://dblp.org/xml/dblp.dtd", HOME_PATH + "/resources/dblp.dtd"])
def _download_DBLP_data(url, file_name):
    """
每天凌晨3点，自动下载xml数据，存入resources路径
    """
    r = requests.get(url, stream=True)
    with open(file_name, "wb") as f:
        for ch in r.iter_content(chunk_size=512):
            f.write(ch)


@background_program.scheduled_job('cron', hour=3)
def _export_DBLP_paper():
    """
    解析XML文件内容,然后将其存入Elasticsearch
    """
    # 初始化elasticsearch的状态, 获得es的客户端
    es_client, is_first_run = init_elasticsearch()
    xml_file = read_gz_file(HOME_PATH + '/resources/dblp.xml.gz')
    paper_category_link_dict = {}
    papers = parse_xml(xml_file, paper_category_link_dict)
    save_doc_to_elastic(is_first_run, papers, paper_category_link_dict, es_client)


def init_DBLP_paper(val):
    time.sleep(val)
    _export_DBLP_paper()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s  %(message)s',
        datefmt='%Y-%m-%d %A %H:%M:%S'
    )

    _export_DBLP_paper()
