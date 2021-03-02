import gzip
import os
import re


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
