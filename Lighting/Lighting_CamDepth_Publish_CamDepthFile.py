# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft

path_obj = pft.PathDetails.parse_path(pm.sceneName())
seq = path_obj.seq
shot = path_obj.shot
publishdir = os.path.dirname(path_obj.getPublishFullPath())


def run():
    return
