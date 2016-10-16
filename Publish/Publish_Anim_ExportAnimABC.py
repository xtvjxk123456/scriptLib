import pixoLibs.magiclist.maya_magic_list as magic_list
import pixoMaya.base as base


def run():
    magic_list.run(base.get_anim_geo, 'Publish Animation',
                   {'Export Alembic': base.export_anim_publish, 'Go to File': base.filebrowse_to_anim})
