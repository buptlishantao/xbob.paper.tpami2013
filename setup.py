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
    version='0.1.0a1',
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
      'gridtk',
    ],

    entry_points={
      'console_scripts': [
        'plda_example_iris.py = xbob.paper.tpami2013.scripts.plda_example_iris:main',
        'lbph_features.py = xbob.paper.tpami2013.scripts.lbph_features:main',
        'pca_train.py = xbob.paper.tpami2013.scripts.pca_train:main',
        'pca_project.py = xbob.paper.tpami2013.scripts.pca_project:main',
        'pca.py = xbob.paper.tpami2013.scripts.pca:main',
        'plda_train.py = xbob.paper.tpami2013.scripts.plda_train:main',
        'plda_enroll.py = xbob.paper.tpami2013.scripts.plda_enroll:main',
        'plda_scores.py = xbob.paper.tpami2013.scripts.plda_scores:main',
        'concatenate_scores.py = xbob.paper.tpami2013.scripts.concatenate_scores:main',
        'plda.py = xbob.paper.tpami2013.scripts.plda:main',
        'plda_subworld.py = xbob.paper.tpami2013.scripts.plda_subworld:main',
        'plot_figure2.py = xbob.paper.tpami2013.scripts.plot_figure2:main',
        ],
      },

    namespace_packages = [
      'xbob',
      'xbob.paper',
    ],

    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Education',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
