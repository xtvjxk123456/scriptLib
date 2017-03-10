# coding:utf-8
import pymel.core as pm
import Publish_Mdl_Check_FaceShader as pmcfs
import maya.OpenMaya as om


def getObj():
    meshs = pmcfs.getObjWithFaceShader()
    names = map(lambda x: x.name(), meshs)
    return names


def fixFaceShaderObject(shapename):
    shape = pm.PyNode(shapename)
    sgs = pm.listConnections(shape, t='shadingEngine')
    sgs = list(set(sgs))

    pm.delete(shape, ch=True)

    faces = [x for x in sgs[0].members() if shapename in x.name()]
    faceidlist = []
    for x in faces:
        shellid = om.MIntArray()
        x.__apicomponent__().getElements(shellid)
        faceidlist.extend(list(shellid))
    selectface = om.MIntArray()
    om.MScriptUtil.createIntArrayFromList(faceidlist, selectface)

    trans = om.MFloatVector()
    shape.__apimfn__().extractFaces(selectface, trans)
    shape.__apimfn__().updateSurface()

    try:
        shapes = pm.polySeparate(shape, ch=False)
    except RuntimeError:
        shapes = []

    if filter(pmcfs.checkShaderMulti, shapes):
        for x in filter(pmcfs.checkShaderMulti, shapes):
            fixFaceShaderObject(x)


def run():
    map(fixFaceShaderObject,getObj()[0:5])
    pm.warning('Fix faceshader(five objs at least) finished.')
