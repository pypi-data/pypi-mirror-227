# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25 23:26

import os
import re


def textfile_search_parse(file, index=-1):
    if not os.path.exists(file):
        raise FileNotFoundError("没有找到相关的文件")

    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 去除 /* */ 注释内容
    text_without_comments = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

    # 去除每行开头的 -- 注释
    text_lines = text_without_comments.split('\n')
    text_without_comments = '\n'.join(line for line in text_lines if not line.strip().startswith('--'))

    # 使用正则表达式来匹配 SQL 语句
    sql_statements = re.split(r';\s*(?!--)', text_without_comments)
    # 去掉分号和空元素
    sql_statements = [sql.replace(";", "").strip() for sql in sql_statements if sql.strip()]

    if not sql_statements:
        raise ValueError("没有识别到相关的SQL语句，请检查输入是否有误")

    if index:
        return sql_statements[index]
    else:
        return sql_statements


def textfile_proceduce_parser(file, index=-1):
    if not os.path.exists(file):
        raise FileNotFoundError("没有找到相关的文件")

    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()

    sql_blocks = re.findall(r"(declare.*?end;)", text, re.DOTALL)

    if index:
        return sql_blocks[index]
    else:
        return sql_blocks
