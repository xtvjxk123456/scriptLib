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
                            'sg_resolution', 'code', 'tasks','description'])
    return shotInfo


def getAssetInfor(asset):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    assetInfo = sg.find_one("Asset", [
        ['code', 'is', asset],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                            ['sg_asset_type', 'sg_asset_name__cn', 'code', 'tasks','shots'])
    return assetInfo


def getTaskInfor(taskName):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    taskInfor = sg.find_one("Task", [
        ['content', 'is', taskName],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                            ['sg_task_type', 'code', 'task_assignees'])

    return taskInfor


def information(shot_name):
    assets = getShotInfo(shot_name)['assets']
    tasks = getShotInfo(shot_name)['tasks']
    print '#' * 60
    print '-------------shot %s----------------' % shot_name
    print 'FrameRange is {}-{}'.format(getShotInfo(shot_name)['sg_cut_in'], getShotInfo(shot_name)['sg_cut_out'])
    print 'Shotgun Asset num is ', len(assets)
    print 'Asset Content:'
    for x in assets:
        CNInfo = getAssetInfor(x['name'])['sg_asset_name__cn']
        if CNInfo:
            cnName = CNInfo.decode('utf-8')
        else:
            cnName = None

        print '-- [', x['name'], '] NameCn :', cnName, '] AssetType : <', getAssetInfor(x['name'])[
            'sg_asset_type'], '>'
        assetTaskInfor = getAssetInfor(x['name'])['tasks']
        if assetTaskInfor:
            for assettask in assetTaskInfor:
                if assettask['name'].endswith('_mdl') or assettask['name'].endswith('_rig') or assettask['name'].endswith('_shd'):
                    assetTaskAssignto = getTaskInfor(assettask['name'])['task_assignees']
                    if assetTaskAssignto:
                        assetTaskUser = assetTaskAssignto[0]['name'].decode('utf-8')
                    else:
                        assetTaskUser = None
                    print '-' * 20, '<{}>:'.format(assettask['name']), assetTaskUser


    print 'Task Information:'
    for x in tasks:
        assignto = getTaskInfor(x['name'])['task_assignees']
        if assignto:
            user_name = assignto[0]['name'].decode('utf-8')
        else:
            user_name = None

        print '-- [', x['name'], ']  AssignTo : <', user_name, '>'
    print '#' * 60
    mc.ScriptEditor()


def run():
    current_shot = mc.file(q=True, sn=True).split('_')
    shot_name = '_'.join(current_shot[1:3])
    information(shot_name)
