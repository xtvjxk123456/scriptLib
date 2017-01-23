# coding:utf-8
import pymel.core as pm
import pixoLibs.pixoShotgun as psg
import os

def init():
    if not pm.pluginInfo('mtoa.mll', q=True, l=True):
        pm.loadPlugin('mtoa.mll')
    defaultRender = pm.getAttr('defaultRenderGlobals.currentRenderer')

    if defaultRender != 'arnold':
        pm.setAttr("defaultRenderGlobals.currentRenderer", 'arnold', type='string')

    pm.mel.RenderGlobalsWindow()


def get_sg_time_range():
    """
    return SG FrameRange
    return Type:tuple
    """

    filename = os.path.basename(pm.sceneName())
    seq = filename.split('_')[1]
    shot = filename.split('_')[2]
    project = filename.split('_')[0]
    return psg.get_cut_range(project, '%s_%s' % (seq, shot))


def run():
    init()
    begin, end = get_sg_time_range()

    defaultRender = pm.PyNode('defaultRenderGlobals')
    defaultRender.imageFilePrefix.set('<RenderLayer>/<RenderLayer>')
    defaultRender.animation.set(True)
    defaultRender.outFormatControl.set(0)
    defaultRender.putFrameBeforeExt.set(1)
    defaultRender.extensionPadding.set(4)
    defaultRender.periodInExt.set(1)
    defaultRender.startFrame.set(begin)
    pm.editRenderLayerAdjustment('defaultRenderGlobals.endFrame')
    defaultRender.endFrame.set(end)

    defaultDriver = pm.PyNode('defaultArnoldDriver')
    defaultDriver.aiTranslator.set('exr')
    defaultDriver.halfPrecision.set(True)
    defaultDriver.autocrop.set(True)
    defaultDriver.tiled.set(True)

    defaultRenderOption = pm.PyNode('defaultArnoldRenderOptions')
    defaultRenderOption.AASamples.set(5)
    defaultRenderOption.GIDiffuseSamples.set(0)
    defaultRenderOption.GIGlossySamples.set(0)
    defaultRenderOption.GIRefractionSamples.set(0)
    defaultRenderOption.GISssSamples.set(0)
    defaultRenderOption.GIVolumeSamples.set(0)
    defaultRenderOption.lock_sampling_noise.set(True)
    defaultRenderOption.ignoreTextures.set(True)
    defaultRenderOption.ignoreShaders.set(True)

    defaultRenderResolution = pm.PyNode('defaultResolution')
    defaultRenderResolution.width.set(1024)
    defaultRenderResolution.height.set(429)
    defaultRenderResolution.deviceAspectRatio.set(2.387)
    defaultRenderResolution.pixelAspect.set(1.000)
