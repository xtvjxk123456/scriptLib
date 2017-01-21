# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft


def run():
    if not pm.ls('CamFocus:Camera'):
        pm.warning(u'没有可以导出的相机')
        return

    pm.select(pm.ls('CamFocus:Camera'))
    if pm.ls(type='unknown'):
        pm.delete(pm.ls(type='unknown'))

    path_obj = pft.PathDetails.parse_path(pm.sceneName())
    pubfile = path_obj.getNewVersionForTask('cam-focus', publish=True)
    os.makedirs(os.path.dirname(pubfile))

    pm.exportSelected(pubfile, force=True)
    pm.saveAs(os.path.join(os.path.dirname(pubfile), os.path.basename(pm.sceneName())))

    pm.warning(u'导出CamFocus相机完成,文件另存为完成')
