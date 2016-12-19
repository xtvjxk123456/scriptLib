# coding:utf-8
import pixoMaya.td_tools as td_tools
import pymel.core as pm


def run():
    if pm.ls(sl=True):
        td_tools.replace_selected_ref_with_proxy()
    else:
        pm.warning(u'请先选中需要替换的参考内容')
