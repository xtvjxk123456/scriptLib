import maya.cmds as mc


def run():
    import deleteInvaildReferenceNode;
    deleteInvaildReferenceNode.run()
    import deleteInvaildReferenceNode;
    deleteInvaildReferenceNode.run()

    try:
        mc.delete(mc.ls(type='polyColorPerVertex'))
    except:
        pass

    import update_prompt_timer
    reload(update_prompt_timer)
    dlg = update_prompt_timer.scene_break_down()
    dlg.show()
    dlg.select_all_red()
    dlg.do_update()
    dlg.close()
    import deleteInvaildReferenceNode;
    deleteInvaildReferenceNode.run()
    import deleteInvaildReferenceNode;
    deleteInvaildReferenceNode.run()
