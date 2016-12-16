# coding=utf-8
import PySide.QtGui as qg
import PySide.QtCore as qc
import maya.OpenMayaUI as apiUI
import shiboken

import os
import previewShaderInAnim as ps
import pymel.core as pm
import glob


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), qg.QMainWindow)


def getAllchars():
    # -----------
    import deleteInvaildReferenceNode
    deleteInvaildReferenceNode.run()
    # -----------
    reference = []
    for x in pm.listReferences():
        asset = os.path.basename(x.path).split('_')[1]
        if ps.get_asset_type_by_name(asset)[1] == 'Character':
            reference.append(x)

    return reference


class CharInfo(qg.QWidget):
    def __init__(self, refnode):
        super(CharInfo, self).__init__()
        self.mainLayout = qg.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.refnode = refnode
        self.refpath = self.refnode.path

        self.char = pm.FileReference(self.refnode).namespace
        self.asset = os.path.basename(self.refpath).split('_')[1]
        self.version = os.path.basename(self.refpath).split('_')[-2]
        self._versions = self._get_versions()

        self.name_label = qg.QLabel(self.char)
        self.version_option = qg.QComboBox()
        self.version_option.addItems(self._versions)
        self.version_option.setCurrentIndex(self._versions.index(self.version))

        self.update_button = qg.QPushButton('change it!')
        self.update_button.clicked.connect(self.update_file)

        self.mainLayout.addWidget(self.name_label)
        self.mainLayout.addWidget(self.version_option)
        self.mainLayout.addWidget(self.update_button)

    def _get_versions(self):
        char_publish = r'Z:/Shotgun/projects/df/_library/assets/Character/{}/rig/_publish/'.format(self.asset)
        versions = ps.find_folders_in_dir(os.path.normpath(char_publish))

        if not versions:
            pm.warning('{} publish dir has noting'.format(self.asset))
            return None
        versions.sort()
        return versions

    def update_file(self):
        current_version = self.version_option.currentText()
        file_base_name = 'df_' + self.asset + '_rig_' + current_version

        current_publish = r'Z:/Shotgun/projects/df/_library/assets/Character/{}/rig/_publish/{}/{}_*'.format(self.asset,
                                                                                                             current_version,
                                                                                                             file_base_name)
        file_path = glob.glob(os.path.normpath(current_publish))[0]
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
        # -----------


class MainUI(qg.QWidget):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle("Only change char version in Anim")
        self.setObjectName("change_version")
        self.setParent(getMayaWindow())
        self.setWindowFlags(qc.Qt.Window)
        self.setStyleSheet(
            "QWidget{color: #eff0f1;background-color: #31363b;selection-background-color:#3daee9;selection-color: #eff0f1;background-clip: border;border: 0px transparent black;outline: 0;}"
            "QWidget:item:selected{background-color: #3daee9;}"
            "QLabel{border: 0px solid black;}"
            "QPushButton{color: rgb(202, 207, 210);background-color: rgb(27, 28, 30);border-width: 1px;border-color: #76797C;border-style: solid;padding: 5px;border-radius: 10px;outline: none;}"
            "QPushButton:pressed{background-color: #3daee9;padding-top: -15px;padding-bottom: -17px;}"
            "QPushButton:hover{border: 1px solid #3daee9;color: #eff0f1;}"
        )

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 0)
        self.layout().setSpacing(5)

        self.tilte = qg.QLabel('just change char version')
        self.tilte.setFixedHeight(30)
        self.tilte.setAlignment(qc.Qt.AlignCenter)
        self.layout().addWidget(self.tilte)

        self.chars = getAllchars()
        self.assetItem = []
        if self.chars:
            for n in self.chars:
                item = CharInfo(n)
                self.assetItem.append(item)
                self.layout().addWidget(item)

        self.batchWidget = qg.QFrame()
        self.batchWidget.setLayout(qg.QHBoxLayout())
        self.batchWidget.layout().insertStretch(0)

        self.changeAll = qg.QPushButton('change all!')
        self.changeAll.clicked.connect(self._change_all)
        self.batchWidget.layout().addWidget(self.changeAll)
        self.layout().insertStretch(-2)
        self.layout().addWidget(self.batchWidget)

    def _change_all(self):
        for item in self.assetItem:
            item.update_file()


def run():
    if pm.window('change_version', q=True, ex=True):
        pm.deleteUI('change_version')
    win = MainUI()
    win.show()
