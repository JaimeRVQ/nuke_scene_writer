# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: scene_writerUI.py
Date: 2019.09.29
Revision: 2019.09.29
Copyright: Copyright Jaime Rivera 2019 | www.jaimervq.com
           The program(s) herein may be used, modified and/or distributed in accordance with the terms and conditions
           stipulated in the Creative Commons license under which the program(s) have been registered. (CC BY-SA 4.0)

Brief:

'''

__author__ = 'Jaime Rivera <jaime.rvq@gmail.com>'
__copyright__ = 'Copyright 2019, Jaime Rivera'
__credits__ = []
__license__ = 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'
__maintainer__ = 'Jaime Rivera'
__email__ = 'jaime.rvq@gmail.com'
__status__ = 'Testing'

from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
import os
import datetime

import nuke_specific_functions
reload(nuke_specific_functions)

class SceneWriter(QtWidgets.QWidget):

    def __init__(self):

        QtWidgets.QWidget.__init__(self)
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path).replace('\\', '/') + '/'
        file = QtCore.QFile(dir_path+'scene_writerUI.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(file, self)

        # WINDOW STYLE
        self.icons_path = dir_path + '/icons/'
        self.setWindowIcon(QtGui.QIcon(self.icons_path + 'write.png'))

        scene = nuke_specific_functions.get_the_scene()
        self.scene_name = scene if scene != '' else 'Untitled'
        self.setWindowTitle('Scene writer ({})'.format(self.scene_name.split('/')[-1]))
        self.setFixedSize(1167,501)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # LOG
        self.showing_log = True

        # SETUP
        self.setup_style()
        self.make_connections()
        self.append_to_log('-- POPULATING SCANLINE RENDER TABLE --', 'cyan')
        self.populate_scanline()
        self.append_to_log('-- POPULATING RAY RENDER TABLE --', 'cyan')
        self.populate_ray()
        self.append_to_log('-- POPULATING WRITE NODES TABLE --', 'cyan')
        self.populate_write()

        self.show()


    def setup_style(self):

        # TABLE SIZES
        scanline_header = self.ui.scanline_table.horizontalHeader()
        scanline_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        scanline_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        scanline_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        scanline_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        scanline_header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        ray_header = self.ui.ray_table.horizontalHeader()
        ray_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        ray_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        ray_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        ray_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        write_header = self.ui.write_table.horizontalHeader()
        write_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        write_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        write_header.resizeSection(2, 200)
        write_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        write_header.resizeSection(3, 90)
        write_header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        write_header.resizeSection(4, 70)
        write_header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        write_header.resizeSection(5, 120)
        write_header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)


        # BUTTONS
        self.ui.write_all_btn.setIcon(QtGui.QIcon(self.icons_path + 'write.png'))
        self.ui.write_all_btn.setIconSize(QtCore.QSize(30, 30))

        self.ui.write_selected_btn.setIcon(QtGui.QIcon(self.icons_path + 'check.png'))
        self.ui.write_selected_btn.setIconSize(QtCore.QSize(15, 15))

        # LOG
        self.ui.clear_btn.setIcon(QtGui.QIcon(self.icons_path + 'clear.png'))
        self.ui.clear_btn.setIconSize(QtCore.QSize(25, 25))
        self.ui.clear_btn.setToolTip('Clear log')

        self.ui.eye_btn.setIcon(QtGui.QIcon(self.icons_path + 'hide.png'))
        self.ui.eye_btn.setIconSize(QtCore.QSize(25, 25))
        self.ui.eye_btn.setToolTip('Hide log output text')


        self.ui.log.insertHtml("<font color = cyan>[{}] SCENE WRITER WINDOW CREATED".format(str(datetime.datetime.now().time())[:12]))
        self.ui.log.insertHtml("<br><font color = cyan>[{0}] SCENE: {1}".format(str(datetime.datetime.now().time())[:12], self.scene_name))


    def make_connections(self):

        self.ui.tabs.currentChanged.connect(self.toggled_tabs)

        self.ui.write_table.cellClicked.connect(self.modify_writes)

        self.ui.clear_btn.clicked.connect(self.clear_log)
        self.ui.eye_btn.clicked.connect(self.toggle_log)
        
        self.ui.write_all_btn.clicked.connect(self.customize_and_write)
        self.ui.write_selected_btn.clicked.connect(lambda: self.customize_and_write(True))

    def populate_scanline(self):

        import nuke

        if len(nuke.allNodes('ScanlineRender')) == 0:
            self.append_to_log('INFO: No ScanlineRender nodes found', 'orange')

        for node in nuke.allNodes('ScanlineRender'):
            row = self.ui.scanline_table.rowCount()

            self.ui.scanline_table.insertRow(self.ui.scanline_table.rowCount())

            scanline_name = QtWidgets.QTableWidgetItem()
            scanline_name.setTextAlignment(QtCore.Qt.AlignCenter)
            scanline_name.setText(node.name())
            scanline_name.setFlags(QtCore.Qt.ItemIsEditable)
            scanline_name.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            self.ui.scanline_table.setItem(row, 0, scanline_name)

            aa_filter = QtWidgets.QComboBox()
            aa_filter.addItems(['Impulse', 'Cubic', 'Keys', 'Simon', 'Rifman', 'Mitchell', 'Parzen', 'Notch', 'Lanczos4', 'Lanczos6',
                                'Sinc4', 'Nearest', 'Bilinear', 'Trilinear', 'Anisotropic'])
            aa_filter.setCurrentIndex(node['filter'].getValue())
            self.ui.scanline_table.setCellWidget(row, 1, aa_filter)

            aa_options = QtWidgets.QComboBox()
            aa_options.addItems(['None', 'Low', 'Medium', 'High'])
            aa_options.setCurrentIndex(node['antialiasing'].getValue())
            self.ui.scanline_table.setCellWidget(row, 2, aa_options)

            aa_samples = QtWidgets.QSpinBox()
            aa_samples.setMinimum(0)
            aa_samples.setMaximum(50)
            aa_samples.setValue(node['samples'].getValue())
            self.ui.scanline_table.setCellWidget(row, 3, aa_samples)

            aa_shutter = QtWidgets.QDoubleSpinBox()
            aa_shutter.setMinimum(-10)
            aa_shutter.setMaximum(10)
            aa_shutter.setSingleStep(0.25)
            aa_shutter.setValue(node['shutter'].getValue())
            self.ui.scanline_table.setCellWidget(row, 4, aa_shutter)

            self.append_to_log('Found ScanlineRender node {}, added to list'.format(node.name()), 'lime')


    def populate_ray(self):

        import nuke

        if len(nuke.allNodes('RayRender')) == 0:
            self.append_to_log('INFO: No RayRender nodes found', 'orange')

        for node in nuke.allNodes('RayRender'):
            row = self.ui.ray_table.rowCount()

            self.ui.ray_table.insertRow(self.ui.ray_table.rowCount())

            ray_name = QtWidgets.QTableWidgetItem()
            ray_name.setTextAlignment(QtCore.Qt.AlignCenter)
            ray_name.setText(node.name())
            ray_name.setFlags(QtCore.Qt.ItemIsEditable)
            ray_name.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            self.ui.ray_table.setItem(row, 0, ray_name)

            aa_filter = QtWidgets.QComboBox()
            aa_filter.addItems(['Impulse', 'Cubic', 'Keys', 'Simon', 'Rifman', 'Mitchell', 'Parzen', 'Notch', 'Lanczos4', 'Lanczos6', 'Sinc4'])
            aa_filter.setCurrentIndex(node['filter'].getValue())
            self.ui.ray_table.setCellWidget(row, 1, aa_filter)

            aa_samples = QtWidgets.QSpinBox()
            aa_samples.setMinimum(0)
            aa_samples.setMaximum(50)
            aa_samples.setValue(node['samples'].getValue())
            self.ui.ray_table.setCellWidget(row, 2, aa_samples)

            aa_shutter = QtWidgets.QDoubleSpinBox()
            aa_shutter.setMinimum(-10)
            aa_shutter.setMaximum(10)
            aa_shutter.setSingleStep(0.25)
            aa_shutter.setValue(node['shutter'].getValue())
            self.ui.ray_table.setCellWidget(row, 3, aa_shutter)

            self.append_to_log('Found RayRender node {}, added to list'.format(node.name()), 'lime')


    def populate_write(self):
        
        import nuke

        if len(nuke.allNodes('Write')) == 0:
            self.append_to_log('INFO: No Write nodes found', 'orange')

        for node in nuke.allNodes('Write'):
            row = self.ui.write_table.rowCount()

            self.ui.write_table.insertRow(self.ui.write_table.rowCount())

            write_name = QtWidgets.QTableWidgetItem()
            write_name.setText(node.name())
            write_name.setFlags(QtCore.Qt.ItemIsEditable)
            write_name.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            self.ui.write_table.setItem(row, 0, write_name)

            write_directory = QtWidgets.QTableWidgetItem()
            write_directory.setFlags(QtCore.Qt.ItemIsEditable)
            write_directory.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            original_write_dir = os.path.dirname(node['file'].value())
            if original_write_dir == '':
                write_directory.setText(os.path.dirname(self.scene_name))
            else:
                write_directory.setText(original_write_dir)
            dir_icon = QtGui.QIcon(self.icons_path + 'folder.png')
            dir_icon.addPixmap(self.icons_path + 'folder.png', QtGui.QIcon.Disabled)
            write_directory.setIcon(dir_icon)
            self.ui.write_table.setItem(row, 1, write_directory)

            comment_line = QtWidgets.QLineEdit()
            comment_validator = QtGui.QRegExpValidator(QtCore.QRegExp("[a-z0-9_]*"))
            comment_line.setValidator(comment_validator)
            comment_line.setAlignment(QtCore.Qt.AlignCenter)
            comment_line.setText('only_lowkey_comments')
            self.ui.write_table.setCellWidget(row, 2, comment_line)

            padding_line = QtWidgets.QLineEdit()
            padding_validator = QtGui.QRegExpValidator(QtCore.QRegExp("#*"))
            padding_line.setValidator(padding_validator)
            padding_line.setAlignment(QtCore.Qt.AlignCenter)
            padding_line.setText('####')
            self.ui.write_table.setCellWidget(row, 3, padding_line)

            format_line = QtWidgets.QLineEdit()
            format_validator = QtGui.QRegExpValidator(QtCore.QRegExp("\.[a-z]*"))
            format_line.setValidator(format_validator)
            format_line.setAlignment(QtCore.Qt.AlignCenter)
            format_line.setText('.png')
            self.ui.write_table.setCellWidget(row, 4, format_line)

            range_line = QtWidgets.QLineEdit()
            range_validator = QtGui.QRegExpValidator(QtCore.QRegExp("\d+-?\d+"))
            range_line.setValidator(range_validator)
            range_line.setAlignment(QtCore.Qt.AlignCenter)
            range_line.setText('1-10')
            self.ui.write_table.setCellWidget(row, 5, range_line)

            self.append_to_log('Found Write node {}, added to list'.format(node.name()), 'lime')


    def toggled_tabs(self, index):

        if index == 1:
            self.ui.write_all_btn.setEnabled(True)
            self.ui.write_selected_btn.setEnabled(True)

        else:
            self.ui.write_all_btn.setEnabled(False)
            self.ui.write_selected_btn.setEnabled(False)


    def modify_writes(self, row, column):

        if column == 0:

            node_cell = self.ui.write_table.item(row, 0)
            state = node_cell.icon()

            if not state:
                check_icon = QtGui.QIcon(self.icons_path + 'check.png')
                check_icon.addPixmap(self.icons_path + 'check.png', QtGui.QIcon.Disabled)
                node_cell.setIcon(check_icon)
            else:
                node_cell.setIcon(QtGui.QIcon())


        elif column == 1:

            dir_cell = self.ui.write_table.item(row, 1)
            new_dir = QtWidgets.QFileDialog().getExistingDirectory()

            if new_dir:
                dir_cell.setText(new_dir)


    def toggle_log(self):

        if self.showing_log:

            self.ui.log.hide()
            self.ui.clear_btn.hide()
            self.ui.eye_btn.move(190, 460)
            self.ui.eye_btn.setIcon(QtGui.QIcon(self.icons_path + 'show.png'))
            self.ui.eye_btn.setToolTip('Show log output text')
            self.showing_log = not self.showing_log

        else:

            self.ui.log.show()
            self.ui.clear_btn.show()
            self.ui.eye_btn.move(1120, 460)
            self.ui.eye_btn.setIcon(QtGui.QIcon(self.icons_path + 'hide.png'))
            self.ui.eye_btn.setToolTip('Hide log output text')
            self.showing_log = not self.showing_log


    def clear_log(self):

        self.ui.log.clear()
        self.ui.log.insertHtml("<font color = cyan>[{}] LOG CLEARED".format(str(datetime.datetime.now().time())[:12]))


    def append_to_log(self, message, color):

        time = str(datetime.datetime.now().time())[:12]
        text = "<br><font color = {0}>[{1}] {2}".format(color, time, message)
        self.ui.log.insertHtml(text)

        self.ui.log.moveCursor(QtGui.QTextCursor.End)
        
    
    def build_original_dictionary(self):

        import nuke
        
        self.append_to_log('-- SAVING ORIGINAL CONFIGURATION OF NODES --', 'cyan')

        original_dictionary = {'scanlines': None,
                               'rays': None,
                               'writes': None}

        # SCANLINE RENDER NODES
        if self.ui.scanline_table.rowCount() == 0:
            self.append_to_log('INFO: No ScanlineRender nodes in the scene', 'orange')

        else:

            scanlines_dict = {}

            for row in range(self.ui.scanline_table.rowCount()):

                scnl_name = str(self.ui.scanline_table.item(row, 0).text())
                scnl_node = nuke.toNode(scnl_name)

                if not scnl_node:
                    self.append_to_log('ERROR: ScanlineRender node {} not found, skipped'.format(scnl_name), 'red')
                else:
                    scanlines_dict[scnl_name] = {}

                    scnl_filter = int(scnl_node['filter'].getValue())
                    scanlines_dict[scnl_name]['filter'] = scnl_filter

                    scnl_antialiasing = int(scnl_node['antialiasing'].getValue())
                    scanlines_dict[scnl_name]['antialiasing'] = scnl_antialiasing

                    scnl_samples = int(scnl_node['samples'].getValue())
                    scanlines_dict[scnl_name]['samples'] = scnl_samples

                    scnl_shutter = scnl_node['shutter'].getValue()
                    scanlines_dict[scnl_name]['shutter'] = scnl_shutter

                    self.append_to_log('ScanlineRender node {0}, FILTER:{1}, AA:{2}, SAMPLES:{3}, SHUTTER:{4}'
                                       ''.format(scnl_name, scnl_filter, scnl_antialiasing, scnl_samples, scnl_shutter), 'lime')

            original_dictionary['scanlines'] = scanlines_dict


        # RAY RENDER NODES
        if self.ui.ray_table.rowCount() == 0:
            self.append_to_log('INFO: No RayRender nodes in the scene', 'orange')

        else:

            rays_dict = {}

            for row in range(self.ui.ray_table.rowCount()):

                ray_name = str(self.ui.ray_table.item(row, 0).text())
                ray_node = nuke.toNode(ray_name)

                if not ray_node:
                    self.append_to_log('ERROR: RayRender node {} not found, skipped'.format(ray_name), 'red')
                else:
                    rays_dict[ray_name] = {}

                    ray_filter = int(ray_node['filter'].getValue())
                    rays_dict[ray_name]['filter'] = ray_filter

                    ray_samples = int(ray_node['samples'].getValue())
                    rays_dict[ray_name]['samples'] = ray_samples

                    ray_shutter = ray_node['shutter'].getValue()
                    rays_dict[ray_name]['shutter'] = ray_shutter

                    self.append_to_log('RayRender node {0}, FILTER:{1}, SAMPLES:{2}, SHUTTER:{3}'
                                       ''.format(ray_name, ray_filter, ray_samples, ray_shutter), 'lime')

            original_dictionary['rays'] = rays_dict

        # WRITE RENDER NODES
        if self.ui.write_table.rowCount() == 0:
            self.append_to_log('INFO: No Write nodes in the scene', 'orange')

        else:

            writes_dict = {}

            for row in range(self.ui.write_table.rowCount()):

                write_name = str(self.ui.write_table.item(row, 0).text())
                write_node = nuke.toNode(write_name)

                if not write_node:
                    self.append_to_log('ERROR: Write node {} not found, skipped'.format(write_name), 'red')
                else:
                    writes_dict[write_name] = {}
                    write_file = str(write_node['file'].value())
                    writes_dict[write_name]['file'] = write_file

                    self.append_to_log('Write node {0}, FILE:{1}'.format(write_name, write_file), 'lime')

            original_dictionary['writes'] = writes_dict

        return original_dictionary

    def build_custom_dictionary(self):

        import nuke

        self.append_to_log('-- BUILDING CUSTOM CONFIGURATION OF NODES --', 'cyan')

        custom_dictionary = {'scanlines': None,
                             'rays': None,
                             'writes': None}

        # SCANLINE RENDER NODES
        if self.ui.scanline_table.rowCount() == 0:
            self.append_to_log('INFO: No ScanlineRender nodes in the list', 'orange')

        else:

            scanlines_dict = {}

            for row in range(self.ui.scanline_table.rowCount()):

                scnl_name = str(self.ui.scanline_table.item(row, 0).text())

                if nuke.toNode(scnl_name) is None:
                    self.append_to_log('ERROR: ScanlineRender node {} not found, skipped'.format(scnl_name), 'red')
                else:
                    scanlines_dict[scnl_name] = {}

                    scnl_filter = self.ui.scanline_table.cellWidget(row, 1).currentIndex()
                    scanlines_dict[scnl_name]['filter'] = scnl_filter

                    scnl_antialiasing = self.ui.scanline_table.cellWidget(row, 2).currentIndex()
                    scanlines_dict[scnl_name]['antialiasing'] = scnl_antialiasing

                    scnl_samples = int(self.ui.scanline_table.cellWidget(row, 3).value())
                    scanlines_dict[scnl_name]['samples'] = scnl_samples

                    scnl_shutter = self.ui.scanline_table.cellWidget(row, 4).value()
                    scanlines_dict[scnl_name]['shutter'] = scnl_shutter

                    self.append_to_log('ScanlineRender node {0}, FILTER:{1}, AA:{2}, SAMPLES:{3}, SHUTTER:{4}'
                                       ''.format(scnl_name, scnl_filter, scnl_antialiasing, scnl_samples, scnl_shutter), 'lime')

            custom_dictionary['scanlines'] = scanlines_dict
            
            
        # RAY RENDER NODES
        if self.ui.ray_table.rowCount() == 0:
            self.append_to_log('INFO: No RayRender nodes in the list', 'orange')

        else:

            rays_dict = {}

            for row in range(self.ui.ray_table.rowCount()):

                ray_name = str(self.ui.ray_table.item(row, 0).text())

                if nuke.toNode(ray_name) is None:
                    self.append_to_log('ERROR: RayRender node {} not found, skipped'.format(ray_name), 'red')
                else:
                    rays_dict[ray_name] = {}

                    ray_filter = self.ui.ray_table.cellWidget(row, 1).currentIndex()
                    rays_dict[ray_name]['filter'] = ray_filter

                    ray_samples = int(self.ui.ray_table.cellWidget(row, 2).value())
                    rays_dict[ray_name]['samples'] = ray_samples

                    ray_shutter = self.ui.ray_table.cellWidget(row, 3).value()
                    rays_dict[ray_name]['shutter'] = ray_shutter

                    self.append_to_log('RayRender node {0}, FILTER:{1}, SAMPLES:{2}, SHUTTER:{3}'
                                       ''.format(ray_name, ray_filter, ray_samples, ray_shutter), 'lime')

            custom_dictionary['rays'] = rays_dict
            
            
        # WRITE RENDER NODES
        if self.ui.write_table.rowCount() == 0:
            self.append_to_log('INFO: No Write nodes in the list', 'orange')

        else:

            writes_dict = {}

            for row in range(self.ui.write_table.rowCount()):

                write_name = str(self.ui.write_table.item(row, 0).text())

                if nuke.toNode(write_name) is None:
                    self.append_to_log('ERROR: Write node {} not found, skipped'.format(write_name), 'red')

                else:
                    target_dir = str(self.ui.write_table.item(row, 1).text())

                    if not os.path.exists(target_dir):
                        self.append_to_log('ERROR: Write node {0} has a non-existent file path, will be skipped'.format(write_name), 'red')

                    else:
                        writes_dict[write_name] = {}

                        write_selected = False
                        if self.ui.write_table.item(row, 0).icon():
                            write_selected = True
                        writes_dict[write_name]['selected'] = write_selected

                        if target_dir.endswith('/'):
                            target_dir = target_dir[:-1]
                        custom_file = (target_dir) + '/' + \
                                      str(self.ui.write_table.cellWidget(row, 2).text()) + '.' + \
                                      str(self.ui.write_table.cellWidget(row, 3).text()) + \
                                      str(self.ui.write_table.cellWidget(row, 4).text())
                        writes_dict[write_name]['file'] = custom_file

                        write_range = str(self.ui.write_table.cellWidget(row, 5).text())
                        writes_dict[write_name]['range'] = write_range

                        self.append_to_log('Write node {0}, SELECTED:{1}, FILE:{2}, RANGE:{3}'.format(write_name, write_selected, custom_file, write_range), 'lime')

            custom_dictionary['writes'] = writes_dict


        return custom_dictionary

        
    def customize_and_write(self, only_selected=False):

        # BUILDING ORIGINAL DICT
        original_dict = self.build_original_dictionary()

        # BUILDING CUSTOM DICT
        custom_dict = self.build_custom_dictionary()

        # CUSTOMIZING NODES
        logs = nuke_specific_functions.customize_nodes(custom_dict, only_selected)
        for log in logs:
            self.append_to_log(log[0], log[1])

        # WRITING
        logs = nuke_specific_functions.write_custom(custom_dict, only_selected)
        for log in logs:
            self.append_to_log(log[0], log[1])

        # RESETING NODES
        logs = nuke_specific_functions.return_to_normal(original_dict)
        for log in logs:
            self.append_to_log(log[0], log[1])