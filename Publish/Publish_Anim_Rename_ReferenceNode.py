import pymel.core as pm

def run():
    if pm.nodeType(pm.ls(sl=True)[0]) == 'reference':
        result = pm.promptDialog(
            title='Rename Object',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if result == 'OK':
            name = pm.promptDialog(query=True, text=True)
            if name != '':
                pm.lockNode(pm.ls(sl=True)[0],l=False)
                pm.rename(pm.ls(sl=True)[0],name)
                pm.lockNode(pm.ls(sl=True)[0])

#rename referece node name
