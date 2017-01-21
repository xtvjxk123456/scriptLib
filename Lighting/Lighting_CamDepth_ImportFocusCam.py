# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import os


def get_latest_camera():
    try:
        path_obj = pft.PathDetails.parse_path(pm.sceneName())
    except Exception:
        pm.warning(u'场景文件名不正确')
        return None
    path_obj.task = 'cam'
    publishcamfile = path_obj.getPublishFullPath()
    mafile = os.path.splitext(publishcamfile)[0]+'.ma'
    mbfile = os.path.splitext(publishcamfile)[0]+'.ma'
    if os.path.exists(mbfile):
        return mbfile
    else:
        if os.path.exists(mafile):
            return mafile
        else:
            return None


def run():
    camfile = get_latest_camera()
    if camfile:
        pm.createReference(camfile,namespace='CamFocus')
    else:
        pm.warning(u'请检查场景文件名或者cam publish目录....')
