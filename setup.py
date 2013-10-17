from setuptools import setup, find_packages
import os

version = open(os.path.join("akorn", "scrapers", "version.txt")).read().strip()

setup(name='akorn.scrapers',
      version=version,
      description="",
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Akorn',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['akorn'],
      include_package_data=True,
      package_data={'akorn.scrapers.journals': ['data/*']},
      zip_safe=False,
      install_requires=[
          'setuptools',
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)
