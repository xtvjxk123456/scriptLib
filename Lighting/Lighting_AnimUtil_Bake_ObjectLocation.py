# bakeResults
# doCreateParentConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };

import maya.mel as mel
import maya.cmds as mc

def run():
    target = mc.ls(sl=True)[0]
    targetloc = mc.spaceLocator( p=[0, 0, 0] )[0]
    #mc.select([target,targetloc],r=True)
    parentNode = mc.parentConstraint( target,targetloc,mo=False,w=1)
    scaleNode = mc.scaleConstraint( target,targetloc,mo=False,w=1)
    begin = mc.playbackOptions(q=True,ast=True)
    end = mc.playbackOptions(q=True,aet=True)
    mc.bakeResults(targetloc,t=(begin,end),sm=True,sb=1,dic=True,pok=True,sac=False,ral=False,bol=False,mr=True,cp=False,s=True)
    mc.delete(parentNode[0],scaleNode[0])

