from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
]

flake8_entry_point = 'flake8.extension'

setuptools.setup(
    name="flake8_pep666_team_6",
    license="MIT",
    version="0.1.0",
    description="our extension to flake8",
    author="Team 6",
    author_email="example@example.com",
    url="https://gitlab.com/me/flake8_example",
    packages=[
        "flake8_pep666_team_6",
    ],
    install_requires=requires,
    entry_points={
        flake8_entry_point: [
            'X6 = flake8_pep666_team_6:Linter',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
