# coding:utf-8
import maya.cmds as mc
import maya.OpenMaya as om


def checkShaderMulti(shapename):
    if not shapename:
        templist = om.MSelectionList()
        om.MGlobal.getSelectionListByName(shapename, templist)
        shapedagpath = om.MDagPath()
        templist.getDagPath(0, shapedagpath)
        fnmesh = om.MFnMesh(shapedagpath)
        sgs = om.MObjectArray()
        faceinsg = om.MObjectArray()
        # 确保这个shape不是一个instanced对象
        fnmesh.getConnectedSetsAndMembers(0, sgs, faceinsg, True)
        if sgs.length() <= 1:
            return False
        else:
            return True
    else:
        return None


def getObjWithFaceShader():
    iter_mesh = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    objs = []
    instanced = []
    while not iter_mesh.isDone():
        m_mesh = iter_mesh.currentItem()
        fn_mesh = om.MFnMesh(m_mesh)
        sgs = om.MObjectArray()
        faceinsg = om.MObjectArray()
        if not iter_mesh.isInstanced(False):
            fn_mesh.getConnectedSetsAndMembers(0, sgs, faceinsg, True)
            if sgs.length() > 1:
                objs.append(fn_mesh.fullPathName())
        else:
            instanced.append(fn_mesh.fullPathName())
            iter_mesh.next()
        iter_mesh.next()
    return objs, instanced


def run():
    meshs = getObjWithFaceShader()[0]
    trans = map(lambda x: mc.listRelatives(x,p=True)[0], meshs)
    objname = '\n'.join(trans)
    message = 'Result:\n\n' +objname
    mc.confirmDialog(t='FaceShader Result',m = message,b='I got it!',icon ='warning')
