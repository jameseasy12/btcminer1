from distutils.core import setup
import py2exe

setup(windows=['guiminer.py'],
      console=['poclbm.py'],
      # OpenCL.dll is vendor specific
      options=dict(py2exe=dict(
          dll_excludes=['OpenCL.dll'],
          #bundle_files=1,
          compressed=True,
          optimize=2,
          excludes = ["Tkconstants", "Tkinter", "tcl"],
      )), 
      data_files = ['msvcp90.dll',
                    'BitcoinMiner.cl',
                    'logo.ico',
                    'LICENSE.txt',
                    'servers.ini',
                    'defaults.ini'])