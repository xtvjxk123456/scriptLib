import maya.cmds as mc
# import pymel.core as pm
import os
import pixoLibs.pixoFileTools as pft
import pixoMaya.shelf.publish_cam as cam_publish
from ui_elements.screenshot import screen_capture_file
import pixoMaya.shelf.animation.anim_organize as organize
import pixoMaya.td_tools as td_tools


def publish_xml():
    dets = pft.PathDetails.parse_path(pm.sceneName())
    dets.name = 'layout'
    xmlfile = dets.getFullPath()
    xmlpub = dets.getPublishFullPath(ext='xml')
    pft.copyFile(xmlfile, xmlpub, force=True)


def update_xml():
    # wipe current xmls on working folder
    dets = pft.PathDetails.parse_path(pm.sceneName())
    dets.ext = 'xml'
    if os.path.exists(dets.getFullPath()):
        os.remove(dets.getFullPath())

    # write out xml to working folder
    refs = pm.ls(references=True)
    for ref in refs:
        td_tools.save_ref_to_xml(ref)


def anim_publish(filepath):
    dets = pft.PathDetails.parse_path(filepath)
    pubfile = dets.getPublishFullPath()
    pubpath = os.path.dirname(pubfile)
    pft.createMissingDirectories(pubpath)
    pft.copyFile(filepath, pubfile, force=True)

    # import pixoLibs.magiclist.maya_magic_list as magic_list
    # magic_list.run(get_anim_geo, 'Publish Animation',
    #                {'Export Alembic': export_anim_publish, 'Go to File': filebrowse_to_anim})

    # you need save maya file by youself because may be some error in maya file


# Auto publish by one clicked

def NoUI_publish():
    filepath = mc.file(q=True, sn=True)
    # make thumb
    screen_capture_file(pft.getPreviewPath(filepath))

    # remove shareReferenc
    import deleteInvaildReferenceNode
    deleteInvaildReferenceNode.run()

    # playblast
    # playblast is hard to write here ,so playblast first

    # publishcamera
    cam_publish.run()

    # update referece
    # you can do it before this script

    publish_xml()

    update_xml()

    organize.run()

    anim_publish(filepath)
    # we can not publish abc cache
    # you can export cache youself
    mc.warning('no UI anim publish complete!<no playblast,no update referece,no anim cache export>')

def run():
    NoUI_publish()