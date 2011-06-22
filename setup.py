from setuptools import setup, find_packages

setup(name="gpu_miner",
      version="2011.beta4",
      long_description=long_description,
      license='MIT',
      packages=['miner'],
			package_data = {
				'miner': ['*.cl']
			},
      entry_points=dict(console_scripts=['gpu_miner=miner:main', 'gpu_miner-%s=miner:main' % sys.version[:3]]),
      zip_safe=False)
