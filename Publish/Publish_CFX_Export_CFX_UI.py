# coding:utf-8
import pymel.core as pm
import previewShaderInAnim as ps
import os
import pixoLibs.pixoFileTools as pft
import pixoLibs.magiclist.maya_magic_list as magic_list

path_obj = pft.PathDetails.parse_path(pm.sceneName())
publishdir = os.path.dirname(path_obj.getPublishFullPath())
cfx = os.path.normpath(os.path.join(publishdir, 'CFX'))


def getChar():
    char = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Character':
            char.append(asset)
    ui_Items = []
    for c in char:
        possibleName = c + '*:' + c + '_CFX'
        trans = pm.ls(possibleName)
        trannames = map(lambda t: t.name(), trans)
        ui_Items.extend(trannames)
    return ui_Items


def exportCFX(items):
    for tran in items():
        # begin = pm.playbackOptions(q=True, ast=True)
        end = pm.playbackOptions(q=True, aet=True)
        cmd = '-frameRange {} {} -stripNamespaces -uvWrite -root {} -file {}'.format(950, end,
                                                                                     pm.PyNode(tran).name(long=True),
                                                                                     os.path.normpath(
                                                                                         os.path.join(cfx,
                                                                                                      '{}.abc'.format(
                                                                                                          tran.split(
                                                                                                              ':')[
                                                                                                              0]
                                                                                                      ))))
    print cmd
    pm.sysFile(cfx, md=True)
    pm.AbcExport(j=cmd)


def openDir(item):
    os.startfile(cfx)


def run():
    magic_list.run(getChar, 'CFX Publish', {'Export': exportCFX, 'Go to File': openDir})
