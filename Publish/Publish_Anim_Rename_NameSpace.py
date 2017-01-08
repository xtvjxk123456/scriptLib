# coding:utf-8
import maya.OpenMaya as om
import re, os
import maya.cmds as mc


def run():
    references_path = {}
    om.MFileIO.getReferences(references_path)

    if len(references_path) == 0:
        mc.warning('no References!!!!!!!')
        return None
    for x in references_path:

        refNode = mc.file(x, q=True, rfn=True)
        resolve_path = mc.referenceQuery(refNode, f=True)
        unresolve_path = mc.referenceQuery(refNode, f=True, wcn=True)
        assetName = os.path.basename(resolve_path).split('_')[1]
        ref_namespace = mc.referenceQuery(refNode, ns=True)

        if unresolve_path != resolve_path:
            num = re.match(r'.*?\{(\d*)\}', resolve_path).group(1)
            NS = assetName + str(num)
        else:
            NS = assetName
        try:
            mc.namespace(rename=(ref_namespace, NS))
        except Exception:
            pass
