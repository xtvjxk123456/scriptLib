# coding:utf-8
import pymel.core as pm


def run():
    defaultRenderGlobal = pm.PyNode('defaultRenderGlobals')
    begin = defaultRenderGlobal.startFrame.get()
    end =defaultRenderGlobal.endFrame.get()

    mainprocess = pm.mel.eval('$tmp = $gMainProgressBar')
    pm.progressBar(mainprocess,
                   edit=True,
                   beginProgress=True,
                   isInterruptable=True,
                   status='Rendering in foreground ...',
                   minValue = int(begin),
                   maxValue=int(end))

    for x in range(int(begin), int(end)+2):
        if pm.progressBar(mainprocess, q=True, ic=True):
            break

        pm.progressBar(mainprocess, e=True, step=1)
        pm.currentTime(x)
        pm.arnoldRender(b=True, seq=str(x))
        pm.refresh()
    pm.progressBar(mainprocess,
                   edit=True,
                   endProgress=True,
                   )
    pm.warning('BatchRender activeRenderLayer complete!')
