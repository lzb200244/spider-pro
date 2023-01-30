# -*- coding: utf-8 -*-
# @Time : 2023/1/9 22:29
# @Site : https://www.codeminer.cn 
"""
file-name:test_concurrence
ex:
"""
import time

import __init__script

from concurrent.futures import ThreadPoolExecutor

from apps.spider.models import MovieDetail

pool = ThreadPoolExecutor(50)


def task(i):
    objs = MovieDetail.objects.first()
    print('开始了')

    if objs.movie_rate != 0:
        objs.movie_rate -= i
        objs.save()
    time.sleep(0.2)


for i in range(50):
    res = pool.submit(task, i)
print(MovieDetail.objects.first().movie_rate)
