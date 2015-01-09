#!/usr/bin/python
import os
from time import gmtime, strftime
import logging

__author__ = 'Kadir Sert'
__location__ = os.path.dirname(os.path.abspath(__file__))
script_run_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.join(__location__, 'log_cleaner.out'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('')
logger.info('************************ Script Calismaya Basladi... ******************************')

try:
    qf = open(os.path.join(__location__, 'log_cleaner_properties'), 'r')
    for line in qf:
        try:
            line = ''.join(line.split())
            if line == '' or line[0] == '#':
                continue
            lc_props = line.split('|||')
            if lc_props[3] == 'delete':
                logger.info(lc_props[0] + ' - ' + lc_props[1] + ' pattern\'i kullanilarak ' + lc_props[2] + ' gunden bu yana degismemis dosyalar siliniyor!')
                logger.info(os.popen('find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2]).read())
                os.system('rm -f ' + '$(find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ')')
            if lc_props[3] == 'zip':
                logger.info(lc_props[0] + ' - ' + lc_props[1] + ' pattern\'i kullanilarak ' + lc_props[2] + ' gunden bu yana degismemis dosyalar zipleniyor!')
                log_files = os.popen('find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2]).read()
                logger.info(log_files)
                if log_files == '':
                    logger.info(lc_props[0] + ' - ' + lc_props[1] + ' pattern\'i kullanilarak log dosyasi bulunamadi!')
                    continue
                if os.path.isfile(os.path.join(__location__, 'temp_file')):
                    os.remove(os.path.join(__location__, 'temp_file'))
                temp_file = open(os.path.join(__location__, 'temp_file'), 'w')
                temp_file.write(log_files)
                temp_file.close()
                tar_file = os.path.join(os.path.dirname(lc_props[4]), script_run_time + '_' + os.path.basename(lc_props[4]))
                os.system('tar -czvf ' + tar_file + ' -T ' + os.path.join(__location__, 'temp_file'))
                if os.path.isfile(os.path.join(__location__, 'temp_file')):
                    os.remove(os.path.join(__location__, 'temp_file'))
                logger.info(lc_props[0] + ' - ' + lc_props[1] + ' pattern\'i kullanilarak ' + lc_props[2] + ' gunden bu yana degismemis dosyalar siliniyor!')
                logger.info(os.popen('find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2]).read())
                os.system('rm -f ' + '$(find ' + lc_props[0] + ' -name ' + lc_props[1] + ' -mtime +' + lc_props[2] + ')')
        except Exception, e:
            logger.error(e)
finally:
    qf.close()