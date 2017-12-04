#!/usr/bin/env python

import sys
import imp
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

modules = []
for n in os.listdir(dir_path + "/" + "lib"):
    extension = n.split('.').pop()
    if (extension == ".py" and 'init' not in name):
        modules.append(imp.load_source(n, dir_path + "/" + "lib" + "/" + n))


def get_lib_func_output(input):
    for m in modules:
         if 'libliblib' in str(m):      
             return m.func(input)
   
