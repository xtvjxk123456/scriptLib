#coding:utf-8
import os
import pixoLibs.pixoFileTools as pft
import aas_sg
import pymel.core as pm




ROOT_DIR = [
            r'Z:/Shotgun/projects/df/Env_GPUCache',
            r"Q:/ants/Env_GPUCache",
            u"Z:\Resource\Share\s苏娜\Shotgun\projects\df\Env_GPUCache",
            ]

def opendir(x):
    path_obj = pft.PathDetails.parse_path(pm.sceneName())
    asset_name = path_obj.shot
    pub_dir = "%s/%s" % (x, asset_name)
    os.startfile(pub_dir.encode('gbk'))


def run():
    map(opendir,ROOT_DIR)
