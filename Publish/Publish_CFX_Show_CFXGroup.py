# coding:utf-8
import pymel.core as pm
import previewShaderInAnim as ps
import os


def getChar():
    char = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Character':
            char.append(asset)
    return char


def config_cfx_group(status):
    """

    :param status: 1:show ,0:hide
    :return:
    """
    chars = getChar()
    for char in chars:
        possibleCFX = char + '*:' + char + '_CFX'
        trans = pm.ls(possibleCFX)
        if trans:
            for tran in trans:
                Attr = pm.PyNode(tran).attr('visibility')
                Attr.set(status)


def run():
    config_cfx_group(1)
