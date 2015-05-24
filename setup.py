__author__ = 'Toyz'

from distutils.core import setup
import py2exe

from distutils.core import setup
import py2exe
import sys

sys.path.append("C:\\Windows\\WinSxS\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91")
Mydata_files = [('interface', ['C:\Users\Travis\IdeaProjects\IMVU CFL Reader\interface\main.ui']),
                (".", ["C:\\Windows\\WinSxS\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\\msvcp90.dll"])]

setup(windows=[{"script":"main_gui.py"}], options={"py2exe":{"includes":["sip"]}}, data_files=Mydata_files)
