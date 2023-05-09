# import subprocess
#
# cmd = "celery -A mycelery.delay_task.spider.main worker -l info -P eventlet"
# process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, error = process.communicate()
#
# print(output.decode())
# print(error.decode())
# # (venv) C:\Users\Administrator\Desktop\project\spider-pro\backstage>celery -A mycelery.async_task.main worker -l info -P eventlet
import time

import pandas as pd

# # 第一次读取文件，获取文件总行数
# with open("data.csv") as f:
#     num_lines = len(f.readlines())
#
# # 设定分块大小
# chunk_size = num_lines // 5
# # 逐块读取文件
# from concurrent.futures import ProcessPoolExecutor
#
# # 创建进程池，设置进程数为4
# pool = ProcessPoolExecutor(4)


# 提交任务到进程池中


# 获取任务执行结果
# def handle_data(df):
#     #
#     return df
#
#
# def wrapper(func):
#     def inner(*args, **kwargs):
#         import time
#         t = time.time()
#         res = func(*args, **kwargs)
#         print(func.__name__ + f"总共用时:{time.time() - t}")
#         return res
#
#     return inner
#
#
# def main():
#     print(pd.read_csv("data.csv", ))
#
#
# @wrapper
# def main():
#     pf = None
#     for i, chunk in enumerate(pd.read_csv("data.csv", chunksize=chunk_size)):
#         task = pool.submit(handle_data, chunk)
#
#         pf = pd.concat((pf, task.result()), axis=0)
#     print(pf)
#
#
# if __name__ == '__main__':
#     main()
