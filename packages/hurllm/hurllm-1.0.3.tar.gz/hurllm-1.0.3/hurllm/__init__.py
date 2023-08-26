from .core import *

def __compile_core():
    try:
        from os import environ, path, listdir, rename, remove
        if 'COLAB_GPU' not in environ and 'KAGGLE_KERNEL_RUN_TYPE' not in environ:
            from shutil import move
            dir_path = path.dirname(path.realpath(__file__))
            dir_path = dir_path.replace('\\', '/')
            dir_path += '/'
            if not path.exists(dir_path+'core.pyc'):
                pycache_dir = dir_path+'__pycache__/'
                for filename in listdir(pycache_dir):
                    if filename.startswith('core'):
                        move(pycache_dir+filename, dir_path+filename)
                        rename(dir_path+filename, dir_path+'core.pyc')
                        remove(dir_path+'core.py')
                        break
    except: pass
__compile_core()
