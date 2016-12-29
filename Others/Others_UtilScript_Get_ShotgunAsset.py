# coding:utf-8
import maya.cmds as mc
import aas_sg

sg = aas_sg.get_standalone_sg()


def getShotInfo(shot):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    shotInfo = sg.find_one("Shot", [
        ['code', 'is', shot],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                           ['assets', 'sg_asset_type', 'sg_head_in', 'sg_tail_out', 'sg_cut_in', 'sg_cut_out',
                            'sg_resolution', 'code','tasks'])
    return shotInfo


def getAssetType(asset):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    assetInfo = sg.find_one("Asset", [
        ['code', 'is', asset],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                            ['sg_asset_type', 'code'])
    return assetInfo


def run():

    current_shot = mc.file(q=True, sn=True).split('_')
    shot_name = '_'.join(current_shot[1:3])

    assets = getShotInfo(shot_name)['assets']
    print '#' * 60
    print '-------------shot %s----------------' % shot_name
    print 'FrameRange is {}-{}'.format(getShotInfo(shot_name)['sg_cut_in'], getShotInfo(shot_name)['sg_cut_out'])
    print 'shotgun asset num is ', len(assets)
    print 'asset content:'
    for x in assets:
        print '-- [', x['name'], ']  AssetType : <', getAssetType(x['name'])['sg_asset_type'], '>'
    print '#' * 60




