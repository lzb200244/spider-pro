# -*- coding: utf-8 -*-
# @Time : 2022/12/23 20:53
# @Site : https://www.codeminer.cn 
"""
ex:离线脚本
"""
# offline_script.py

import os
import sys
import django


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backstage.settings.dev")
django.setup()
