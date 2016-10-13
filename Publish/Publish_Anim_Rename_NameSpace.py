import pymel.core as pm
import re,os
import maya.cmds as mc


def run():
    references = pm.ls(type='reference')

    if len(references)== 0:
        mc.warning('no References!!!!!!!')
        return None
    for x in references:
        try:
            pm.referenceQuery(x,f=True,wcn=True)
        except Exception:
            continue
        ref= pm.FileReference(x) 
        normalPath = ref.path
        assetName= re.match(r'[a-zA-Z]+_([a-zA-Z]+)_[a-zA-Z]+_[a-zA-Z]+[\d]+_*',os.path.basename(normalPath)).group(1)
        cnPath = ref.withCopyNumber()

        if normalPath != cnPath:
            num= re.match(r'.*?\{(\d*)\}',cnPath).group(1)
            NS= assetName+str(num)
        else:
            NS= assetName
        try:
                    pm.namespace(rename = (ref.namespace,NS))
        except Exception:
                    pass
