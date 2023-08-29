'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-03-27 16:29:57
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-08-16 14:53:30
FilePath: /py-minium/minium/miniprogram/base_driver/version.py
Description: minium build version
'''
import os
import json

g_version = None
def build_version():
    global g_version
    if g_version:
        return g_version
    config_path = os.path.join(os.path.dirname(__file__), "version.json")
    if not os.path.exists(config_path):
        return {}
    else:
        with open(config_path, "r", encoding="utf8") as f:
            version = json.load(f)
            g_version = version
            return version