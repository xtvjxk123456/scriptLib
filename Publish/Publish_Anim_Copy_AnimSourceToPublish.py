import pixoLibs.pixoFileTools as pft
import os
import maya.cmds as mc

def run():    
    f =mc.file(q=True,sn=True)
    path_obj = pft.PathDetails.parse_path(f)
    publishName = path_obj.getPublishFullPath()
    mc.sysFile(os.path.dirname(publishName),makeDir=True)
    mc.sysFile(f,copy=publishName)

    try:
        xmlf = os.path.splitext(f)[0]+'.xml'
        xmlpublishName = os.path.splitext(publishName)[0]+'.xml'
        mc.sysFile(xmlf,copy=xmlpublishName)
    except Exception:
        pass

#copy anim source file to publish dir
