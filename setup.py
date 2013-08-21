from setuptools import setup, find_packages

setup(

    name='xbob.paper.tpami2013',
    version='0.0.1a0',
    description='PLDA example',
    url='http://pypi.python.org/pypi/xbob.paper.tpami2013',
    license='GPLv3',
    author='Laurent El Shafey',
    author_email='Laurent.El-Shafey@idiap.ch',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
      'setuptools',
      'bob >= 1.2.0',
      'xbob.db.multipie',
    ],

    entry_points={
      'console_scripts': [
        'plda_example_iris.py = xbob.paper.tpami2013.scripts.plda_example_iris:main',
        'lbph_features.py = xbob.paper.tpami2013.scripts.lbph_features:main',
        'pca_train.py = xbob.paper.tpami2013.scripts.pca_train:main',
        'pca_project.py = xbob.paper.tpami2013.scripts.pca_project:main',
        'plda_train.py = xbob.paper.tpami2013.scripts.plda_train:main',
        'plda_models.py = xbob.paper.tpami2013.scripts.plda_models:main',
        'plda_scores.py = xbob.paper.tpami2013.scripts.plda_scores:main',
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
