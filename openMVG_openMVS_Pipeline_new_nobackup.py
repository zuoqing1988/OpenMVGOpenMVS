import os
import sys
import shutil
import time

sys.path.append('openMVGopenMVS\\py')
import ZQ_utils

# Indicate the openMVG and openMVS binary directories
OPENMVG_BIN = "openMVGopenMVS"
OPENMVS_BIN = "openMVGopenMVS"
WORK_DIR = os.path.join(os.getcwd(),'openMVGopenMVS\\tmp')
MESHLAB_DIR = 'C:\\Program Files\\VCG\\MeshLab'
CAMERA_SENSOR_WIDTH_DIRECTORY = OPENMVG_BIN
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY,'sensor_width_camera_database.txt')
matches_dir = os.path.join(WORK_DIR,'matches')
reconstruction_dir = os.path.join(WORK_DIR,'reconstruction')
mvs_dir = os.path.join(WORK_DIR,'mvs')

## RUN
focal = 1000;
pair_list_file = 'pair_list.txt'
argc = len(sys.argv);
if argc != 3 and argc != 4 and argc != 5:
    print('input_dir output_dir [focal] [pair_list_file]')

time1 = time.time()
input_dir = sys.argv[1].replace('/','\\')
output_dir = sys.argv[2].replace('/','\\')

use_focal = 0
if argc >= 4:
    use_focal = 1
    focal = sys.argv[3];
use_pair_list = 0
if argc >= 5:
    use_pair_list = 1
    pair_list_file = os.path.join(input_dir,sys.argv[4]);

print(input_dir)
print(output_dir)
ZQ_utils.mkdir_ine(output_dir)

print('Copy data to work directionary')
ZQ_utils.cleardir_ine(WORK_DIR)
ZQ_utils.mkdir_ine(WORK_DIR)
ZQ_utils.copy_jpg_fold_to_fold(input_dir, WORK_DIR)
        
print('Intrinsics analysis')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_SfMInit_ImageListing.exe'))+' -i '+ZQ_utils.aug_path(input_dir)+' -o '+ZQ_utils.aug_path(matches_dir) + ' -d '+ ZQ_utils.aug_path(camera_file_params)+' -g 0 -c 2'
if use_focal:
    cmdline = cmdline+' -f '+focal
print(cmdline)
os.system(cmdline)

print('Compute features')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_ComputeFeatures.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(matches_dir,'sfm_data.json'))+' -o '+ZQ_utils.aug_path(matches_dir)+ ' -m SIFT -n 8 -p HIGH -a -l 8192'
print(cmdline)
os.system(cmdline)

print('Compute matches')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN, 'openMVG_main_ComputeMatches.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(matches_dir,'sfm_data.json'))+' -o '+ZQ_utils.aug_path(matches_dir)+' -r 0.8 -n ANNL2 -I 5000'
if use_pair_list:
    cmdline = cmdline + ' -l '+ZQ_utils.aug_path(pair_list_file)
print(cmdline)
os.system(cmdline)

print('Incremental reconstruction')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN, 'openMVG_main_IncrementalSfM.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(matches_dir,'sfm_data.json'))+' -m '+ZQ_utils.aug_path(matches_dir)+ ' -o '+ZQ_utils.aug_path(reconstruction_dir)+' -r 2 -s 0.75 -c 2 -f "ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION"'
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1)

print('Colorize Structure')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_ComputeSfM_DataColor.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.bin'))+ ' -o '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'colorized.ply'))
print(cmdline)
os.system(cmdline)

print('Structure from Known Poses')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_ComputeStructureFromKnownPoses.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.bin'))+ ' -m '+ZQ_utils.aug_path(matches_dir)+' -f '+ZQ_utils.aug_path(os.path.join(matches_dir,'matches.f.bin'))+' -o '+ ZQ_utils.aug_path(os.path.join(reconstruction_dir,'robust.bin'))
print(cmdline)
os.system(cmdline)

print('Colorized robust triangulation')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_ComputeSfM_DataColor.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'robust.bin'))+ ' -o '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'robust_colorized.ply'))
print(cmdline)
os.system(cmdline)

print('Copy SFM result to output_dir')
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'colorized.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'colorized.ply'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'Reconstruction_Report.html'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'Reconstruction_Report.html'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'residuals_histogram.svg'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'residuals_histogram.svg'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'SfMReconstruction_Report.html'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'SfMReconstruction_Report.html'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'SfMStructureFromKnownPoses_Report.html'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'SfMStructureFromKnownPoses_Report.html'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'cam_info.txt'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'info.txt'))
print(cmdline)
os.system(cmdline)

time2 = time.time()
print('openMVG cost time: %f'%(time2-time1))

print('Export to openMVS')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_openMVG2openMVS.exe'))+ ' -i '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'robust.bin'))+' -o '+ZQ_utils.aug_path(os.path.join(mvs_dir,'scene.mvs'))+' -d '+ZQ_utils.aug_path(mvs_dir)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Densify point cloud')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'DensifyPointCloud.exe'))+' -i scene.mvs -o scene_dense.mvs -w '+ZQ_utils.aug_path(mvs_dir)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

                   
print('Reconstruct the mesh')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'ReconstructMesh.exe'))+' -i scene_dense.mvs -o scene_dense_mesh.mvs -w '+ZQ_utils.aug_path(mvs_dir)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Refine the mesh')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'RefineMesh.exe'))+' -i scene_dense_mesh.mvs -o scene_dense_mesh_refine.mvs -w '+ZQ_utils.aug_path(mvs_dir)+' --resolution-level=2 --min-resolution=1280'
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Texture the mesh')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'TextureMesh.exe'))+' -i scene_dense_mesh_refine.mvs -o texture_mesh.ply -w '+ZQ_utils.aug_path(mvs_dir)+' --empty-color=0'
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);


print('Convert ply to obj')
cmdline = ZQ_utils.aug_path(os.path.join(MESHLAB_DIR,'meshlabserver.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.ply'))+' -o '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj'))+' -m wt'
print(cmdline)
os.system(cmdline)



print('Copy to output_dir')
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.ply'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.png'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.png'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj'))
print(cmdline)
os.system(cmdline)

cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj.mtl'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj.mtl'))
print(cmdline)
os.system(cmdline)

time3 = time.time()
print('openMVS cost time: %f'%(time3-time2))
print('Done! total cost time: %f'%(time3-time1))
