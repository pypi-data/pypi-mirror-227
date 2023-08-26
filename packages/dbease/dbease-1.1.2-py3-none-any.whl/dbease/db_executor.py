# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/25 1:01

import time
import warnings
import cx_Oracle
from dbease import connection
from dbease import parser

warnings.filterwarnings('ignore')


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("\033[92m程序运行结束，运行时间{:.0f}小时{:.0f}分{:.2f}秒.\033[0m".format(hours, minutes, seconds))


def to_execute(usr, file=None, query=None, index=None, commit=False, series=False, tolerant=False):
    start_time = time.time()

    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_search_parse(file, index)
            print(query)

        try:
            if series:  # 跑多个语句
                if not isinstance(query, list):
                    query = [query]

                error_count = 0
                for item in query:
                    print(item)
                    try:
                        cursor.execute(item)
                    except Exception as error:
                        error_count += 1
                        if not tolerant:
                            raise error
                        else:
                            print("\033[94m异常代码：\n{}\033[0m".format(item))
                            print("\033[91m\U0001F622 {}\033[0m".format(error))

                if commit:
                    if error_count == 0:
                        connect.commit()
                    else:
                        connect.rollback()
            else:  # 跑单个语句
                try:
                    cursor.execute(query)
                    if commit:
                        connect.commit()
                except Exception as error:
                    print("\033[94m异常代码：\n{}\033[0m".format(query))
                    raise error

        except Exception as error:
            raise error

        finally:
            cursor.close()
            connect.close()

    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()
        seconds = end_time - start_time
        seconds_to_hms(seconds)


def to_proceduce(usr, file=None, query=None, index=None, series=False, tolerant=False):
    start_time = time.time()

    try:
        connect = connection.get_connection_from_pool(usr)
        cursor = connect.cursor()

        if not query:
            query = parser.textfile_proceduce_parser(file, index)

        try:
            if series:  # 跑多个语句
                if not isinstance(query, list):
                    query = [query]

                error_count = 0
                for item in query:
                    try:
                        cursor.execute(item)
                    except Exception as error:
                        error_count += 1
                        if not tolerant:
                            raise error
                        else:
                            print("\033[94m异常代码：\n{}\033[0m".format(item))
                            print("\033[91m\U0001F622 {}\033[0m".format(error))

            else:  # 跑单个语句
                try:
                    cursor.execute(query)
                except Exception as error:
                    print("\033[94m异常代码：\n{}\033[0m".format(query))
                    raise error
        except Exception as error:
            raise error
    except cx_Oracle.Error as error:
        raise error
    finally:
        end_time = time.time()
        seconds = end_time - start_time
        seconds_to_hms(seconds)
