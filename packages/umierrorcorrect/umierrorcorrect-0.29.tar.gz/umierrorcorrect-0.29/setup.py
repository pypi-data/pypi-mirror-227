#!/usr/bin/env python3
from setuptools import setup
from setuptools import find_packages

pack = find_packages() 

install_requires = ["pysam>=0.8.4","scipy","matplotlib"]

exec(open('umierrorcorrect/version.py').read())

setup(name='umierrorcorrect',
      version=__version__,
      description='UMI error correct',
      long_description = open('README.md').read(),
      url='http://github.com/stahlberggroup/umierrorcorrect',
      author='Tobias Osterlund',
      author_email='tobias.osterlund@gu.se',
      download_url = 'https://github.com/stahlberggroup/umierrorcorrect/archive/'+ __version__ +'.tar.gz', 
      packages=pack,
      license='mit',
      package_data={'umierrorcorrect': ['README.md']
                   },
      include_package_data=True,
      install_requires=install_requires,
      classifiers=['Topic :: Scientific/Engineering :: Bio-Informatics'],
      scripts=['umierrorcorrect/run_umierrorcorrect.py',
                'umierrorcorrect/preprocess.py',
                'umierrorcorrect/run_mapping.py',
                'umierrorcorrect/umi_error_correct.py',
                'umierrorcorrect/get_consensus_statistics.py',
                'umierrorcorrect/call_variants.py',
                'umierrorcorrect/filter_bam.py',
                'umierrorcorrect/filter_cons.py',
                'umierrorcorrect/downsampling_plots.py',
                'umierrorcorrect/fit_background_model.py'],
      zip_safe=False)
