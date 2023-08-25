#from distutils.core import setup

#setup(name='xlpub',
#        version='1.0',
#        py_modules=['xlpub'],
#        )

import setuptools
#from setuptools import setup

with open('README.md','r') as fh:
    long_description=fh.read()
    pass

setuptools.setup(name='xlpkg',
      version='1.0.0.4',
      description='My public package',
      author='xiaolong',
      author_email='longx888@126.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='',
      packages=setuptools.find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          ],
      )
      #packages=['xlpkg'],
      #install_requires=['requests', 'numpy']

