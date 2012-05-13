from setuptools import setup, find_packages

setup(
	name='Grey Goo',
	version='1.1.1',
	packages=find_packages(),
	install_requires=[
		'pygame>=1.9.1',
		'numpy>=1.3',
	],
	package_data={
		'gamename': ['data/*'],
	},
	entry_points={
		'console_scripts': [
			'GreyGoo = src.main:main',
		]
	}
)
