# coding:utf-8
import pymel.core as pm
import previewShaderInAnim as ps
import os
import pixoLibs.pixoFileTools as pft
import maya.cmds as mc

path_obj = pft.PathDetails.parse_path(pm.sceneName())
publishdir = os.path.dirname(path_obj.getPublishFullPath())
cfx = os.path.normpath(os.path.join(publishdir, 'CFX'))


def getChar():
    char = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Character':
            char.append(asset)
    return char


def exportCFX():
    chars = getChar()
    for char in chars:
        possibleName = char + '*:' + char + '_CFX'
        trans = pm.ls(possibleName)
        if trans:
            for tran in trans:
                # begin = pm.playbackOptions(q=True, ast=True)
                end = pm.playbackOptions(q=True, aet=True)
                cmd = '-frameRange {} {} -stripNamespaces -uvWrite -root {} -file {}'.format(950, end,
                                                                                             tran.name(long=True),
                                                                                             os.path.normpath(
                                                                                                 os.path.join(cfx,
                                                                                                              '{}.abc'.format(
                                                                                                                  tran.name().split(
                                                                                                                      ':')[
                                                                                                                      0]
                                                                                                              ))))
            print cmd
            mc.sysFile(cfx, md=True)
            pm.AbcExport(j=cmd)


def configCloth(status):
    """

    :param status: 0:hide cloth,1:show cloth
    :return: None
    """
    print "-" * 40
    chars = getChar()
    needCFX = []
    for char in chars:
        possibleCFX = char + '*:' + char + '_CFX'
        trans = pm.ls(possibleCFX)
        if trans:
            # print u"---{} 需要布料解算".format(char)
            needCFX.append(char)

    for char in needCFX:
        possibleLocator = char + '*:' + char + '_loc'
        trans = pm.ls(possibleLocator)
        if trans:

            for tran in trans:
                try:
                    Attr = pm.PyNode(tran).attr('wrap_cloth')
                except pm.MayaAttributeError, e:
                    pm.warning(u'绑定设置不合理,缺少相应属性设置:{}'.format(e))
                    continue

                Attr.set(status)
        else:
            pm.warning(u'绑定设置不合理,缺少节点设置:{}'.format(possibleLocator))
    print "-" * 40


def run():
    exportCFX()
    pm.warning('Export CFX done...')
