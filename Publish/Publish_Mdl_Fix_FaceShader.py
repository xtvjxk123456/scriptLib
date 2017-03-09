# coding:utf-8
import pymel.core as pm
import pixoLibs.magiclist.maya_magic_list as magic_list
import Publish_Mdl_Check_FaceShader as pmcfs
import maya.OpenMaya as om


def getObj():
    meshs = pmcfs.getObjWithFaceShader()
    names = map(lambda x: x.name(), meshs)
    return names


def fixFaceShaderObject(items):
    for item in items():
        itemnode = pm.PyNode(item)
        sgs = pm.listConnections(itemnode, t='shadingEngine')
        sgs = list(set(sgs))
        # sgs代表有多个shadingGroup
        # pm.select(shape,r=True)
        # ------------------------------------------------------------------------------
        # hilite是醒目的意思,比较适合选择用来建模(这种选择可以方便的进入组件(点线面))
        # pm.hilite(item, r=True)
        # pm.selectMode(component=True)
        # ------------------------------------------------------------------------------
        # 先删除历史
        pm.delete(itemnode, ch=True)

        # ------------------------------------------------------------------------------
        # 这里以前有个bug,这个bug只是考虑到用材质球选择面,而不是考虑到用材质球选择当前物体的面
        # pm.select([x for x in sgs[0].members() if item in x.name()], r=True)
        # ------------------------------------------------------------------------------
        faces = [x for x in sgs[0].members() if item in x.name()]
        faceidlist = []
        for x in faces:
            shellid = om.MIntArray()
            x.__apicomponent__().getElements(shellid)
            faceidlist.extend(list(shellid))
        selectface = om.MIntArray()
        om.MScriptUtil.createIntArrayFromList(faceidlist, selectface)

        # ------------split face------------------------------

        # trans = om.MFloatVector()
        # meshfn = om.MFnMesh(selectobj)
        # result = meshfn.extractFaces(faceid, trans)
        # print result
        # meshfn.updateSurface()
        trans = om.MFloatVector()
        itemnode.__apimfn__().extractFaces(selectface, trans)
        itemnode.__apimfn__().updateSurface()

        # -------------------------------------------------
        # ------------------seprate mesh--------------------
        # pm.runtime.ExtractFace()
        # pm.runtime.DeleteHistory()
        # shapes = pm.listRelatives(pm.ls(sl=True))

        try:
            shapes = pm.polySeparate(itemnode, ch=False)
        except RuntimeError:
            shapes = [itemnode]

        if filter(pmcfs.checkShaderMulti, shapes):
            for x in filter(pmcfs.checkShaderMulti, shapes):
                fixFaceShaderObject(x)


def run():
    magic_list.run(getObj, 'FaceShader Fix', {'Fix': fixFaceShaderObject})
