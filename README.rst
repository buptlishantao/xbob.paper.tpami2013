Probabilistic Linear Discriminant Analysis Experiments
======================================================

This package contains scripts that shows how to use the implementation
of the scalable formulation of Probabilistic Linear Discriminant Analysis 
(PLDA), integrated into bob, as well as how to reproduce experiments of
the article mentioned below.

If you use this package and/or its results, please cite the following
publications:

1. The original paper with the scalable formulation of PLDA explained 
   in details::

    @article{ElShafey_TPAMI_2013,
      author = {El Shafey, Laurent and McCool, Chris and Wallace, Roy and Marcel, S{\'{e}}bastien},
      title = {A Scalable Formulation of Probabilistic Linear Discriminant Analysis: Applied to Face Recognition},
      year = {2013},
      month = jul,
      journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
      volume = {35},
      number = {7},
      pages = {1788-1794},
      doi = {10.1109/TPAMI.2013.38},
      pdf = {http://publications.idiap.ch/downloads/papers/2013/ElShafey_TPAMI_2013.pdf}
    }

2. Bob as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos and L. El Shafey and R. Wallace and M. G\"unther and C. McCool and S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }

3. If you decide to use the Multi-PIE database, you should also mention the
   following paper, where it is introduced::

    @article{Gross_IVC_2010,
     author = {Gross, Ralph and Matthews, Iain and Cohn, Jeffrey and Kanade, Takeo and Baker, Simon},
     title = {Multi-PIE},
     journal = {Image and Vision Computing},
     year = {2010},
     month = may,
     volume = {28},
     number = {5},
     issn = {0262-8856},
     pages = {807--813},
     numpages = {7},
     doi = {10.1016/j.imavis.2009.08.002},
     url = {http://dx.doi.org/10.1016/j.imavis.2009.08.002},
     acmid = {1747071},
    } 

4. If you only use the Multi-PIE annotations, you should cite the following paper
   since annotations were made for the experiments of this work::

    @article{ElShafey_TPAMI_2013,
      author = {El Shafey, Laurent and McCool, Chris and Wallace, Roy and Marcel, S{\'{e}}bastien},
      title = {A Scalable Formulation of Probabilistic Linear Discriminant Analysis: Applied to Face Recognition},
      year = {2013},
      month = jul,
      journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
      volume = {35},
      number = {7},
      pages = {1788-1794},
      doi = {10.1109/TPAMI.2013.38},
      pdf = {http://publications.idiap.ch/downloads/papers/2013/ElShafey_TPAMI_2013.pdf}
    }


Installation
------------

Just download this package and uncompressed it locally::

  $ wget http://pypi.python.org/packages/source/x/xbob.paper.tpami2013/xbob.paper.tpami2013-0.0.1.zip
  $ unzip xbob.paper.tpami2013-0.0.1.zip
  $ cd xbob.paper.tpami2013

Use buildout to bootstrap and have a working environment ready for
experiments::

  $ python bootstrap
  $ ./bin/buildout

This also requires that bob (>= 1.2.0) is installed.


PLDA tutorial
-------------

The following example consists of a simple script, that makes use of
PLDA modeling on the Fisher's iris dataset. It performs the following
tasks:

  1. Train a PLDA model using the first two classes of the dataset
  2. Enrol a class-specific PLDA model for the third class of the dataset
  3. Compute (verification) scores for both positive and negative samples
  4. Plot the distribution of the score and save it into a file called iris.png

To run this simple example, you just need to execute the following command::

  $ ./bin/plda_example_iris.py --output-img plda_example_iris.png


Reproducing Multi-PIE experiments
---------------------------------

Getting the data
~~~~~~~~~~~~~~~~

You first need to buy and download the Multi-PIE database:
  http://multipie.org/
as well as the annotations available here:
  http://www.idiap.ch/resource/biometric/


Feature extraction
~~~~~~~~~~~~~~~~~~

The following command will extract LBP histograms features.
You should set the paths to the data according to your own environment::

  $ ./bin/lbph_features.py --image-dir /PATH/TO/MULTIPIE/IMAGES --annotation-dir /PATH/TO/MULTIPIE/ANNOTATIONS --output-dir /PATH/TO/OUTPUT_DIR/


Dimensionality reduction
~~~~~~~~~~~~~~~~~~~~~~~~

Once the features has been extracted, they are projected into a lower
dimensional subspace using Principal Component Analysis (PCA)::

  $ ./bin/pca_train.py --output-dir /PATH/TO/OUTPUT_DIR/
  $ ./bin/pca_project.py --output-dir /PATH/TO/OUTPUT_DIR/


PLDA modeling and scoring
~~~~~~~~~~~~~~~~~~~~~~~~~

PLDA is then applied on the dimensionality reduced features.

This involves three different steps:
  1. Training
  2. Model enrollment
  3. Scoring

The following commands will perform all these steps::

  $ ./bin/plda_train.py --output-dir /PATH/TO/OUTPUT_DIR/
  $ ./bin/plda_models.py --output-dir /PATH/TO/OUTPUT_DIR/
  $ ./bin/plda_scores.py --group dev --output-dir /PATH/TO/OUTPUT_DIR/
  $ ./bin/plda_scores.py --group eval --output-dir /PATH/TO/OUTPUT_DIR/

Then, the HTER on the evaluation set can be obtained using the 
evaluation script from the bob library as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/OUTPUT_DIR/U/plda/scores/scores-dev -t /PATH/TO/OUTPUT_DIR/U/plda/scores/scores-eval -x

