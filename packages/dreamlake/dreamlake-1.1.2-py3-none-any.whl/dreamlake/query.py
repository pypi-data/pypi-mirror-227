# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25

import time
import warnings
import cx_Oracle
import pandas as pd
from dreamlake import connection
from dreamlake import parser
from prettytable import PrettyTable

warnings.filterwarnings("ignore")


def create_pretty_table(data_list, headers):
    table = PrettyTable()
    table.field_names = headers

    for row in data_list:
        table.add_row(row)

    return table


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("\033[92m程序运行结束，运行时间{:.0f}小时{:.0f}分{:.2f}秒.\033[0m".format(hours, minutes, seconds))


def read_table(usr, file=None, query=None, index=-1, **kwargs):
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)

        if not query:
            query = parser.textfile_search_parse(file, index)

        try:
            table = pd.read_sql(query, con=connect, **kwargs)
            return table
        except Exception as error:
            raise error
        finally:
            connect.close()
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)


def fetch_all(usr, file=None, query=None, index=-1, format_table=True, head=5):
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_search_parse(file, index)

        cursor.execute(query)
        field_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        if format_table:
            table = PrettyTable()
            table.field_names = field_names
            if head:
                for row in result[:head]:
                    table.add_row(row)
            else:
                for row in result:
                    table.add_row(row)
        else:
            table = result

        cursor.close()
        connect.close()

        return table
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)


def fetch_one(usr, file=None, query=None, index=-1, format_table=True):
    start_time = time.time()  # 记录开始时间
    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_search_parse(file, index)

        cursor.execute(query)
        field_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()

        if format_table:
            table = PrettyTable()
            table.field_names = field_names
            table.add_row(result)
        else:
            table = result

        cursor.close()
        connect.close()
        return table
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()  # 记录结束时间
        seconds = end_time - start_time  # 计算运行时间
        seconds_to_hms(seconds)
