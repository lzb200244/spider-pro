# import subprocess
#
# cmd = "celery -A mycelery.delay_task.spider.main worker -l info -P eventlet"
# process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, error = process.communicate()
#
# print(output.decode())
# print(error.decode())
# # (venv) C:\Users\Administrator\Desktop\project\spider-pro\backstage>celery -A mycelery.async_task.main worker -l info -P eventlet
