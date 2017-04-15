# coding:utf-8


def run():
    import Publish_Anim_Export_AnimABC_noUI
    Publish_Anim_Export_AnimABC_noUI.run()

    import pixoMaya.shelf.playblast as pb
    pb.run()
    # ------------------------------------------
    import Publish_Cam_CamPublish
    Publish_Cam_CamPublish.run()
    # ------------------------------------------

