
import commands
import os
import subprocess
import sys
import shutil
import time

sys.path.append('openMVGopenMVS\\py')
import ZQ_utils

# Indicate the openMVG and openMVS binary directories
OPENMVG_BIN = "openMVGopenMVS"
WORK_DIR = os.path.join(os.getcwd(),'openMVGopenMVS\\tmp')
config_for_vse_file = os.path.join(OPENMVG_BIN,'config_for_vse_calib.txt')
matches_dir = os.path.join(WORK_DIR,'matches')
reconstruction_dir = os.path.join(WORK_DIR,'sfm')

## RUN
focal = 1000;
pair_list_file = 'pair_list.txt'
argc = len(sys.argv);
if argc != 3:
    print 'input_dir output_dir '

input_dir = sys.argv[1]
output_dir = sys.argv[2]
backup_dir = os.path.join(output_dir,'backup')

time1 = time.time();
print input_dir
print output_dir
print backup_dir
ZQ_utils.mkdir_ine(output_dir)
ZQ_utils.mkdir_ine(backup_dir)

print 'Copy data to work directionary'
ZQ_utils.cleardir_ine(WORK_DIR)
ZQ_utils.mkdir_ine(WORK_DIR)
ZQ_utils.mkdir_ine(matches_dir)
ZQ_utils.mkdir_ine(reconstruction_dir)
ZQ_utils.copy_jpg_fold_to_fold(input_dir, WORK_DIR)
        

print 'Run SFM PIPELINE'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_pipeline_for_VSExMotion.exe'))+' '+ZQ_utils.aug_path(config_for_vse_file)
stats = os.system(cmdline)
if stats != 0:
    sys.exit(1);

print 'Copy SFM result to output_dir'
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'sfm_data.ply'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.bin'))+' '+ZQ_utils.aug_path(os.path.join(backup_dir,'sfm_data.bin'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'Reconstruction_Report.html'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'Reconstruction_Report.html'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'residuals_histogram.svg'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'residuals_histogram.svg'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'SfMReconstruction_Report.html'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'SfMReconstruction_Report.html'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'cam_info.txt'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'info.txt'))
print cmdline
os.system(cmdline)

time2 = time.time();
print 'sfm cost time: '
print time2-time1
