# coding:utf-8
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import maya.OpenMayaUI as apiUI
import shiboken

import os
import sys
import pymel.core as pm
import previewShaderInAnim as ps
import glob
import aas_sg

sg = aas_sg.get_standalone_sg()
ASSETLIBPATH = 'Z:/Shotgun/projects/df/_library/assets/'


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)


def getAssetPath(asset, task):
    try:
        assetType = ps.get_asset_type_by_name(asset)[1]
    except Exception, e:
        pm.warning(e)
        return None
    standardPath = os.path.normpath(os.path.join(ASSETLIBPATH, '{}/{}/{}/_publish'.format(assetType, asset, task)))
    if task == 'shader':
        standardPath = os.path.normpath(os.path.join(ASSETLIBPATH, '{}/{}/{}/_publish'.format(assetType, asset, 'shd')))
    if os.path.exists(standardPath):
        versions = ps.find_folders_in_dir(standardPath)

        if not versions:
            pm.warning(u'资产{}没有publish过{}任何文件'.format(asset, task))
            return None
        versions.sort()
        rightPath = os.path.join(standardPath, '{}/df_{}_{}_{}_???.m?'.format(versions[-1], asset, task, versions[-1]))
        if task == 'shader':
            rightPath = os.path.join(standardPath,
                                     '{}/df_{}_{}_{}_???.m?'.format(versions[-1], asset, 'shd_shaders', versions[-1]))
        file_path = glob.glob(os.path.normpath(rightPath))
        if file_path:
            return file_path[0]
        else:
            pm.warning(u'资产{}文件{}没有publish完成?'.format(asset, task))
            return None
    else:
        pm.warning(u'资产{}没有publish过{}任何文件'.format(asset, task))
        return None


def getAllAsset():
    assets = sg.find('Asset', [], ['code'])
    codes = [x['code'] for x in assets]
    return codes


class AdvComboBox(QtGui.QComboBox):
    """
    can filter it's item
    """

    def __init__(self, parent=None):
        super(AdvComboBox, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer
        self.completer = QtGui.QCompleter(self)
        # Set the model that the QCompleter uses
        # - in PySide doing this as a separate step worked better
        self.completer.setModel(self.pFilterModel)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)

        self.setCompleter(self.completer)

        # connect signals

        def filter(text):
            # print "Edited: ", text, "type: ", type(text)
            self.pFilterModel.setFilterFixedString(str(text))

        self.lineEdit().textEdited[unicode].connect(filter)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        print "activated"
        if text:
            print "text: ", text
            index = self.findText(str(text))
            print "index: ", index
            self.setCurrentIndex(index)

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(AdvComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(AdvComboBox, self).setModelColumn(column)


class MainUI(QtGui.QWidget):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle("import asset into scene")
        self.setObjectName("import_asset")
        self.setParent(getMayaWindow())
        self.setWindowFlags(QtCore.Qt.Window)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(2, 2, 2, 0)
        self.mainLayout.setSpacing(10)

        self.information = QtGui.QLabel('Import asset in selected task')
        self.information.setAlignment(QtCore.Qt.AlignCenter)

        self.assetList = AdvComboBox()
        self.assetList.addItems(getAllAsset())
        self.assetList.setModelColumn(0)
        self.assetList.activated[unicode].connect(self._update_tooltip)

        self.taskList = QtGui.QComboBox()
        self.taskList.addItems(['mdl', 'rig', 'shd', 'shader'])
        self.taskList.activated[unicode].connect(self._update_tooltip)

        self.importButton = QtGui.QPushButton('import it!')
        self.importButton.clicked.connect(self._import_asset_in_task)

        self.previewBar = QtGui.QStatusBar()
        self.previewBar.showMessage('Ready!')

        self.importLayout = QtGui.QHBoxLayout()
        self.importLayout.addWidget(self.assetList)
        self.importLayout.addWidget(self.taskList)
        self.importLayout.addWidget(self.importButton)

        self.mainLayout.addWidget(self.information)
        self.mainLayout.addLayout(self.importLayout)
        self.mainLayout.insertStretch(-2)
        self.mainLayout.addWidget(self.previewBar)

    def _update_tooltip(self, task):
        result = getAssetPath(self.assetList.currentText(), self.taskList.currentText())
        self.importButton.setToolTip(result)

    # def _preview_result(self, task):
    #     result = getAssetPath(self.assetList.currentText(), task)
    #     return result

    def _import_asset_in_task(self):
        assetName = self.assetList.currentText()
        taskName = self.taskList.currentText()
        importpath = getAssetPath(assetName, taskName)
        if importpath:
            postfix = ''
            if taskName == 'shader':
                postfix = '_shd'
            pm.createReference(importpath, namespace=assetName + postfix)
            self.previewBar.showMessage('Done!', 100000)
            self.previewBar.showMessage('Ready!')


def run():
    if pm.window('import_asset', q=True, ex=True):
        pm.deleteUI('import_asset')
    win = MainUI()
    win.show()
