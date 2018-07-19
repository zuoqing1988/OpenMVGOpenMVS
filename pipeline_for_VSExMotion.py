
import commands
import os
import subprocess
import sys
import time

sys.path.append('openMVGopenMVS\\py')
import ZQ_utils

# Indicate the openMVG and openMVS binary directories
OPENMVG_BIN = "openMVGopenMVS"
OPENMVS_BIN = "openMVGopenMVS"
WORK_DIR = os.path.join(os.getcwd(),'openMVGopenMVS\\tmp')
MESHLAB_DIR = 'C:\\Program Files\\VCG\\MeshLab'
config_for_vse_file = os.path.join(OPENMVG_BIN,'config_for_vse.txt')
matches_dir = os.path.join(WORK_DIR,'matches')
reconstruction_dir = os.path.join(WORK_DIR,'sfm')
mvs_dir = os.path.join(WORK_DIR,'mvs')
exiv2_exe_name = os.path.join(OPENMVG_BIN,'exiv2.exe')
ImageResize_exe_name = os.path.join(OPENMVG_BIN,'ImageResize.exe')
copy_and_resize_exe_name = os.path.join(OPENMVG_BIN,'copy_and_resize_fold_to_fold')

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
ZQ_utils.mkdir_ine(matches_dir)
ZQ_utils.mkdir_ine(reconstruction_dir)
ZQ_utils.mkdir_ine(mvs_dir)

time00 = time.time()
#ZQ_utils.copy_jpg_fold_to_fold(input_dir, WORK_DIR)
#ZQ_utils.copy_jpg_fold_to_fold_and_resize(exiv2_exe_name, ImageResize_exe_name,input_dir, WORK_DIR, '1920')
if not ZQ_utils.copy_jpg_fold_to_fold_and_resize_multi_thread(copy_and_resize_exe_name,exiv2_exe_name, ImageResize_exe_name,input_dir, WORK_DIR, '1920','10'):
    print 'fail'
    sys.exit(1);
time01 = time.time()
print 'copy_and_resize cost: '
print time01-time00

print 'Run SFM PIPELINE'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_pipeline_for_VSExMotion.exe'))+' '+ZQ_utils.aug_path(config_for_vse_file)
stats = os.system(cmdline)
if stats != 0:
    sys.exit(1);

print 'Copy SFM result to output_dir'
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'sfm_data.ply'))
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

print 'Export to openMVS'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVG_BIN,'openMVG_main_openMVG2openMVS.exe'))+ ' -i '+ZQ_utils.aug_path(os.path.join(reconstruction_dir,'sfm_data.bin'))+' -o '+ZQ_utils.aug_path(os.path.join(mvs_dir,'scene.mvs'))+' -d '+ZQ_utils.aug_path(mvs_dir)
print cmdline
os.system(cmdline)

print 'Densify point cloud'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'DensifyPointCloud.exe'))+' -i scene.mvs -o scene_dense.mvs -w '+ZQ_utils.aug_path(mvs_dir) +' --resolution-level=2 --min-resolution=640'
print cmdline
os.system(cmdline)

                   
print 'Reconstruct the mesh'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'ReconstructMesh.exe'))+' -i scene_dense.mvs -o scene_dense_mesh.mvs -w '+ZQ_utils.aug_path(mvs_dir)
print cmdline
os.system(cmdline)

print 'Refine the mesh'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'RefineMesh.exe'))+' -i scene_dense_mesh.mvs -o scene_dense_mesh_refine.mvs -w '+ZQ_utils.aug_path(mvs_dir)+' --resolution-level=2 --min-resolution=640 --max-views=6 --reduce-memory=0'
print cmdline
os.system(cmdline)

print 'Texture the mesh'
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'TextureMesh.exe'))+' -i scene_dense_mesh_refine.mvs -o texture_mesh.ply -w '+ZQ_utils.aug_path(mvs_dir)+' --empty-color=0'
print cmdline
os.system(cmdline)


print 'Convert ply to obj'
cmdline = ZQ_utils.aug_path(os.path.join(MESHLAB_DIR,'meshlabserver.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.ply'))+' -o '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj'))+' -m wt'
print cmdline
os.system(cmdline)


print 'Copy to output_dir'
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.ply'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.png'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.png'))
print cmdline
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj'))
print cmdline
os.system(cmdline)

cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(mvs_dir,'texture_mesh.obj.mtl'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj.mtl'))
print cmdline
os.system(cmdline)

time3 = time.time()
print 'MVS cost time: '
print time3-time2

print 'Done! total cost time: '
print time3-time1
