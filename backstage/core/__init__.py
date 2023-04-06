# from redis import Redis
# from selenium import webdriver
#
#
# # diver = webdriver.Firefox()
# # try:
# #     diver.get('http://codeminer.cn')
# #     print(diver.page_source)
# # finally:
# #     diver.quit()
# #     diver.close()
# class SS:
#     def __init__(self):
#         print('进来了')
#
#     def open(self):
#         print('打开了')
#
#     def close(self):
#         print('关闭了')
#
#     def __enter__(self):
#         self.open()
#         print('开始了')
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # print(exc_tb)  #
#         # print(exc_val)  # 异常值
#         # print(exc_type)  # 异常类型
#         print('结束了')
#
#
# with SS() as s:
#     print(s)
#     print(1)
