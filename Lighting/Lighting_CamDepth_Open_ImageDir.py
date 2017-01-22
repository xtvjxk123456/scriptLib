# coding:utf-8
import pymel.core as pm
import os


def run():
    projectdir = pm.Workspace.getPath()
    imagedir = os.path.join(projectdir, 'images')
    os.startfile(imagedir)
