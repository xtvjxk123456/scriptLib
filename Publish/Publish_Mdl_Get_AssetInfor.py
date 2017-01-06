# coding:utf-8
import Others_UtilScript_Get_Shotgun_ShotInfor as ougs
import pymel.core as pm
import os


def checkScene():
    if pm.sceneName():
        filename = os.path.basename(pm.sceneName())

        if filename.split('_')[1][0].isdigit():
            # scene is shot file
            return False
        else:
            # scene is asset file
            return True
    else:
        return False


def assetName():
    filename = os.path.basename(pm.sceneName())
    return filename.split('_')[2]


def information_asset(name):
    print '-' * 60
    print '-------------Asset %s----------------' % name
    print 'Task Info:'
    tasks = ougs.getAssetInfor(name)['tasks']
    if tasks:
        for task in tasks:
            user = ougs.getTaskInfor(task['name'])['task_assignees']
            if user:
                userName = user[0]['name'].decode('utf-8')
            else:
                userName = None
            print ' ' * 5, '[ {} ]:'.format(task['name'].split('_')[-1]), userName
    print 'Relate Shot:'
    shots = ougs.getAssetInfor(name)['shots']
    if shots:
        for shot in shots:
            description = ougs.getShotInfo(shot['name'])['description']
            if description:
                descriptionInfor = description.decode('utf-8')
            else:
                descriptionInfor = None
            print ' ' * 5, '[ {} ]: '.format(shot['name']), descriptionInfor, u'(备注)'
            shotTasks = ougs.getShotInfo(shot['name'])['tasks']
            if shotTasks:
                for shotTask in shotTasks:
                    if shotTask['name'].endswith('_lgt'):
                        shotTaskUser = ougs.getTaskInfor(shotTask['name'])['task_assignees']
                        if shotTaskUser:
                            shotTaskUserName = shotTaskUser[0]['name'].decode('utf-8')
                        else:
                            shotTaskUserName = None
                        print ' ' * 10, '[ {} ]'.format(shotTask['name']), shotTaskUserName

    print '-' * 60
    pm.ScriptEditor()


def run():
    if checkScene():
        information_asset(assetName())
    else:
        pm.warning(u'这个文件不是资产文件,不能获取信息')
