import pixoLibs.pixoFileTools as pft 
import maya.mel as mel
import maya.cmds as mc
import os

#change here
_cacheDir = r'Z:\Shotgun\projects\df\data\CamAbc'
def run():                                                                   
    path_obj = pft.PathDetails.parse_path( mc.file(q=1,sn=1))
    startTime = int(mc.playbackOptions(ast=True, q=True))
    endTime =   int(mc.playbackOptions(aet=True, q=True))
    cam_PublishFullPath_abc =_cacheDir+'\{}\{}'.format(path_obj.seq,path_obj.shot)+'\{}'.format(path_obj.task)+ '\\'+mc.ls(sl=True)[0]+'.abc'
    # mel.eval('AbcExport -j "-frameRange '+str(startTime)+' '+str(endTime)+' -stripNamespaces -worldSpace -root '+ mc.ls(sl=True,l=True)[0] +' -file '+cam_PublishFullPath_abc+'"')
    mc.sysFile(os.path.dirname(cam_PublishFullPath_abc),md=True)
    mel.eval('AbcExport -j "-frameRange {} {} -stripNamespaces -worldSpace -root {} -file {}"'.format(str(startTime),str(endTime),mc.ls(sl=True,l=True)[0],os.path.normpath(cam_PublishFullPath_abc).replace('\\','/')))

