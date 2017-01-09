# coding:utf-8
import os
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
# import maya.mel as mel
import maya.cmds as mc



def lockObjectTransform(shapename):
    name = pm.PyNode(shapename).getParent()
    name.attr('tx').lock()
    name.attr('ty').lock()
    name.attr('tz').lock()
    name.attr('rx').lock()
    name.attr('ry').lock()
    name.attr('rz').lock()
    name.attr('sx').lock()
    name.attr('sy').lock()
    name.attr('sz').lock()


def UnlockObjectTransform(shapename):
    name = pm.PyNode(shapename).getParent()
    name.attr('tx').unlock()
    name.attr('ty').unlock()
    name.attr('tz').unlock()
    name.attr('rx').unlock()
    name.attr('ry').unlock()
    name.attr('rz').unlock()
    name.attr('sx').unlock()
    name.attr('sy').unlock()
    name.attr('sz').unlock()


def DeleteKeyFrameInTransfrom(transform):
    mc.cutKey(transform, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])


def getCameraInShot():
    transforms = map(lambda x: mc.listRelatives(x, p=True, pa=True)[0], mc.ls(type='camera'))
    cameraList = zip(transforms, mc.ls(type='camera'))
    f = pm.sceneName()
    # path_obj = pft.PathDetails.parse_path(f)
    basefilename = os.path.basename(f).split('_')
    seq = basefilename[1]
    shot = basefilename[2]
    cameraName = 'cam_' + seq + '_' + shot
    allPossible = []
    for x in cameraList:
        if x[0].split('|')[-1] == cameraName:
            allPossible.append(x[1])
    if not allPossible:
        mc.warning(u'找不到想要的相机,请检查先相机的命名')
    return allPossible


def makeCameraToWorld(cameraShape):
    if not cameraShape:
        return
    CameraTransform = mc.listRelatives(cameraShape, p=True)[0]
    TempLocator = mc.spaceLocator(p=[0, 0, 0], name='tempLocator')[0]
    # constrain tempLocator and bake
    ##############mc.select([CameraTransform,TempLocator],r=True)
    parentNode = mc.parentConstraint(CameraTransform, TempLocator, mo=False, w=1)
    scaleNode = mc.scaleConstraint(CameraTransform, TempLocator, mo=False, w=1)
    begin = mc.playbackOptions(q=True, ast=True)
    end = mc.playbackOptions(q=True, aet=True)
    mc.bakeResults(TempLocator, t=(begin, end), sm=True, sb=1, dic=True, pok=True, sac=False, ral=False, bol=False,
                   mr=True, cp=False, s=True)
    mc.delete(tuple([parentNode[0], scaleNode[0]]))
    # unlock camera first
    UnlockObjectTransform(cameraShape)

    # delete anim curve in transform
    DeleteKeyFrameInTransfrom(CameraTransform)

    # unparent camera
    try:
        CameraTransform = mc.parent(CameraTransform, w=True)[0]
    except Exception:
        pass
    # transfer back to camrea
    ############mc.select([TempLocator,CameraTransform],r=True)
    mc.parentConstraint(TempLocator, CameraTransform, mo=False, w=1)
    try:
        mc.scaleConstraint(TempLocator, CameraTransform, mo=False, w=1)
    except Exception:
        pass
    mc.bakeResults(CameraTransform, t=(begin, end), sm=True, sb=1, dic=True, pok=True, sac=False, ral=False, bol=False,
                   mr=True, cp=False, s=True)
    mc.delete(TempLocator)


def run():
    map(makeCameraToWorld, getCameraInShot())
