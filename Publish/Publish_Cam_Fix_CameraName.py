# coding:utf-8
import Publish_Layout_Bake_CameraToWorld as plb
import maya.cmds as mc


def fix_cam_shape_name(shape):
    CameraTransform = mc.listRelatives(shape, p=True)[0]
    rightname = CameraTransform + 'Shape'
    mc.rename(shape, rightname)


def run():
    try:
        map(fix_cam_shape_name, plb.getCameraInShot())
    except RuntimeError:
        mc.warning(u'出现错误,请询问td')
