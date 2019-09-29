# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: nuke_specific_functions.py
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

import nuke

def get_the_scene():
    scene = nuke.root().knob('name').value()
    return scene

def customize_nodes(custom_dict, only_selected_writes):

    response = []
    response.append(['-- CUSTOMIZING NODES --', 'cyan'])

    if custom_dict['scanlines']:
        for target_scanline_node in custom_dict['scanlines'].keys():

            node = nuke.toNode(target_scanline_node)

            for attr in custom_dict['scanlines'][target_scanline_node]:
                attr_value = custom_dict['scanlines'][target_scanline_node][attr]
                node[attr].setValue(attr_value)
                response.append(['ScanlineRender {0}, Attribute {1} set to {2}'.format(target_scanline_node, attr, attr_value), 'lime'])
    else:
        response.append(['INFO: No ScanlineRender nodes in the list, skipping customization step', 'orange'])


    if custom_dict['rays']:
        for target_ray_node in custom_dict['rays'].keys():

            node = nuke.toNode(target_ray_node)

            for attr in custom_dict['rays'][target_ray_node]:
                attr_value = custom_dict['rays'][target_ray_node][attr]
                node[attr].setValue(attr_value)
                response.append(['RayRender {0}, Attribute {1} set to {2}'.format(target_ray_node, attr, attr_value), 'lime'])
    else:
        response.append(['INFO: No RayRender nodes in the list, skipping customization step', 'orange'])


    if custom_dict['writes']:
        for target_write_node in custom_dict['writes'].keys():

            node = nuke.toNode(target_write_node)

            selected = custom_dict['writes'][target_write_node]['selected']

            if (not selected) and (only_selected_writes):
                response.append(['Write node {0} was not selected, will not be customized/rendered'.format(target_write_node), 'orange'])
            else:
                file_value = custom_dict['writes'][target_write_node]['file']
                node['file'].setValue(file_value)
                response.append(["Write node {0}, Attribute 'file' set to {1}".format(target_write_node, file_value), 'lime'])
    else:
        response.append(['INFO: No Write nodes in the list, skipping customization step', 'orange'])


    return response


def write_custom(custom_dict, only_selected_writes):

    response = []
    response.append(['-- WRITING --', 'cyan'])

    if custom_dict['writes']:
        for target_write_node in custom_dict['writes'].keys():

            node = nuke.toNode(target_write_node)

            frame_start = 0
            frame_end = 1
            frame_range = custom_dict['writes'][target_write_node]['range']
            if '-' in frame_range:
                frame_start = frame_range.split('-')[0]
                frame_end = frame_range.split('-')[1]
            else:
                frame_start = frame_range
                frame_end = frame_range

            selected = custom_dict['writes'][target_write_node]['selected']

            if (not selected) and (only_selected_writes):
                response.append(['Write node {0} was not selected, will not be rendered'.format(target_write_node), 'orange'])
            else:
                response.append(["STARTED Writing node {0}, for frame range {1}-{2}".format(target_write_node, frame_start, frame_end), 'fuchsia'])
                nuke.execute(target_write_node, frame_start, frame_end)
                response.append(["FINISHED Writing node {0}, for frame range {1}-{2}".format(target_write_node, frame_start, frame_end), 'fuchsia'])

    else:
        response.append(['ERROR: No valid Write nodes to write', 'red'])

    return response


def return_to_normal(original_dict):

    response = []
    response.append(['-- RESETING NODES BACK TO ORIGINAL VALUES --', 'cyan'])

    for category in original_dict.keys():

        if original_dict[category]:
            for node in original_dict[category].keys():

                n = nuke.toNode(node)

                for attribute in original_dict[category][node].keys():

                    attr_value = original_dict[category][node][attribute]
                    n[attribute].setValue(attr_value)
                    response.append(["Restored node {0} attribute {1} back to {2}".format(node,attribute, attr_value), 'lime'])
        else:
            if category == 'scanlines':
                response.append(["INFO: No ScanlineRender nodes were previously customized, skipping step", 'orange'])
            if category == 'rays':
                response.append(["INFO: No RayRender nodes were previously customized, skipping step", 'orange'])
            if category == 'writes':
                response.append(["INFO: No Write nodes were previously customized, skipping step", 'orange'])

    return response