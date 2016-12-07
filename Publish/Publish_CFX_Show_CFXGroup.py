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
    print '_'*40
    chars = getChar()
    needCFX = []
    noNeedCFX = []
    for char in chars:
        possibleCFX = char + '*:' + char + '_CFX'
        trans = pm.ls(possibleCFX)
        if trans:
            # print u"---{} 需要布料解算".format(char)
            needCFX.append(char)
            for tran in trans:
                Attr = pm.PyNode(tran).attr('visibility')
                Attr.set(status)
        else:
            # print u"---{} 不需要布料解算".format(char)
            noNeedCFX.append(char)
    print u"需要布料解算的角色有:"
    for x in needCFX:
        print '----',x
    print u"不需要布料解算的角色有:"
    for n in noNeedCFX:
        print '----', n
    print '_' * 40


def run():
    config_cfx_group(1)
