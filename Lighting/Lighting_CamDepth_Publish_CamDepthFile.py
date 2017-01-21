# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft


path_obj = pft.PathDetails.parse_path(pm.sceneName())
seq = path_obj.seq
shot = path_obj.shot
publishdir = os.path.dirname(path_obj.getPublishFullPath())


def run():
    pm.select(pm.ls('CamFocus:Camera'))
    if pm.ls(type='unknown'):
        pm.delete(pm.ls(type='unknown'))
    publishFocus = os.path.join(publishdir, 'CamFocus/{}_{}_{}_cam.ma'.format(path_obj.project, path_obj.seq, path_obj.shot))
    os.makedirs(os.path.dirname(os.path.normpath(publishFocus)))
    pm.exportSelected(os.path.normpath(publishFocus),force=True)

    pm.saveAs(os.path.join(os.path.dirname(os.path.normpath(publishFocus)),os.path.basename(pm.sceneName())))

    pm.warning(u'导出CamFocus相机完成,文件另存为完成')
