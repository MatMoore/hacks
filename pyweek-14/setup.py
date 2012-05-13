from setuptools import setup, find_packages

setup(
	name='Grey Goo',
	version='1.1.2',
	packages=find_packages(),
	install_requires=[
		'pygame>=1.9.1',
		'numpy>=1.3',
	],
	package_data={
		'src': ['data/*'],
	},
	entry_points={
		'console_scripts': [
			'greygoo = src.__main__:main',
		]
	}
)
