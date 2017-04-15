# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import os
import maya.cmds as cmds
import maya.mel


def export_anim_publish(data):
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
        current = int(cmds.currentTime(q=True))
        cmds.refresh(suspend=True)
        command = 'AbcExport - j "-frameRange %s %s -attrPrefix ai -uvWrite -writeVisibility -dataFormat hdf -root %s ' \
                  '-file %s"' % (current, current, export_obj, pubfile)
        maya.mel.eval(command)
        cmds.refresh(suspend=False)
        # confirmPrompt('Export Alembic', 'AbcExport successful! \n file write: %s' % pubfile)
        # TODO Add to shotgun, submit Abc to deadline
        # publishSG([filepath])
        # exportAlembic(filepath, abcfile, models, 'anim')


def run():
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

        export_anim_publish(lambda: [item.name()])
    pm.warning('Export Complete!')
