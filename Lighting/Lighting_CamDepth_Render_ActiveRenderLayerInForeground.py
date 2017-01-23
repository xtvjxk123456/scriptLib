# coding:utf-8
import pymel.core as pm


def run():
    defaultRenderGlobal = pm.PyNode('defaultRenderGlobals')
    begin = defaultRenderGlobal.startFrame.get()
    end =defaultRenderGlobal.endFrame.get()
    seqcmds = '{}..{}'.format(begin,end+1)
    pm.arnoldRender(b=True,seq=seqcmds)
    pm.warning('BatchRender activeRenderLayer complete!')