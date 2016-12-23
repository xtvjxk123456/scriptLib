# coding:utf-8


def run():
    import Publish_Cam_Fix_CameraName
    Publish_Cam_Fix_CameraName.run()

    import Publish_Layout_Lock_Camrea
    Publish_Layout_Lock_Camrea.run()

    import Publish_Cam_Delete_UselessNodeOnCamera
    Publish_Cam_Delete_UselessNodeOnCamera.run()

    import pixoMaya.shelf.publish_cam as cam_publish
    cam_publish.run()
