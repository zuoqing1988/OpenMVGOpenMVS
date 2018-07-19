
import os
import re 
import shutil
import threading
import multiprocessing

def exists2(dirname):
    dirlist = re.findall(r'.+?(?=\\)',str(dirname))
    path = '';
    for dir in dirlist :
        path = path+dir
        if not os.path.exists(path):
            return False
    return os.path.exists(dirname)

def mkdir_ine(dirname):
    """Create the folder if not presents"""
    if not exists2(dirname):
        os.makedirs(dirname)
        print dirname

def cleardir_ine(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return 
    """Clear the folder"""
    filelist=[]
    filelist=os.listdir(dirname)
    for f in filelist:
        filepath = os.path.join( dirname, f )
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath+" removed!"
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath,True)
            print "dir "+filepath+" removed!"

def aug_path(path):
    flag = 0
    for i in path:
        if i.isspace():
            flag = 1
    if flag == 1:
        return '"'+path+'"'
    else:
        return path

def copy_jpg_fold_to_fold(src_fold, dst_fold):
    files = os.listdir(src_fold)
    file_num = len(files)
    for i in range (file_num):
        suffix = os.path.splitext(files[i])[1]
        if suffix.lower() == '.jpg'.lower():
            cmdline = 'copy /Y '+aug_path(os.path.join(src_fold,files[i]))+' '+aug_path(os.path.join(dst_fold,files[i]))
            print cmdline
            os.system(cmdline)

def copy_and_resize_one_thread(exiv2_name,ImageResize_name,src_name,dst_name,max_dim):
        cmdline = 'copy /Y '+aug_path(src_name)+' '+aug_path(dst_name)
        print cmdline
        os.system(cmdline)
        if not extract_exif_of_image(exiv2_name, dst_name):
            if not image_resize(ImageResize_name,dst_name,dst_name,max_dim):
                return False
        else:
            if not image_resize(ImageResize_name,dst_name,dst_name,max_dim):
                return False
            insert_exif_of_image(exiv2_name,dst_name)
        return True

def copy_jpg_fold_to_fold_and_resize(exiv2_name, ImageResize_name, src_fold, dst_fold, max_dim):
    files = os.listdir(src_fold)
    file_num = len(files)
    for i in range (file_num):
        name_vec = os.path.splitext(files[i])
        base_name = name_vec[0]
        suffix = name_vec[1]
        if suffix.lower() == '.jpg'.lower():
            src_name = os.path.join(src_fold,files[i])
            dst_name = os.path.join(dst_fold,files[i])
            if not copy_and_resize_one_thread(exiv2_name, ImageResize_name, src_name, dst_name, max_dim):
                return False
    return True

def copy_jpg_fold_to_fold_and_resize_multi_thread(copy_and_resize_name, exiv2_name, ImageResize_name, src_fold, dst_fold, max_dim, nthreads):
    cmdline = aug_path(copy_and_resize_name) + ' ' + aug_path(exiv2_name) + ' '+aug_path(ImageResize_name) +' '+aug_path(src_fold) + ' '+dst_fold +' ' +max_dim + ' '+nthreads
    stats = os.system(cmdline)
    if stats != 0:
        return False
    return True

def extract_exif_of_image(exe_name, img_name):
    base_name = os.path.splitext(img_name)[0]
    dst_name = base_name+'.exv'
    if exists2(dst_name) :
        os.remove(dst_name)
    cmdline = exe_name+' ex '+img_name
    stats = os.system(cmdline)
    if stats != 0:
        return False
    else:
        file_size = os.stat(dst_name)
        if file_size.st_size <= 9:
            return False
        return True
         
def insert_exif_of_image(exe_name, img_name):
    base_name = os.path.splitext(img_name)[0]
    dst_name = base_name+'.exv'
    if not exists2(dst_name):
        return False
    cmdline = exe_name+' in '+img_name;
    stats = os.system(cmdline)
    if stats != 0:
        return False
    else :
        return True
         
def image_resize(exe_name, src_name, dst_name, max_dim):
     cmdline = exe_name+' '+src_name+' '+dst_name+' ' + max_dim
     stats = os.system(cmdline)
     if stats != 0:
         return False
     else :
         return True