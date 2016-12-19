# coding:utf-8
import pixoMaya.td_tools as td_tools
import pymel.core as pm
import pixoLibs.pixoFileTools as pft


def get_shader_file_for_selected_proxy(obj):
    sel = obj
    sel_shape = td_tools.return_shape(sel)
    if isinstance(sel_shape, pm.nodetypes.AiStandIn):
        print 'valid'
        arnold_proxy_path = pm.getAttr('%s.dso' % sel_shape)
        dets = pft.PathDetails.parse_path(arnold_proxy_path)
        dets.ext = 'm*'
        dets.name = None
        dets.user = '*'
        files = list(dets.findMatchingFiles())
        return files[0].getPublishFullPath()
    else:
        print 'not a valid arnold proxy'
        return None


def run():
    if pm.ls(sl=True):
        for x in pm.ls(sl=True):

            layers = td_tools.which_render_layers(x)
            shader_file = get_shader_file_for_selected_proxy(x)
            pm.delete(x)
            dets = pft.PathDetails.parse_path(shader_file)
            if dets.category == 'assets':
                namespace = dets.shot
            else:
                if dets.task == 'anim':
                    namespace = dets.name
            # if the namespace exists - remove it
            td_tools.removeNamespace(namespace)
            pm.createReference(shader_file, namespace=namespace)
            td_tools.set_render_layers('%s:%s_mdl' % (namespace, namespace), layers)
    else:
        pm.warning(u'请先选中需要替换的代理内容')
