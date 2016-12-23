# coding:utf-8


def run():
    import pixoMaya.shelf.playblast as pb
    pb.run()
    # ------------------------------------------
    import Publish_Cam_Fix_CameraName
    Publish_Cam_Fix_CameraName.run()

    import Publish_Layout_Lock_Camrea
    Publish_Layout_Lock_Camrea.run()

    import Publish_Cam_Delete_UselessNodeOnCamera
    Publish_Cam_Delete_UselessNodeOnCamera.run()

    import Publish_Cam_CamPublish
    Publish_Cam_CamPublish.run()
    # ------------------------------------------

    import Publish_Anim_Export_AnimABC_noUI
    Publish_Anim_Export_AnimABC_noUI.run()
