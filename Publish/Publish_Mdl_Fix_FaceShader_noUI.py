# coding:utf-8
import maya.cmds as mc
import Publish_Mdl_Check_FaceShader as pmcfs
import maya.OpenMaya as om


def fixFaceShaderObject(shapename):
    # 确保这个shape不是一个instanced对象

    templist = om.MSelectionList()
    om.MGlobal.getSelectionListByName(shapename, templist)
    shapedagpath = om.MDagPath()
    templist.getDagPath(0, shapedagpath)
    fnmesh = om.MFnMesh(shapedagpath)

    sgs = om.MObjectArray()
    faceinsg = om.MObjectArray()
    fnmesh.getConnectedSetsAndMembers(0, sgs, faceinsg, True)

    fn_firstsg = om.MFnDependencyNode(sgs[0])
    firstsgname = fn_firstsg.name()

    fn_compent = om.MFnSingleIndexedComponent(faceinsg[0])
    m_faceid = om.MIntArray()
    fn_compent.getElements(m_faceid)

    tempTrans = om.MFloatVector()
    fnmesh.extractFaces(m_faceid, tempTrans)
    fnmesh.updateSurface()
    try:
        shapes = mc.polySeparate(fnmesh.fullPathName(), ch=False)
    except RuntimeError:
        shapes = []

    if filter(pmcfs.checkShaderMulti, shapes):
        for objname in filter(pmcfs.checkShaderMulti, shapes):
            fixFaceShaderObject(objname)


def run():
    meshs, _ = pmcfs.getObjWithFaceShader()

    map(fixFaceShaderObject, meshs[0:5])
    mc.warning('Fix faceshader(five objs at least) finished.')
