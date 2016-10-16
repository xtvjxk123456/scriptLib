# coding:utf-8
import pixoMaya.base as base
import maya.cmds as mc


def getobject():
    try:
        objects = mc.listRelatives('Anim')
    except Exception:
        mc.error(u'没有Anim这个组，你需要整理')
    else:
        return objects


def run():
    base.export_anim_publish(getobject)
    mc.warning('Export Complete!')