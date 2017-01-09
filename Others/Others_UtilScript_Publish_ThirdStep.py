# coding:utf-8
import maya.OpenMaya as om


def run():
    import Publish_Anim_AutoAnimPublish
    Publish_Anim_AutoAnimPublish.run()

    om.MFileIO.save()

    import Publish_Anim_Copy_AnimSourceToPublish
    Publish_Anim_Copy_AnimSourceToPublish.run()
