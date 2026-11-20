import logging
import threading

import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from conf import HOME_PATH
from utils.common_utils import read_gz_file
from utils.dblp_data.parse_data import parse_xml
from utils.sqlite_utils import save_docs_to_sqlite

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
    每周自动下载xml数据，存入resources路径
    """
    r = requests.get(url, stream=True)
    with open(file_name, "wb") as f:
        for ch in r.iter_content(chunk_size=512):
            f.write(ch)


@blocking_scheduler.scheduled_job('cron', hour=3)
def _export_DBLP_paper():
    """
    解析XML文件内容,然后将其存入SQLite检索库
    """
    xml_file = read_gz_file(HOME_PATH + '/resources/dblp.xml.gz')
    if xml_file is None:
        logging.warning("未找到dblp.xml.gz, 跳过本次写入")
        return
    paper_category_link_dict = {}
    papers = parse_xml(xml_file, paper_category_link_dict)
    save_docs_to_sqlite(papers, paper_category_link_dict["link"])


if __name__ == '__main__':
    logging.info("当前程序运行路径: " + HOME_PATH)
    logging.info("数据初始化程序开始运行....")
    threading.Thread(target=_export_DBLP_paper, daemon=True).start()
    blocking_scheduler.start()
