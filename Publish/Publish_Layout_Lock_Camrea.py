import pymel.core as pm
import Publish_Layout_Bake_CameraToWorld as plb


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


def run():
    map(lockObjectTransform, plb.getCameraInShot())
