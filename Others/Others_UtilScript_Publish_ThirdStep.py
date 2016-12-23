# coding:utf-8


def run():
    import Publish_Anim_AutoAnimPublish
    Publish_Anim_AutoAnimPublish.run()

    import pymel.core as pm
    pm.saveFile()

    import Publish_Anim_Copy_AnimSourceToPublish
    Publish_Anim_Copy_AnimSourceToPublish.run()
