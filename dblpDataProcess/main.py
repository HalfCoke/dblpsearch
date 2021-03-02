import logging
import time
import _thread
import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from conf import HOME_PATH, INIT_WAIT_TIME
from utils.common_utils import read_gz_file
from utils.dblp_data.parse_data import parse_xml
from utils.es_utils import init_elasticsearch, save_doc_to_elastic

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filemode='w',
                    filename='/var/log/dblpDataProcess.log')
blocking_scheduler = BlockingScheduler(timezone=pytz.timezone('Asia/Shanghai'))


@blocking_scheduler.scheduled_job('cron', day_of_week=0,
                                  args=["https://dblp.org/xml/dblp.xml.gz", HOME_PATH + "/resources/dblp.xml.gz"])
@blocking_scheduler.scheduled_job('cron', day_of_week=0,
                                  args=["https://dblp.org/xml/dblp.dtd", HOME_PATH + "/resources/dblp.dtd"])
def _download_DBLP_data(url, file_name):
    """
    每天凌晨3点，自动下载xml数据，存入resources路径
    """
    r = requests.get(url, stream=True)
    with open(file_name, "wb") as f:
        for ch in r.iter_content(chunk_size=512):
            f.write(ch)


@blocking_scheduler.scheduled_job('cron', hour=3)
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
    logging.info("数据初始化程序开始运行....")
    _export_DBLP_paper()
    logging.info("数据初始化程序运行完成")


if __name__ == '__main__':
    logging.info("当前程序运行路径: " + HOME_PATH)
    logging.info(f"等待{INIT_WAIT_TIME}秒后运行数据初始化程序...")
    _thread.start_new_thread(init_DBLP_paper, (INIT_WAIT_TIME,))
    blocking_scheduler.start()
