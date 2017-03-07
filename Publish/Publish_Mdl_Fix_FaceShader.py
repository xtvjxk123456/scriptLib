# coding:utf-8
import pymel.core as pm
import pixoLibs.magiclist.maya_magic_list as magic_list
import Publish_Mdl_Check_FaceShader as pmcfs


def getObj():
    meshs = pmcfs.getObjWithFaceShader()
    names = map(lambda x: x.name(), meshs)
    return names


def fixFaceShaderObject(items):
    for item in items():
        sgs = pm.listConnections(pm.PyNode(item), t='shadingEngine')
        sgs = list(set(sgs))
        # sgs代表有多个shadingGroup
        # pm.select(shape,r=True)
        # hilite是醒目的意思,比较适合选择用来建模(这种选择可以方便的进入组件(点线面))
        pm.hilite(item, r=True)
        pm.selectMode(component=True)
        # 这里以前有个bug,这个bug只是考虑到用材质球选择面,而不是考虑到用材质球选择当前物体的面
        pm.select([x for x in sgs[0].members() if item in x.name()], r=True)
        pm.runtime.ExtractFace()
        pm.runtime.DeleteHistory()
        shapes = pm.listRelatives(pm.ls(sl=True))
        if filter(pmcfs.checkShaderMulti, shapes):
            for x in filter(pmcfs.checkShaderMulti, shapes):
                fixFaceShaderObject(x)


def run():
    magic_list.run(getObj, 'FaceShader Fix', {'Fix': fixFaceShaderObject})
