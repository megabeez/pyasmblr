from setuptools import setup,find_packages
import os
os.system('pip install -r requirements.txt')
setup(
	name='pyasmblr',
	version='1.0',
	description='Simple Assembler',
	url='https://github.com/megabeez/pyasmblr',
	author='Behzad',
	author_email='behzadghat@gmail.com',
	zip_safe=False
	)
