# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft
#import pixoLibs.pixoShotgun as psg
import shutil


def run():
    if not pm.ls('cam_focus_*'):
        pm.warning(u'没有可以导出的相机')
        return

    if pm.ls(type='unknown'):
        pm.delete(pm.ls(type='unknown'))

    path_obj = pft.PathDetails.parse_path(pm.sceneName())
    pubfile = path_obj.getNewVersionForTask('cam-focus', publish=True)
    if not path_obj.user:
        pm.warning(u'请检查本场景文件的路径,特别注意下文件名本身')
        return
    os.makedirs(os.path.dirname(pubfile))

    # --------------------------------------------------------------------------------------------------------
    # 序列帧输出
    projectdir = pm.Workspace.getPath()
    imagedir = os.path.join(projectdir, 'images')
    # os.makedirs(os.path.join(os.path.dirname(pubfile), 'images'))
    # pm.sysFile(imagedir, copy=os.path.join(os.path.dirname(pubfile), 'images'))
    shutil.copytree(imagedir, os.path.join(os.path.dirname(pubfile), 'images'))
    # --------------------------------------------------------------------------------------------------------
    # 相机输出
    cams = map(lambda x: x.getParent(), filter(lambda x: x.name().startswith('cam_focus_'), pm.ls(type='camera')))
    pm.select(cams)
    camsFile =os.path.splitext(pubfile)[0] + '.ma'
    pm.exportSelected(camsFile, force=True)
    # --------------------------------------------------------------------------------------------------------
    # 上传shotgun
    # psg.addToShotgun(camsFile, '')
    # --------------------------------------------------------------------------------------------------------
    # 输出制作文件
    animSourceFile = os.path.join(os.path.dirname(pubfile), os.path.basename(pm.sceneName()))
    pm.saveAs(animSourceFile)

    # --------------------------------------------------------------------------------------------------------
    # 打开publish目录
    pm.warning(u'导出CamFocus相机完成,文件另存为完成,序列帧复制完成')
    os.startfile(os.path.join(os.path.dirname(pubfile), 'images'))
