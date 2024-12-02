import os
import sys
import shutil
import time

sys.path.append('openMVGopenMVS\\py')
import ZQ_utils

# Indicate the openMVG and openMVS binary directories
VISUALSFM_BIN = 'visualsfm'
OPENMVS_BIN = 'openMVGopenMVS'
WORK_DIR = os.path.join(os.getcwd(),'openMVGopenMVS\\tmp')
MESHLAB_DIR = 'C:\\Program Files\\VCG\\MeshLab'
   

## RUN
if len(sys.argv) != 3:
    print('input_dir output_dir')

time1 = time.time()
input_dir = sys.argv[1].replace('/','\\')
output_dir = sys.argv[2].replace('/','\\')
print(input_dir)
print(output_dir)
ZQ_utils.mkdir_ine(output_dir)

print('Copy data to work directionary')
ZQ_utils.cleardir_ine(WORK_DIR)
ZQ_utils.mkdir_ine(WORK_DIR)
ZQ_utils.copy_jpg_fold_to_fold(input_dir, WORK_DIR)
        

print('VisualSfM')
cmdline = ZQ_utils.aug_path(os.path.join(VISUALSFM_BIN,'VisualSfM.exe'))+' sfm+shared+sort '+ ZQ_utils.aug_path(WORK_DIR)+' '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'visualsfm.nvm'))
print(cmdline)
os.system(cmdline)

time2 = time.time()
print('visual sfm cost time: %f'%(time2-time1))

print('Extract pose from NVM')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'ExtractPoseFromNVM.exe'))+' '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'visualsfm.nvm'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'info.txt'))
print(cmdline)
os.system(cmdline)


print('InterfaceVisualSfM')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'InterfaceVisualSfM'))+' -i visualsfm.nvm -o scene.mvs -w '+ZQ_utils.aug_path(WORK_DIR)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Densify point cloud')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'DensifyPointCloud.exe'))+' -i scene.mvs -o scene_dense.mvs -w '+ZQ_utils.aug_path(WORK_DIR)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Reconstruct the mesh')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'ReconstructMesh.exe'))+' -i scene_dense.mvs -o scene_dense_mesh.mvs -w '+ZQ_utils.aug_path(WORK_DIR)
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print("Refine the mesh")
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'RefineMesh.exe'))+' -i scene_dense_mesh.mvs -o scene_dense_mesh_refine.mvs -w '+ZQ_utils.aug_path(WORK_DIR)+' --resolution-level=2 --min-resolution=1280'
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Texture the mesh')
cmdline = ZQ_utils.aug_path(os.path.join(OPENMVS_BIN,'TextureMesh.exe'))+' -i scene_dense_mesh_refine.mvs -o texture_mesh.ply -w '+ZQ_utils.aug_path(WORK_DIR)+' --empty-color=0'
print(cmdline)
stats = os.system(cmdline)
if stats != 0:
    print('fail!\n')
    sys.exit(1);

print('Convert ply to obj')
cmdline = ZQ_utils.aug_path(os.path.join(MESHLAB_DIR,'meshlabserver.exe'))+' -i '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.ply'))+' -o '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.obj'))+' -m wt'
print(cmdline)
os.system(cmdline)


print('Copy to output_dir')
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.ply'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.ply'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.png'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.png'))
print(cmdline)
os.system(cmdline)
cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.obj'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj'))
print(cmdline)
os.system(cmdline)

cmdline = 'copy '+ZQ_utils.aug_path(os.path.join(WORK_DIR,'texture_mesh.obj.mtl'))+' '+ZQ_utils.aug_path(os.path.join(output_dir,'texture_mesh.obj.mtl'))
print(cmdline)
os.system(cmdline)

time3 = time.time()
print('openMVS cost time: %f'%(time3-time2))
print('Done! total cost time: %f'%(time3-time1))
