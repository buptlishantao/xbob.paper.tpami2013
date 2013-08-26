#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:54:13 CEST 2013
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(

    name='xbob.paper.tpami2013',
    version='0.3.0a1',
    description='Example on how to use the scalable implementation of PLDA and how to reproduce experiments of the article',
    url='http://pypi.python.org/pypi/xbob.paper.tpami2013',
    license='GPLv3',
    author='Laurent El Shafey',
    author_email='Laurent.El-Shafey@idiap.ch',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=[
      'setuptools',
      'bob >= 1.2.0',
      'xbob.db.multipie',
      'xbob.db.verification.filelist',
      'six',  # py2/3 compatibility library
      'gridtk',
    ],

    entry_points={
      'console_scripts': [
        'plda_example_iris.py = xbob.paper.tpami2013.scripts.plda_example_iris:main',
        'lbph_extraction.py = xbob.paper.tpami2013.scripts.lbph_extraction:main',
        'lbph_features.py = xbob.paper.tpami2013.scripts.lbph_features:main',
        'pca_train.py = xbob.paper.tpami2013.scripts.pca_train:main',
        'lda_train.py = xbob.paper.tpami2013.scripts.lda_train:main',
        'linear_project.py = xbob.paper.tpami2013.scripts.linear_project:main',
        'pca_features.py = xbob.paper.tpami2013.scripts.pca_features:main',
        'plda_train.py = xbob.paper.tpami2013.scripts.plda_train:main',
        'plda_enroll.py = xbob.paper.tpami2013.scripts.plda_enroll:main',
        'plda_scores.py = xbob.paper.tpami2013.scripts.plda_scores:main',
        'concatenate_scores.py = xbob.paper.tpami2013.scripts.concatenate_scores:main',
        'toolchain_plda.py = xbob.paper.tpami2013.scripts.toolchain_plda:main',
        'experiment_plda_subworld.py = xbob.paper.tpami2013.scripts.experiment_plda_subworld:main',
        'plot_figure2.py = xbob.paper.tpami2013.scripts.plot_figure2:main',
        'meanmodel_enroll.py = xbob.paper.tpami2013.scripts.meanmodel_enroll:main',
        'distance_scores.py = xbob.paper.tpami2013.scripts.distance_scores:main',
        'toolchain_lbph.py = xbob.paper.tpami2013.scripts.toolchain_lbph:main',
        'toolchain_lda.py = xbob.paper.tpami2013.scripts.toolchain_lda:main',
        'toolchain_pca.py = xbob.paper.tpami2013.scripts.toolchain_pca:main',
        'plot_table3.py = xbob.paper.tpami2013.scripts.plot_table3:main',
        'lfw_features.py = xbob.paper.tpami2013.scripts.lfw_features:main',
        'toolchain_pcaplda.py = xbob.paper.tpami2013.scripts.toolchain_pcaplda:main',
        'experiment_pcaplda_lfw.py = xbob.paper.tpami2013.scripts.experiment_pcaplda_lfw:main',
        'plot_table2.py = xbob.paper.tpami2013.scripts.plot_table2:main',
        ],
      },

    namespace_packages = [
      'xbob',
      'xbob.paper',
    ],

    classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Education',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
