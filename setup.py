from setuptools import setup, find_packages

setup(
	name="bitcoin-gpu-miner",
	version="2011.beta4",
	scripts = ['poclbm.py'],
	install_requires = ['numpy>=1.6.0','pyopencl>=2011.1beta3', 'pycrypto>=2.3', 'jsonrpc>=0.99a01'],
	package_data = {
		'': ['*.cl']
	}	
)
	