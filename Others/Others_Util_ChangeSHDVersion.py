# coding:utf-8
from Others_Util_ChangeCharVersion import CharInfo, getMayaWindow
import pymel.core as pm
import os
import glob
import previewShaderInAnim as ps


def getAllSHD():
    # -----------
    import deleteInvaildReferenceNode
    deleteInvaildReferenceNode.run()
    # -----------
    reference = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Environment':
            reference.append(x)

    return reference


class SHDInfo(CharInfo):
    def __init__(self, refnode):
        super(CharInfo, self).__init__(refnode)

    def _get_versions(self):
        SHD_publish = r'Z:/Shotgun/projects/df/_library/assets/Environment/{}/shd/_publish/'.format(self.asset)
        versions = ps.find_folders_in_dir(os.path.normpath(SHD_publish))

        if not versions:
            pm.warning('{} publish dir has noting'.format(self.asset))
            return None
        versions.sort()
        return versions

    def update_file(self):
        current_version = self.version_option.currentText()
        file_base_name = 'df_' + self.asset + '_shd_' + current_version

        current_publish = r'Z:/Shotgun/projects/df/_library/assets/Environment/{}/shd/_publish/{}/{}_*'.format(
            self.asset,
            current_version,
            file_base_name)
        file_paths = glob.glob(os.path.normpath(current_publish))
        if len(file_paths) == 1:
            file_path = file_paths[0]
            oldpath = self.refpath
            pm.warning('Begin changing {} version'.format(self.char))
            pm.warning('--Old:{}'.format(os.path.normpath(oldpath)))
            pm.warning('--New:{}'.format(os.path.normpath(file_path)))

            if os.path.normpath(file_path) != os.path.normpath(oldpath):
                pm.FileReference(self.refnode).replaceWith(os.path.normpath(file_path))
                # update "refpath" value
                self.refpath = self.refnode.path
            # -----------
            import deleteInvaildReferenceNode
            deleteInvaildReferenceNode.run()
        else:
            pm.warning(u'{}的shd publish目录有问题'.format(self.asset))
