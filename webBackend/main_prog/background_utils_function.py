import gzip
import logging
import os
import re
from time import time
from xml.etree import ElementTree
from xml.etree.ElementTree import iterparse

import pdfplumber

from common import HOME_PATH


def read_gz_file(file_name):
    """
函数读取gz文件，然后返回一个生成器，每个元素为文件中的行
    :param file_name: 文件名
    """
    if os.path.exists(file_name):
        return gzip.open(file_name, 'rt')


def get_xml_entity(dblp_dtd):
    """
    :param dblp_dtd: 文本文件的迭代器对象
    :return: 返回xml Entity的字典
    """
    xml_entity = {}
    pattern = re.compile(r'<!ENTITY ([a-zA-Z]*)\s*"(\S*)"[\s\S]*')
    for line in dblp_dtd:
        s = pattern.findall(line)
        if len(s) != 0:
            xml_entity[s[0][0]] = s[0][1]
    return xml_entity


def read_pdf_file(file_name):
    """
    使用期刊目录的pdf文件，获取各个类别的会议、期刊的dblp链接
    :param file_name:
    :return:
    """
    with pdfplumber.open(file_name) as f:
        paper_catalogue_link = {}
        pre_catalogue = ''
        for i in range(1, len(f.pages)):
            logging.info("处理pdf：第{}页".format(i))
            page = f.pages[i]
            has_catalogue_or_not = _judge_has_catalogue(page.extract_text())
            if has_catalogue_or_not is not None:
                # 如果当前页有类别，则存入变量pre_catalogue中
                pre_catalogue = has_catalogue_or_not
                # 以链接为key,类别为键,存入字典
                table_info = page.extract_table()
                # 获取除表头以外的内容，将链接存入列表
                for line_index in range(1, len(table_info)):
                    paper_catalogue_link[table_info[line_index][-1]] = pre_catalogue
            else:
                # 如果当前页没有类别，则说明与上一页类别相同，且没有表头
                # 获取对应类别的字典，准备将链接存入字典
                table_info = page.extract_table()
                # 将链接存入列表
                for line_index in range(len(table_info)):
                    paper_catalogue_link[table_info[line_index][-1]] = pre_catalogue
    return paper_catalogue_link


def _judge_has_catalogue(content):
    """
    根据当前pdf页的文本内容，判断是否有类别，如果有，则返回类别，如果没有则返回None
    :param content: pdf一页的文本内容
    :return: 如果有类别，则返回响应类别，如果没有则返回None
    """
    res = content.split('、')
    if len(res) != 2:
        return None
    else:
        return res[-1][0]


def read_links_from_text(file_name):
    """
从包含链接的文本文件中读取
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as f:
        conference_name = _get_conference_name(f.readlines())
    return conference_name


def _get_conference_name(conference_links):
    """
    从链接中，得到dblp链接中对会议或期刊的简称
    :param conference_links_list:
    :return:
    """
    return conference_links.split('/')[5].strip()


def _pre_parse_xml():
    """
进行解析xml文档的一些准备工作
    :return: path_parts是在进行xml解析的时候匹配xml的tag
    :return: xml_entity是xml中实体对应的字典，如果没有这个会解析失败
    :return: paper_catalogue_link是一个字典，key分别为'A','B','C',对应的值为相应类别的会议、期刊的简称。
    """
    from common import PAPER_TAG
    # 这个列表是为了在进行xml解析的时候匹配tag
    # 这个split是为了将字符串path转换为列表
    # [['dblp', 'article'], ['dblp', 'inproceedings'], ['dblp', 'proceedings']]
    path_parts = [['dblp'] + path.split('/') for path in PAPER_TAG]

    # 将xml entity从dblp.dtd读入内存
    with open(HOME_PATH + '/resources/dblp.dtd', 'r') as f:
        xml_entity = get_xml_entity(f.readlines())

    # 获得ABC三类会议、期刊的简写
    from common import PAPER_CATALOGUE
    start_time = time()
    paper_catalogue_link = read_pdf_file(PAPER_CATALOGUE)
    logging.info("处理PDF花费: " + str(int(time() - start_time)) + " s")
    # {会议\期刊简称:会议类别的字典}
    paper_cata = {}
    for key, value in paper_catalogue_link.items():
        try:
            paper_cata[_get_conference_name(key)] = value
        except:
            pass
    return path_parts, xml_entity, paper_cata


def _find_text(title_elem):
    title = ""
    if title_elem.text:
        title += title_elem.text.strip()
    children = title_elem.getchildren()
    for child in children:
        title += _find_text(child)
    return title


def _find_title(elem):
    title = ""
    title_elem = elem.find('title')
    title += _find_text(title_elem)

    children = title_elem.getchildren()
    if children:
        title += children[-1].tail if children[-1].tail else ""
    if title[-1] != ".":
        title += "."
    return title.strip()


def parse_xml(xml_file, paper_category_link_dict):
    # 获得解析器
    parse = ElementTree.XMLParser()
    # 获得解析xml时的一些变量
    path_parts, xml_entity, paper_category_link = _pre_parse_xml()
    paper_category_link_dict["link"] = paper_category_link
    # 设定解析器参数
    for key, value in xml_entity.items():
        parse.entity[key.strip()] = value

    # 迭代解析xml文本
    xml_data = iterparse(xml_file, ('start', 'end'), parser=parse)
    # 标签数量统计字典
    tag_count_dict = {}
    # xml标签栈
    tag_stack = []
    # xml元素栈
    elem_stack = []
    for event, elem in xml_data:
        # 如果是开始标签
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        # 如果是结束标签
        elif event == 'end':
            # 此时的标签栈符合设定
            if tag_stack in path_parts:
                keys = elem.get('key').split('/')
                # 将三个类别的会议简称进行合并判断，方便从xml中筛选出所有符合要求的文章
                if keys[0] in ['conf', 'journals'] and keys[1] in paper_category_link.keys():
                    yield elem
            if len(tag_stack) == 2:
                count = tag_count_dict.setdefault(tag_stack[-1], 0)
                if count % 10000 == 0:
                    logging.info("清除标签: {tag}, 共{count}个".format(tag=tag_stack[-1], count=count))
                tag_count_dict[tag_stack[-1]] = count + 1
                elem_stack[-2].clear()
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
