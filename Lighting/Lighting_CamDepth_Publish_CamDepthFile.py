# coding:utf-8
import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft
import pixoLibs.pixoShotgun as psg
import shutil
import subprocess


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
    imagedir = os.path.join(projectdir, 'images/focus')
    # os.makedirs(os.path.join(os.path.dirname(pubfile), 'images'))
    # pm.sysFile(imagedir, copy=os.path.join(os.path.dirname(pubfile), 'images'))
    shutil.copytree(imagedir, os.path.join(os.path.dirname(pubfile), 'images/focus'))
    # --------------------------------------------------------------------------------------------------------
    # 相机输出
    cams = map(lambda x: x.getParent(), filter(lambda x: x.name().startswith('cam_focus_'), pm.ls(type='camera')))
    pm.select(cams,r=True)
    camsFile = os.path.splitext(pubfile)[0] + '.ma'
    pm.exportSelected(camsFile, force=True)
    # --------------------------------------------------------------------------------------------------------
    # 生成缩略图
    mmfpeg = 'ffmpeg.exe'
    seqfile = os.path.normpath(os.path.join(os.path.dirname(pubfile), 'images/focus/focus.%04d.exr'))
    movfile = os.path.join(os.path.dirname(pubfile), '{}.mov'.format(os.path.basename(pubfile).split('.')[0]))
    beginframe, endframe = psg.get_cut_range(path_obj.project, '%s_%s' % (path_obj.seq, path_obj.shot))
    framenum = endframe - beginframe + 2
    # 这里有个bug在ffmpeg里
    convertcmd = '{} -apply_trc iec61966_2_1 -start_number 1001 -f image2 -r 24 -i {} -vcodec h264 -vframes {} -s 1024X429 {}'.format(mmfpeg,
                                                                                                              seqfile,
                                                                                                              framenum,
                                                                                                              movfile)

    p = subprocess.Popen(convertcmd, shell=True, cwd=os.path.dirname(__file__))
    p.wait()
    # -----------------------------------------------------------------------------------
    # 上传shotgun
    versionID = psg.addToShotgun(camsFile, '')
    if versionID:
        psg.uploadQuicktime(versionID, movfile)
    # --------------------------------------------------------------------------------------------------------
    # 输出制作文件
    animSourceFile = os.path.join(os.path.dirname(pubfile), os.path.basename(pm.sceneName()).replace("anim",'focus'))
    pm.saveAs(animSourceFile)

    # --------------------------------------------------------------------------------------------------------
    # 打开publish目录
    pm.warning(u'导出CamFocus相机完成,文件另存为完成,序列帧复制完成')
    os.startfile(os.path.dirname(pubfile))
