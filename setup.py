import sys
from setuptools import setup, find_packages

setup(name="gpu_miner",
      version="2011.beta4",
      packages=['miner'],
			package_data = { 'miner': ['kernel.cl'] },
      entry_points=dict(console_scripts=['gpu_miner=miner:main', 'gpu_miner-%s=miner:main' % sys.version[:3]]),
			# install_requires = ['pyopencl==2011.1beta3', 'pycrypto>=2.3', 'jsonrpc>=0.99a01'],
			# setup_requires= ['numpy>=1.6.0'],
      zip_safe=False)
