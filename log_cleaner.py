#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from time import localtime, strftime
import logging
import argparse

__author__ = 'Kadir Sert'
script_run_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
__location__ = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(__location__, 'logs')
tempdir = os.path.join(__location__, 'temp')
props_file_name = 'lc_props'
is_test_mode = False
os.chdir(__location__)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--props", help="For custom properties file. Default value: lc_props", default="lc_props")
parser.add_argument("-t", "--test", help="Test the properties file and not apply the rules.", action="store_true")
args = parser.parse_args()

if args.props:
    props_file_name = args.props
props_file_path = os.path.join(__location__, props_file_name)
if args.test:
    is_test_mode = True
    test_log_path = os.path.join(logdir, props_file_name + '.testout')
    if os.path.isfile(test_log_path):
        os.remove(test_log_path)
    handler = logging.FileHandler(test_log_path)
else:
    log_path = os.path.join(logdir, props_file_name + '.out')
    handler = logging.FileHandler(log_path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('')
logger.info('****************** Script Started. Using ' + props_file_path + ' file! ************************')

props_file = open(props_file_path, 'r')
for line in props_file:
    try:
        line = ''.join(line.split())
        if line == '' or line[0] == '#':
            continue
        lc_props = line.split('|||')
        if lc_props[3] == 'delete':
            lc_message = 'Deleting file(s): ' + lc_props[0] + ' - ' + lc_props[1] + ' -mtime: ' + lc_props[2]
            logger.info(lc_message)
            lc_command = 'find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ' -type f'
            lc_message = os.popen(lc_command).read()
            logger.info(lc_message)
            lc_command = 'rm -f ' + '$(find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ' -type f' + ')'
            if not is_test_mode:
                os.system(lc_command)
        if lc_props[3] == 'zip':
            lc_message = 'Compressing file(s): ' + lc_props[0] + ' - ' + lc_props[1] + ' -mtime: ' + lc_props[2]
            logger.info(lc_message)
            lc_command = 'find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ' -type f'
            log_files = os.popen(lc_command).read()
            logger.info(log_files)
            if log_files == '':
                lc_message = lc_props[0] + ' - ' + lc_props[1] + ' file(s) not found!'
                logger.info(lc_message)
                continue
            if not is_test_mode:
                if os.path.isfile(os.path.join(tempdir, props_file_name + '_temp_file')):
                    os.remove(os.path.join(tempdir, props_file_name + '_temp_file'))
                temp_file = open(os.path.join(tempdir, props_file_name + '_temp_file'), 'w')
                temp_file.write(log_files)
                temp_file.close()
            tar_file = os.path.join(os.path.dirname(lc_props[4]), script_run_time + '_' + os.path.basename(lc_props[4]))
            lc_command = 'tar -czvf ' + tar_file + ' -T ' + os.path.join(tempdir, props_file_name + '_temp_file')
            if not is_test_mode:
                os.system(lc_command)
                if os.path.isfile(os.path.join(tempdir, props_file_name + '_temp_file')):
                    os.remove(os.path.join(tempdir, props_file_name + '_temp_file'))
            lc_message = 'Deleting file(s): ' + lc_props[0] + ' - ' + lc_props[1] + ' -mtime: ' + lc_props[2]
            logger.info(lc_message)
            lc_command = 'find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ' -type f'
            lc_message = os.popen(lc_command).read()
            logger.info(lc_message)
            lc_command = 'rm -f ' + '$(find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ' -type f' + ')'
            if not is_test_mode:
                if os.path.isfile(tar_file):
                    os.system(lc_command)
    except Exception, e:
        logger.error(e)
props_file.close()
