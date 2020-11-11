from setuptools import setup

setup(name='gomc-wrapper',
      version='0.01',
      description='GPU Optimized Monte Carlo (GOMC) Python wrapper',
      url='http://github.com/evenmn/gomc-wrapper',
      author='Even Marius Nordhagen',
      author_email='evenmn@fys.uio.no',
      license='MIT',
      packages=['gomc_wrapper'],
      include_package_data=True,
      zip_safe=False)
