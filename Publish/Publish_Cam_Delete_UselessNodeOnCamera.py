# coding:utf-8
import pymel.core as pm


def run():
    imagePlanes = pm.ls(type='imagePlane')
    if imagePlanes:
        pm.delete(imagePlanes)
    greasePlanes = pm.ls(type='greasePlane')
    if greasePlanes:
        pm.delete(greasePlanes)
    pm.warning(u'删除相机上不需要的节点完毕')
