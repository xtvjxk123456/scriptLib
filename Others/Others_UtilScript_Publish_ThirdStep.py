# coding:utf-8


def run():
    import Publish_Anim_AutoAnimPublish
    Publish_Anim_AutoAnimPublish.run()

    import maya.OpenMaya as om
    om.MFileIO.save()

    import Publish_Anim_Copy_AnimSourceToPublish
    Publish_Anim_Copy_AnimSourceToPublish.run()
