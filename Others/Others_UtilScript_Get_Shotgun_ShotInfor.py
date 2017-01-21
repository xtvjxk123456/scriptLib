# coding:utf-8
import maya.cmds as mc
import aas_sg

sg = aas_sg.get_standalone_sg()

Status_cn = {
    'wtg': u'准备开始',
    'fin': u'最终通过',
    'ip': u'正在进行',
    'omt': u'暂停(以后可能继续)',
    'hld': u'暂停(以后不可能继续)',
    'rdy': u'可以开始',
    'apr': 'Approved',
    'mdfy': 'Need Modify',
    'cmpt': u'完成',
    'recd': u'收到的',
    'upluip': u'上传中的',
    'cbb': u'能更好些(吧?)',

}

Asset_type_cn = {
    'Prop': u'道具',
    'Character': u'角色',
    'Environment': u'场景',
    'Vehicle': u'装置',
    'Matte Painting': u'绘图'
}


def getShotInfo(shot):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    shotInfo = sg.find_one("Shot", [
        ['code', 'is', shot],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                           ['assets', 'sg_asset_type', 'sg_head_in', 'sg_tail_out', 'sg_cut_in', 'sg_cut_out',
                            'sg_resolution', 'code', 'tasks', 'description'])
    return shotInfo


def getAssetInfor(asset):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    assetInfo = sg.find_one("Asset", [
        ['code', 'is', asset],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                            ['sg_asset_type', 'sg_asset_name__cn', 'code', 'tasks', 'shots'])
    return assetInfo


def getTaskInfor(taskName):
    projeceInfo = sg.find_one("Project", [['name', 'is', 'df']], ['code', 'sg_description', 'project', 'name'])
    taskInfor = sg.find_one("Task", [
        ['content', 'is', taskName],
        ['project', 'is', {'type': 'Project', 'id': projeceInfo['id']}]
    ],
                            ['sg_task_type', 'code', 'task_assignees','sg_status_list'])

    return taskInfor


def information_shot(shot_name):
    assets = getShotInfo(shot_name)['assets']
    tasks = getShotInfo(shot_name)['tasks']
    print '#' * 60
    print '-------------shot %s----------------' % shot_name
    print 'FrameRange is {}-{}'.format(getShotInfo(shot_name)['sg_cut_in'], getShotInfo(shot_name)['sg_cut_out'])
    print 'Shotgun Asset num is ', len(assets)
    print 'Asset Content:'
    for x in assets:
        asset_sg=getAssetInfor(x['name'])
        CNInfo = asset_sg['sg_asset_name__cn']
        if CNInfo:
            cnName = CNInfo.decode('utf-8')
        else:
            cnName = None

        print '   [', x['name'], '] NameCn :', cnName, ' AssetType : <', Asset_type_cn[asset_sg['sg_asset_type']], '>'
        assetTaskInfor = asset_sg['tasks']
        if assetTaskInfor:
            for assettask in assetTaskInfor:
                if assettask['name'].endswith('_mdl') or assettask['name'].endswith('_rig') or assettask[
                    'name'].endswith('_shd'):
                    asset_task_sg =getTaskInfor(assettask['name'])
                    assetTaskAssignto = asset_task_sg['task_assignees']
                    assetTaskStatus = asset_task_sg['sg_status_list']

                    if assetTaskAssignto:
                        assetTaskUser = assetTaskAssignto[0]['name'].decode('utf-8')
                    else:
                        assetTaskUser = None
                    print ' ' * 15, '<{}>:'.format(assettask['name']), 'Status:['+Status_cn[assetTaskStatus]+']',assetTaskUser

    print 'Task Information:'
    for x in tasks:
        shot_task_sg =getTaskInfor(x['name'])
        assignto = shot_task_sg['task_assignees']
        if assignto:
            user_name = assignto[0]['name'].decode('utf-8')
        else:
            user_name = None
        shotTaskStatus =shot_task_sg['sg_status_list']
        print '   [', x['name'], '] Status:['+Status_cn[shotTaskStatus] +'] AssignTo : <', user_name, '>'
    print '#' * 60
    mc.ScriptEditor()


def run():
    current_shot = mc.file(q=True, sn=True).split('_')
    shot_name = '_'.join(current_shot[1:3])
    information_shot(shot_name)
