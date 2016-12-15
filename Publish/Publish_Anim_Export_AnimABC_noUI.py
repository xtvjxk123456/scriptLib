# coding:utf-8
import pixoMaya.base as base
import pymel.core as pm


def run():
    try:
        items =pm.listRelatives('Anim')
    except Exception:
        pm.error(u'没有Anim组,需要组织下动画文件')

    for item in items:
        if item in pm.ls('PsychoOne*:PsychoOne_rig'):
            for x in pm.ls('PsychoOne*:WeiBo_cn'):
                x.simulation.set(0)
            pm.currentTime(950)
            for x in pm.ls('PsychoOne*:WeiBo_cn'):
                x.simulation.set(1)

        base.export_anim_publish(lambda: [item.name()])
    pm.warning('Export Complete!')
