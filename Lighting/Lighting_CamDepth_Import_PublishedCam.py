# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import os
import previewShaderInAnim as ps
import glob

def get_latest_camera():
    try:
        path_obj = pft.PathDetails.parse_path(pm.sceneName())
    except Exception:
        pm.warning(u'场景文件名不正确')
        return None
    path_obj.task = 'cam'
    publishdir = os.path.dirname(os.path.dirname(path_obj.getPublishFullPath()))
    versions = ps.find_folders_in_dir(publishdir)
    if not versions:
        pm.warning(u'cam没有publish过任何文件')
        return None
    versions.sort()
    rightPath = os.path.join(publishdir, '{}/df_{}_{}_{}_{}_???.m?'.format(versions[-1], path_obj.seq, path_obj.shot, 'cam',versions[-1]))
    file_path = glob.glob(os.path.normpath(rightPath))
    if file_path:
        return file_path[0]
    else:
        pm.warning(u'cam文件没有publish完成?')
        return None


def run():
    camfile = get_latest_camera()
    if camfile:
        fileref = pm.createReference(camfile,namespace='CamFocus')
        nodes = fileref.nodes()
        cam = filter(lambda x: x.name().startswith('CamFocus:cam_') and x.type()=='transform',nodes)
        # print cam
        fileref.importContents(removeNamespace =True)
        pm.rename(cam[0],cam[0].name().replace('cam_','cam_focus_'))
    else:
        pm.warning(u'请检查场景文件名或者cam publish目录....')
