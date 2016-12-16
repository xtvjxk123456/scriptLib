#coding:utf-8
import pixoLibs.pixoFileTools as pft
import maya.cmds as mc
import maya.mel as mel
import os
import Publish_Layout_Bake_CameraToWorld as plb

# change here
_cacheDir = r'Z:\Shotgun\projects\df\data\CamAbc'


def run():
    path_obj = pft.PathDetails.parse_path(mc.file(q=1, sn=1))
    startTime = int(mc.playbackOptions(ast=True, q=True))
    endTime = int(mc.playbackOptions(aet=True, q=True))
    cam_PublishFullPath_abc = _cacheDir + '\{}\{}'.format(path_obj.seq, path_obj.shot) + '\{}'.format(
        path_obj.task) + '\\' + 'cam_{}_{}.abc'.format(path_obj.seq, path_obj.shot)
    mc.sysFile(os.path.dirname(cam_PublishFullPath_abc), md=True)
    cam = plb.getCameraInShot()
    if len(cam) == 1:
        mel.eval(
            'AbcExport -j "-frameRange {} {} -stripNamespaces -worldSpace -root {} -file {}"'.format(str(startTime),
                                                                                                     str(endTime),
                                                                                                     mc.ls(
                                                                                                         mc.listRelatives(
                                                                                                             cam[0],
                                                                                                             p=True),
                                                                                                         l=True)[0],
                                                                                                     os.path.normpath(
                                                                                                         cam_PublishFullPath_abc).replace(
                                                                                                         '\\', '/')))
    else:
        mc.warning(u'请检查场景相机,有问题存在')
