#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import localtime, strftime
import logging

__author__ = 'Kadir Sert'
__location__ = os.path.dirname(os.path.abspath(__file__))
script_run_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
if len(sys.argv) == 1:
    is_test_mode = False
elif len(sys.argv) == 2 and sys.argv[1] == 'test':
    is_test_mode = True
    if os.path.isfile(os.path.join(__location__, 'log_cleaner_test.out')):
        os.remove(os.path.join(__location__, 'log_cleaner_test.out'))
else:
    print 'Invalid Argument !!!'
    sys.exit()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if is_test_mode:
    handler = logging.FileHandler(os.path.join(__location__, 'log_cleaner_test.out'))
else:
    handler = logging.FileHandler(os.path.join(__location__, 'log_cleaner.out'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('')
logger.info('************************ Script Started... ******************************')

props_file = open(os.path.join(__location__, 'log_cleaner_properties'), 'r')
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
                if os.path.isfile(os.path.join(__location__, 'temp_file')):
                    os.remove(os.path.join(__location__, 'temp_file'))
                temp_file = open(os.path.join(__location__, 'temp_file'), 'w')
                temp_file.write(log_files)
                temp_file.close()
            tar_file = os.path.join(os.path.dirname(lc_props[4]), script_run_time + '_' + os.path.basename(lc_props[4]))
            lc_command = 'tar -czvf ' + tar_file + ' -T ' + os.path.join(__location__, 'temp_file')
            if not is_test_mode:
                os.system(lc_command)
                if os.path.isfile(os.path.join(__location__, 'temp_file')):
                    os.remove(os.path.join(__location__, 'temp_file'))
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
