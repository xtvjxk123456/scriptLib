import maya.cmds as mc

def run():
    if len(mc.ls(sl=True))!=1:
        mc.warning('operation is wrong...')
        return None
    mc.lockNode(mc.ls(sl=True)[0],l=False)
    mc.delete(mc.ls(sl=True)[0])
