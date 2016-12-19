# coding:utf-8
import pixoMaya.td_tools as td_tools
import pymel.core as pm
import pixoLibs.pixoFileTools as pft


def get_proxy_for_selected_reference(obj):
    ref_obj = td_tools.ReferenceObj(obj)
    filepath = ref_obj.file
    if filepath:
        if '{' in filepath:
            filepath = filepath.split('{')[0]
        dets = pft.PathDetails.parse_path(filepath)
        dets.user = '*'
        dets.ext = '*'
        dets.name = 'proxy'
        files = list(dets.findMatchingFiles())
        return files[0].getPublishFullPath()
    else:
        return None


def run():
    if pm.ls(sl=True):
        for x in pm.ls(sl=True):
            layers = td_tools.which_render_layers(x)
            ref_obj = td_tools.ReferenceObj(x)
            print layers
            ref = pm.FileReference(ref_obj.file)
            proxy_file = get_proxy_for_selected_reference(x)
            ref.remove()
            # import proxy
            dets = pft.PathDetails.parse_path(proxy_file)
            name_space = dets.shot
            try:
                pm.system.namespace(add=name_space)
            except RuntimeError:
                pass
            pm.system.namespace(set=name_space)
            pm.importFile(proxy_file)
            pm.system.namespace(set=':')
            sel = pm.PyNode('%s:ArnoldStandIn' % name_space)
            sel.rename('%s:%s_mdl' % (name_space, name_space))
            # add this to all the render layers.
            print 'trying to add this:  %s:%s_mdl' % (name_space, name_space)
            td_tools.set_render_layers('%s:%s_mdl' % (name_space, name_space), layers)
    else:
        pm.warning(u'请先选中需要替换的参考内容')
