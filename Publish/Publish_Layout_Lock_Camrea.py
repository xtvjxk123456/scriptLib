import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import maya.cmds as mc

def lockObjectTransform(shapename):
	name = pm.PyNode(shapename).getParent()
	pm.PyNode(name).attr('tx').lock()
	pm.PyNode(name).attr('ty').lock()
	pm.PyNode(name).attr('tz').lock()
	pm.PyNode(name).attr('rx').lock()
	pm.PyNode(name).attr('ry').lock()
	pm.PyNode(name).attr('rz').lock()
	pm.PyNode(name).attr('sx').lock()
	pm.PyNode(name).attr('sy').lock()
	pm.PyNode(name).attr('sz').lock()
	
def getCameraInShot():
	transforms = map(lambda x: mc.listRelatives(x,p=True,pa=True)[0],mc.ls(type='camera'))
	cameraList = zip(transforms,mc.ls(type='camera'))
	f =mc.file(q=True,sn=True)
   	path_obj = pft.PathDetails.parse_path(f)
   	cameraName = 'cam_'+path_obj.seq+'_'+path_obj.shot
	allPossible =[]
	for x in cameraList:
		if x[0].split('|')[-1] == cameraName:
			allPossible.append(x[1])
	return allPossible

def run():
    map(lockObjectTransform,getCameraInShot())
