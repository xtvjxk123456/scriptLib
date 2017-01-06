# coding:utf-8
import Others_UtilScript_Get_Shotgun_ShotInfor as ougs
import pymel.core as pm
import os


def checkScene():
    filename = os.path.basename(pm.sceneName())
    if filename.split('_')[1][0].isdigit():
        # scene is shot file
        return False
    else:
        # scene is asset file
        return True


def assetName():
    filename = os.path.basename(pm.sceneName())
    return filename.split('_')[2]


def run():
    if checkScene():
        name = assetName()

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
                print '-' * 15, '{}:'.format(task['name'].split('_')[-1]), userName
        print 'Relate Shot:'


        print '-' * 60
