# coding:utf-8
import pymel.core as pm


def checkShaderMulti(shape):
    sgs = pm.listConnections(shape, t='shadingEngine')
    sgs = list(set(sgs))
    if len(sgs) > 1:
        # print shape, 'has multi shader'
        return True
    if len(sgs) == 1:
        # print shape, 'has single shader'
        return False
    if len(sgs) == 0:
        # print shape, 'has no shader '
        return False


def getObjWithFaceShader():
    allmesh = pm.ls(type='mesh')

    multis = filter(checkShaderMulti, allmesh)
    return multis


def run():
    meshs = getObjWithFaceShader()
    trans = map(lambda x: x.getParent(), meshs)
    objname = '\n'.join(map(lambda x:x.name(),trans))
    message = 'Result:\n\n' +objname
    pm.confirmDialog(t='FaceShader Result',m = message,b='I got it!',icon ='warning')
