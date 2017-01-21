# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft
import shutil


def run():
    if not pm.ls('CamFocus:Camera'):
        pm.warning(u'没有可以导出的相机')
        return

    if pm.ls(type='unknown'):
        pm.delete(pm.ls(type='unknown'))

    path_obj = pft.PathDetails.parse_path(pm.sceneName())
    pubfile = path_obj.getNewVersionForTask('cam-focus', publish=True)
    if not pubfile:
        pm.warning(u'请检查本场景文件的路径,特别注意下文件名本身')
        return
    os.makedirs(os.path.dirname(pubfile))

    projectdir = pm.Workspace.getPath()
    imagedir = os.path.join(projectdir, 'images')
    # os.makedirs(os.path.join(os.path.dirname(pubfile), 'images'))
    # pm.sysFile(imagedir, copy=os.path.join(os.path.dirname(pubfile), 'images'))
    shutil.copytree(imagedir, os.path.join(os.path.dirname(pubfile), 'images'))

    pm.select(pm.ls('CamFocus:Camera'), r=True)
    pm.exportSelected(os.path.splitext(pubfile)[0] + '.ma', force=True)
    pm.saveAs(os.path.join(os.path.dirname(pubfile), os.path.basename(pm.sceneName())))

    pm.warning(u'导出CamFocus相机完成,文件另存为完成')
