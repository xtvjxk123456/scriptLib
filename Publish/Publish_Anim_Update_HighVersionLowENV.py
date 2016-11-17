# coding :utf-8
import pymel.core as pm
import os
from aas_sg import get_file_last_version
import previewShaderInAnim as ps
import glob


class AssetReference(object):
    def __init__(self, path):
        self.path = os.path.normpath(path)
        self.filename = os.path.basename(self.path)
        self.asset = self.filename.split('_')[1]
        self.project = self.filename.split('_')[0]
        self.ext = self.filename.split('.')[-1]
        self.task = self.filename.split('_')[2].split('.')[0]
        self.assetType = ps.get_asset_type_by_name(self.asset)[1]

    def old_path(self):
        return self.path

    def aas_path(self):
        publishPath = r'Z:/Shotgun/projects/{}/_library/assets/{}/{}/{}/_publish/{}'.format(self.project,
                                                                                            self.assetType,
                                                                                            self.asset,
                                                                                            self.task,
                                                                                            '_'.join([self.project,
                                                                                                      self.asset,
                                                                                                      self.task, 'v000',
                                                                                                      'xxx.{}'.format(
                                                                                                          self.ext)]))
        if os.path.exists(os.path.normpath(get_file_last_version(publishPath, True))):
            return os.path.normpath(get_file_last_version(publishPath, True))
        else:
            return self.path()

    def high_version_low_mdl_path(self):
        if 'Environment' == self.assetType and 'mdl' == self.task:
            publishPath = r'Z:/Shotgun/projects/{}/_library/assets/{}/{}/{}/_publish/*/{}'.format(self.project,
                                                                                                  self.assetType,
                                                                                                  self.asset,
                                                                                                  self.task,
                                                                                                  '_'.join(
                                                                                                      [self.project,
                                                                                                       self.asset,
                                                                                                       self.task,
                                                                                                       'lo']))
            # paths = glob.glob(publishPath + '_*.{}'.format(self.ext))
            paths = glob.glob(publishPath + '_*')
            versions = {}
            for path in paths:
                version = os.path.basename(os.path.normpath(path)).split('_')[4]
                try:
                    versions.update({version: path})
                except Exception:
                    continue

            order = sorted(versions.keys())
            return os.path.normpath(versions[order[-1]])
        else:
            return None


def run():
    for fileRef in pm.listReferences():
        node = AssetReference(fileRef.path)
        if 'Environment' == node.assetType:
            lowENV = node.high_version_low_mdl_path()
            if lowENV:
                fileRef.replaceWith(lowENV)
