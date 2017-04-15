# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import os
import maya.cmds as cmds
import maya.mel


def export_anim_publish(data, begin, end):
    filepath = pm.sceneName()
    dets = pft.PathDetails.parse_path(filepath)
    dets.ext = 'abc'
    pubfile = dets.getPublishFullPath()
    pubpath = os.path.dirname(pubfile)
    pft.createMissingDirectories(pubpath)

    for ref in data():
        dets.name = ref.split(':')[0]
        pubfile = dets.getPublishFullPath()
        mdl_name = '%s_%s' % (ref.split('_')[0], 'mdl')
        export_obj = pm.ls(mdl_name)[0].longName()

        # startTime = int(cmds.playbackOptions(animationStartTime=True, query=True))
        # startTime = 950
        # endTime = int(cmds.playbackOptions(animationEndTime=True, query=True))
        # current = int(cmds.currentTime(q=True))
        cmds.refresh(suspend=True)
        command = 'AbcExport - j "-frameRange %s %s -attrPrefix ai -uvWrite -writeVisibility -dataFormat hdf -root %s ' \
                  '-file %s"' % (begin, end, export_obj, pubfile)
        maya.mel.eval(command)
        cmds.refresh(suspend=False)


def exportCustomTime(begin, end):
    try:
        items = pm.listRelatives('Anim')
    except Exception:
        pm.error(u'没有Anim组,需要组织下动画文件')

    for item in items:
        # if item in pm.ls('PsychoOne*:PsychoOne_rig'):
        #     for x in pm.ls('PsychoOne*:WeiBo_cn'):
        #         x.simulation.set(0)
        #     pm.currentTime(950)
        #     for x in pm.ls('PsychoOne*:WeiBo_cn'):
        #         x.simulation.set(1)

        export_anim_publish(lambda: [item.name()],begin,end)
    pm.warning('Export Complete!')


def run():
    if cmds.window('customtime', q=True, ex=True):
        cmds.deleteUI('customtime')

    customUI = cmds.window('customtime', t='set time range', mnb=True, mxb=True, rtf=True)
    mainlayout = cmds.columnLayout('mainlayout', p=customUI)
    beginctrl = cmds.intFieldGrp(l='Begin', v1=0, p=mainlayout)
    endctrl = cmds.intFieldGrp(l='End', v1=1, p=mainlayout)
    # begin= cmds.intFieldGrp(beginctrl,q=True,v1=True)
    # end= cmds.intFieldGrp(endctrl,q=True,v1=True)
    exportbutton = cmds.button(l='Export', c=lambda *argv: exportCustomTime(int(cmds.intFieldGrp(beginctrl,q=True,v1=True)),
                                                                            int(cmds.intFieldGrp(endctrl,q=True,v1=True))), p=mainlayout)
    cmds.showWindow(customUI)
