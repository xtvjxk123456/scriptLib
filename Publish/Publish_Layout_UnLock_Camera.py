import pymel.core as pm
import pixoLibs.pixoFileTools as pft
import maya.cmds as mc

def UnlockObjectTransform(shapename):
	name = pm.PyNode(shapename).getParent()
	pm.PyNode(name).attr('tx').unlock()
	pm.PyNode(name).attr('ty').unlock()
	pm.PyNode(name).attr('tz').unlock()
	pm.PyNode(name).attr('rx').unlock()
	pm.PyNode(name).attr('ry').unlock()
	pm.PyNode(name).attr('rz').unlock()
	pm.PyNode(name).attr('sx').unlock()
	pm.PyNode(name).attr('sy').unlock()
	pm.PyNode(name).attr('sz').unlock()
	
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
    map(UnlockObjectTransform,getCameraInShot())
