# coding:utf-8

import pymel.core as pm


def run():
    needLayer = pm.ls(sl=True)
    for x in needLayer:
        ns = x.name().rpartition(':')[0]
        pm.select(x)
        layer = pm.createDisplayLayer(name=ns + '_layer')
        pm.PyNode(layer).attr('visibility').set(False)
