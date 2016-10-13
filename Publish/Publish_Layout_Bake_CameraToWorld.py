# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
# import maya.mel as mel
import maya.cmds as mc


def lockObjectTransform(shapename):
    name = pm.PyNode(shapename).getParent()
    pm.PyNode(name).attr('tx').lock()
    pm.PyNode(name).attr('ty').lock()
    pm.PyNode(name).attr('tz').lock()
    pm.PyNode(name).attr('rx').lock()
    pm.PyNode(name).attr('ry').lock()
    pm.PyNode(name).attr('rz').lock()
    pm.PyNode(name).attr('sx').lock()
    pm.PyNode(name).attr('sy').lock()
    pm.PyNode(name).attr('sz').lock()


def UnlockObjectTransform(shapename):
    name = pm.PyNode(shapename).getParent()
    pm.PyNode(name).attr('tx').unlock()
    pm.PyNode(name).attr('ty').unlock()
    pm.PyNode(name).attr('tz').unlock()
    pm.PyNode(name).attr('rx').unlock()
    pm.PyNode(name).attr('ry').unlock()
    pm.PyNode(name).attr('rz').unlock()
    pm.PyNode(name).attr('sx').unlock()
    pm.PyNode(name).attr('sy').unlock()
    pm.PyNode(name).attr('sz').unlock()


def DeleteKeyFrameInTransfrom(transform):
    mc.cutKey(transform, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])


def getCameraInShot():
    transforms = map(lambda x: mc.listRelatives(x, p=True, pa=True)[0], mc.ls(type='camera'))
    cameraList = zip(transforms, mc.ls(type='camera'))
    f = mc.file(q=True, sn=True)
    path_obj = pft.PathDetails.parse_path(f)
    cameraName = 'cam_' + path_obj.seq + '_' + path_obj.shot
    allPossible = []
    for x in cameraList:
        if x[0].split('|')[-1] == cameraName:
            allPossible.append(x[1])
    return allPossible


def makeCameraToWorld(cameraShape):
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
