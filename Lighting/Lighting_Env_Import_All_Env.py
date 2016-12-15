# coding:utf-8
import os
import re

import pixoLibs.pixoFileTools as pft
from scenegraph.scene import Scene
from scenegraph import util
import aas_sg

import maya.cmds as mc
import pymel.core as pm

# workDir = r'e:\test'
sg = aas_sg.get_standalone_sg()

ProjectName = 'df'
ProjectDirPath = os.path.join('Z:\\Shotgun\\projects\\', ProjectName)
ProjectAssetPath = os.path.join(ProjectDirPath, r'_library\assets')


def find_folders_in_dir(dirpath):
    """

    :param dirpath: 目录路径,类型为os.path认可的路径
    :return: 目录内容,都是文件夹名字,类型为list
    """
    content = os.listdir(dirpath)
    for item in content:
        if not os.path.isdir(os.path.join(dirpath, item)):
            content.remove(item)
    return content


def find_files_in_dir(dirpath):
    """

    :param dirpath: 目录路径,类型为os.path认可的路径
    :return: 目录内容,都是文件名字,类型为list
    """
    content = os.listdir(dirpath)
    for item in content:
        if os.path.isdir(os.path.join(dirpath, item)):
            content.remove(item)
    return content


def check_files_in_type(filenames, type):
    """

    :param fileNames: 文件名列表,类型为list
    :param type: 文件后缀,格式< '.xxx' >, 类型为string
    :return: 文件名列表,类型为list
    """
    for filename in filenames:
        if os.path.splitext(filename)[1] != type:
            filenames.remove(filename)
    return filenames


def get_asset_type_by_name(assetName):
    """

    :param name: 资产名<请注意:资产名在搜索时是不区分大小写的,请使用正确的名字>
    :return: ID 和 资产类型
    """

    asset = sg.find('Asset', [['code', 'is', str(assetName)]], ['sg_asset_type'])
    if len(asset) > 1:
        raise Exception(u'这个资产%s在数据库里有多条记录,数据库可以有错' % assetName)

    if len(asset) == 1:
        return asset[0]['id'], asset[0]['sg_asset_type']
    if len(asset) == 0:
        raise Exception(u'这个资产%s没有在数据库里' % assetName)


def get_anim_dir_newest():
    """
    # 用来分析lgt场景文件的,不是用来分析资产文件的
    :return: 最新版本的anim publish文件目录,该目录下有缓存信息
    """

    detail = pft.PathDetails.parse_path(mc.file(q=True, sn=True))
    # AnimFileNameBase = ProjectName+'_'+detail.seq+'_'+detail.shot+'_anim'
    basePath = detail.seq + '\\' + detail.shot + r'\3d\anim\_publish'
    AnimSceneFileDir = os.path.join(ProjectDirPath, basePath)

    if not os.path.exists(AnimSceneFileDir):
        raise Exception(u'难道没有publish过%s_%sanim文件?' % (detail.seq, detail.shot))
    else:
        files = find_folders_in_dir(AnimSceneFileDir)
        if len(files) == 0:
            raise Exception(u'%s\npublish文件夹里没文件,请重新publish' % AnimSceneFileDir)
        files.sort()
        newestDir = os.path.join(AnimSceneFileDir, files[-1])
        return newestDir


def check_anim_publish():
    """
    检查anim的最新的publish目录有没有正常的数据
    :return: 返回所有的abc文件
    """
    animPublishDir = get_anim_dir_newest()
    publishFiles = find_files_in_dir(animPublishDir)
    publishFiles = check_files_in_type(publishFiles, '.abc')
    if len(publishFiles) == 0:
        raise Exception(u'%s\npublish目录没有缓存文件,请重新publsh' % animPublishDir)
    return publishFiles


def get_shader_publish_dir(assetName):
    """

    :param assetName: 资产名
    :return: shader的publish文件版本的目录
    """

    assetType = get_asset_type_by_name(assetName)[1]
    shaderPublish = os.path.join(ProjectAssetPath, assetType + '\\' + assetName + r'\shd\_publish')
    return shaderPublish


def get_shd_file_newest(assetName):
    """

    :param assetName: 资产名
    :return: 最新的publish的shader文件路径
    """
    shaderDir = get_shader_publish_dir(assetName)
    shaderVerions = find_folders_in_dir(shaderDir)

    if len(shaderVerions) == 0:
        raise Exception(u'这个资产%s没有发布任何的shader文件' % assetName)

    shaderVerions.sort()
    newestDir = os.path.join(shaderDir, shaderVerions[-1])
    newestDirFiles = find_files_in_dir(newestDir)
    newestFileBase = 'df_' + assetName + '_shd_' + shaderVerions[-1]

    for fileItem in newestDirFiles:
        if re.match(newestFileBase + '.*', fileItem):
            return os.path.join(newestDir, fileItem)


def run():
    working_path = str(pm.sceneName())
    path_obj = pft.PathDetails.parse_path(working_path)
    if path_obj.task != "lgt":
        pm.warning("current file is not a light file.")
        return
    # get the latest anim xml
    path_obj.task = "anim"
    path_obj.version = "000"
    path_obj.ext = "xml"
    work_xml_dir, work_xml_name = os.path.split(path_obj.getPublishFullPath())
    work_xml_dir = os.path.dirname(os.path.dirname(work_xml_dir))
    work_xml_path = os.path.join(work_xml_dir, work_xml_name)
    latest_lay_xml = aas_sg.get_file_last_version(work_xml_path)
    # get the environ items
    loaded_scene = Scene.load(latest_lay_xml)

    references = {}
    for asset_node in util.walk_scene(loaded_scene):
        if asset_node.base_asset.startswith("Character"):
            references[asset_node.name] = ['Character', asset_node.paths[0]]
        if asset_node.base_asset.startswith("Prop"):
            references[asset_node.name] = ['Prop', asset_node.paths[0]]
        if asset_node.base_asset.startswith("Environment"):
            references[asset_node.name] = ['Environment', asset_node.paths[0]]

    # publishfiles = check_anim_publish()

    for namespace, data in references.items():
        if data[0] == 'Environment':
            try:
                asset_name = re.match(r'([a-zA-Z]*)[\d]*', namespace).group(1)
            except Exception, e:
                mc.warning(u'发生位置错误:{}'.format(e))
                return False
            try:
                shd_path = get_shd_file_newest(asset_name)
            except Exception, e:
                mc.warning(u'获取shd路径发生错误:{}'.format(e))
                return False
            # import shd
            try:
                pm.createReference(shd_path, namespace=asset_name)
            except Exception, e:
                mc.warning(u'参考文件发生错误:{}'.format(e))
                return False
