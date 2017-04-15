# coding:utf-8
import maya.cmds as mc


def run():
    oldcurrent = mc.currentTime(q=True)
    import Others_UtilTempScript_Export_AnimABC_noUI_CurrentFrame
    Others_UtilTempScript_Export_AnimABC_noUI_CurrentFrame.run()

    import pixoMaya.shelf.playblast as pb
    pb.run()

    # ------------------------------------------
    import Publish_Cam_CamPublish
    Publish_Cam_CamPublish.run()
    # ------------------------------------------
    mc.currentTime(oldcurrent)
