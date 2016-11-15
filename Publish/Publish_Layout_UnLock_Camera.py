import pymel.core as pm
import Publish_Layout_Bake_CameraToWorld as plb


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


def run():
    map(UnlockObjectTransform, plb.getCameraInShot())
