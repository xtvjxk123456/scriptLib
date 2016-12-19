# coding:utf-8
import pixoMaya.td_tools as td_tools
import pymel.core as pm


def run():
    if pm.ls(sl=True):
        td_tools.replace_selected_proxy_with_shader_file()
    else:
        pm.warning(u'请先选中需要替换的代理内容')
