import maya.cmds as mc

def run():
    try:
        mc.delete(mc.ls(type ='polyColorPerVertex'))
        mc.warning('Delete All polyColorPerVertex over')
    except Exception:
        mc.warning('Delete All polyColorPerVertex over,no more to Delele')
