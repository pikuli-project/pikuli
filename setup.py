#!/usr/bin/env python

from setuptools import setup, find_packages
from shutil import copyfile
from distutils.sysconfig import get_python_lib
from os import path, listdir
from sys import maxsize
from platform import system
import subprocess


def package_env(file_name, strict=False):
    file_path = path.join(path.dirname(__file__), file_name)
    if path.exists(file_path) or strict:
        return open(file_path).read()
    else:
        return ''

if __name__ == '__main__':
    lib_path = get_python_lib()

    if system() == 'Windows':
        install_requires = ['numpy', 'psutil', 'pypiwin32', 'comtypes', 'pillow']
        bitness = 'x64' if maxsize > 2**32 else 'x86'
        current_dir = path.dirname(path.abspath(__file__))
        copyfile(path.join(current_dir, 'Pikuli', 'opencv', 'windows', bitness, 'cv2.pyd'),
                 path.join(lib_path, 'cv2.pyd'))
    elif system() == 'Darwin':
        install_requires = ['numpy', 'psutil', 'pyobjc-framework-Quartz', 'pillow']

        opencv_dir = '/usr/local/Cellar/opencv'
        cv_version = max(listdir(opencv_dir))
        cv_path = path.join(opencv_dir, cv_version, 'lib/python2.7/site-packages/')
        copyfile(path.join(cv_path, 'cv.py'), path.join(lib_path, 'cv.py'))
        copyfile(path.join(cv_path, 'cv2.so'), path.join(lib_path, 'cv2.so'))
    else:
        install_requires = []

    setup(
        name='Pikuli',
        version='1.1.17',
        description='Cross Platform GUI Test Automation tool.',
        long_description=package_env('README.rst'),
        author='Nikita Voronchev, Roman Bukharov',
        author_email='pikuli.gui.automation@gmail.com',
        packages=['Pikuli'] + ['.'.join(('pikuli', p)) for p in
                               find_packages('pikuli')],
        include_package_data=True,
        install_requires=install_requires,
        zip_safe=False
    )
