# coding:utf-8
import pymel.core as pm


def init():
    if not pm.pluginInfo('mtoa.mll', q=True, l=True):
        pm.loadPlugin('mtoa.mll')
    defaultRender = pm.getAttr('defaultRenderGlobals.currentRenderer')

    if defaultRender != 'arnold':
        pm.setAttr("defaultRenderGlobals.currentRenderer", 'arnold', type='string')

    pm.mel.RenderGlobalsWindow()


def run():
    init()
    defaultRender = pm.PyNode('defaultRenderGlobals')
    defaultRender.imageFilePrefix.set('<RenderLayer>/<RenderLayer>')
    defaultRender.animation.set(True)
    defaultRender.outFormatControl.set(0)
    defaultRender.putFrameBeforeExt.set(1)
    defaultRender.extensionPadding.set(4)
    defaultRender.periodInExt.set(1)

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
    defaultRenderResolution.width.set(2048)
    defaultRenderResolution.height.set(858)
    defaultRenderResolution.deviceAspectRatio.set(2.387)
    defaultRenderResolution.pixelAspect.set(1.000)
