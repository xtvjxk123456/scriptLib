# coding:utf-8
import pymel.core as pm
import os
import previewShaderInAnim as ps
import pixoLibs.pixoFileTools as pft
import maya.cmds as mc

path_obj = pft.PathDetails.parse_path(pm.sceneName())
publishdir = os.path.dirname(path_obj.getPublishFullPath())
cfx = os.path.normpath(os.path.join(publishdir, 'CFX'))


def getChar():
    char = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Character':
            char.append(asset)
    return char


def exportCFX(chars, begin, end):
    for char in chars:
        possibleName = char + '*:' + char + '_CFX'
        trans = pm.ls(possibleName)
        if trans:
            for tran in trans:
                # begin = pm.playbackOptions(q=True, ast=True)
                # end = pm.playbackOptions(q=True, aet=True)
                cmd = '-frameRange {} {} -stripNamespaces -uvWrite -root {} -file {}'.format(begin, end,
                                                                                             tran.name(long=True),
                                                                                             os.path.normpath(
                                                                                                 os.path.join(cfx,
                                                                                                              '{}.abc'.format(
                                                                                                                  tran.name().split(
                                                                                                                      ':')[
                                                                                                                      0]
                                                                                                              ))))
            print cmd
            mc.sysFile(cfx, md=True)
            pm.AbcExport(j=cmd)


def run():
    if mc.window('customtimeCFX', q=True, ex=True):
        mc.deleteUI('customtimeCFX')

    customUI = mc.window('customtimeCFX', t='set CFX time range', mnb=True, mxb=True, rtf=True)
    mainlayout = mc.columnLayout('mainlayout', p=customUI)
    beginctrl = mc.intFieldGrp(l='Begin', v1=0, p=mainlayout)
    endctrl = mc.intFieldGrp(l='End', v1=1, p=mainlayout)
    # begin= cmds.intFieldGrp(beginctrl,q=True,v1=True)
    # end= cmds.intFieldGrp(endctrl,q=True,v1=True)
    mc.button(l='Export',
              c=lambda *argv: exportCFX(getChar(), int(mc.intFieldGrp(beginctrl, q=True, v1=True)),
                                        int(mc.intFieldGrp(endctrl, q=True, v1=True))),
              p=mainlayout)
    mc.showWindow(customUI)
