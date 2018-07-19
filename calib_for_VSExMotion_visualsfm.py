
import commands
import os
import subprocess
import sys
import shutil
import time

sys.path.append('openMVGopenMVS\\py')
import ZQ_utils

# Indicate the openMVG and openMVS binary directories
VISUALSFM_BIN = 'visualsfm'
OPENMVS_BIN = 'openMVGopenMVS'
WORK_DIR = os.path.join(os.getcwd(),'openMVGopenMVS\\tmp')


## RUN
focal = 1000;
pair_list_file = 'pair_list.txt'
argc = len(sys.argv);
if argc != 3 and argc != 4 and argc != 5:
    print 'input_dir output_dir [focal] [pair_list_file]'

input_dir = sys.argv[1]
output_dir = sys.argv[2]

time1 = time.time();
print input_dir
print output_dir
ZQ_utils.mkdir_ine(output_dir)

print 'Copy data to work directionary'
ZQ_utils.cleardir_ine(WORK_DIR)
ZQ_utils.mkdir_ine(WORK_DIR)
ZQ_utils.copy_jpg_fold_to_fold(input_dir, WORK_DIR)
        

print 'VisualSfM'
cmdline = ZQ_utils.aug_path(os.path.join(VISUALSFM_BIN,'VisualSfM.exe'))+' sfm '+ ZQ_utils.aug_path(WORK_DIR)+' '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'visualsfm.nvm'))
stats = os.system(cmdline)
if stats != 0:
    sys.exit(1);

print 'Extract pose from NVM'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'ExtractPoseFromNVM.exe'))+' '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'visualsfm.nvm'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'info.txt'))
print cmdline
os.system(cmdline)

time2 = time.time();
print 'sfm cost time: '
print time2-time1
