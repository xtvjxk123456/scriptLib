#coding:utf-8
import os
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import aas_sg
import logging

#ROOT_DIR = "Q:/ants/Env_GPUCache"
LOG_FILENAME = 'Q:/ants/Env_GPUCache/20160831.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def export_env_gpu_cache(ROOT_DIR):
    top_node = pm.ls("*_mdl*", assemblies=True)
    if not top_node:
        logging.warning("no top node found in %s" % pm.sceneName())
        return
    
    top_node = top_node[0]
    SG_nodes = top_node.getChildren()
    # get pub path
    path_obj = pft.PathDetails.parse_path(pm.sceneName())
    asset_name = path_obj.shot
    pub_dir = "%s/%s" % (ROOT_DIR, asset_name)
    for SG_node in SG_nodes:
        try:
            pm.gpuCache(SG_node.name(),
                        startTime=1, 
                        endTime=1,
                        optimize=True, 
                        optimizationThreshold=40000,
                        directory=pub_dir,
                        fileName=SG_node.name()
                        )
        except Exception, e:
            logging.warning(e)

ROOT_DIR = [
            u"Z:\Resource\Share\s苏娜\Shotgun\projects\df\Env_GPUCache",
            r"Q:/ants/Env_GPUCache",
            r'Z:/Shotgun/projects/df/Env_GPUCache'
            ]

def run():
    map(export_env_gpu_cache,ROOT_DIR)
