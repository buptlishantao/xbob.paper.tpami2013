======================================================
Probabilistic Linear Discriminant Analysis Experiments
======================================================

This package contains scripts that show how to use the implementation
of the scalable formulation of Probabilistic Linear Discriminant Analysis 
(PLDA), integrated into `Bob <http://www.idiap.ch/software/bob>`_, as 
well as how to reproduce experiments of the article mentioned below. 
It is implemented and maintained via `github 
<http://www.github.com/bioidiap/xbob.paper.tpami2013>`_.

.. contents::

References
----------

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

3. If you decide to use the Multi-PIE database, you should mention the
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

5. If you decide to use the Labeled Faces in the Wild (LFW) database, you should 
   mention the following paper, where it is introduced::

    @TechReport{LFWTech,
      author = {Gary B. Huang and Manu Ramesh and Tamara Berg and Erik Learned-Miller},
      title = {Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments},
      institution = {University of Massachusetts, Amherst},
      year = {2007},
      number = {07-49},
      month =  oct,
    }


Installation
------------

.. note:: 

  If you are reading this page through our GitHub portal and not through PyPI,
  note **the development tip of the package may not be stable** or become
  unstable in a matter of moments.

  Go to `http://pypi.python.org/pypi/xbob.paper.tpami2013
  <http://pypi.python.org/pypi/xbob.paper.tpami2013>`_ to download the latest
  stable version of this package.

There are two options you can follow to get this package installed and
operational on your computer: you can use automatic installers like `pip
<http://pypi.python.org/pypi/pip/>`_ (or `easy_install
<http://pypi.python.org/pypi/setuptools>`_) or manually download, unpack and
use `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ to create a
virtual work environment just for this package. In both cases, you must
first install `Bob`_ (>= 1.2.0), whose installation process is described 
in the `user guide 
<http://www.idiap.ch/software/bob/docs/releases/last/sphinx/html/Installation.html>`_.


Using an automatic installer
============================

Using ``pip`` is the easiest (shell commands are marked with a ``$`` signal)::

  $ pip install xbob.paper.tpami2013

You can also do the same with ``easy_install``::

  $ easy_install xbob.paper.tpami2013

This will download and install this package plus any other required
dependencies. It will also verify if the version of Bob you have installed
is compatible.

This scheme works well with virtual environments by `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ or if you have root access to your
machine. Otherwise, we recommend you use the next option.


Using ``zc.buildout``
=====================

Download the latest version of this package from `PyPI
<http://pypi.python.org/pypi/xbob.paper.tpami2013>`_ and unpack it in your
working area::

  $ wget http://pypi.python.org/packages/source/x/xbob.paper.tpami2013/xbob.paper.tpami2013-0.3.0a2.zip
  $ unzip xbob.paper.tpami2013-0.3.0a2.zip
  $ cd xbob.paper.tpami2013-0.3.0a2

The installation of the toolkit itself uses `buildout 
<http://www.buildout.org/>`_. You don't need to understand its inner workings
to use this package. Here is a recipe to get you started::
  
  $ python bootstrap.py 
  $ ./bin/buildout

These two commands should download and install all non-installed dependencies and
get you a fully operational test and development environment.

.. note::

  The python shell used in the first line of the previous command set
  determines the python interpreter that will be used for all scripts developed
  inside this package. Because this package makes use of `Bob`,
  you must make sure that the ``bootstrap.py``
  script is called with the **same** interpreter used to build Bob, or
  unexpected problems might occur.

  If Bob is installed by the administrator of your system, it is safe to
  consider it uses the default python interpreter. In this case, the above 3
  command lines should work as expected. If you have Bob installed somewhere
  else on a private directory, edit the file ``buildout.cfg`` **before**
  running ``./bin/buildout``. Find the section named ``buildout`` and edit or
  add the line ``prefixes`` to point to the directory where Bob is installed or
  built. For example::

    [buildout]
    ...
    prefixes=/home/laurent/work/bob/build


PLDA tutorial
-------------

The following example consists of a simple script, that makes use of
Probabilistic Linear Discriminant Analysis (PLDA) modeling on the 
Fisher's iris dataset. It performs the following tasks:

  1. Train a PLDA model using the first two classes of the dataset
  2. Enroll a class-specific PLDA model for the third class of the dataset
  3. Compute (verification) scores for both positive and negative samples
  4. Plot the distribution of the scores and save it into a file

To run this simple example, you just need to execute the following command::

  $ ./bin/plda_example_iris.py --output-img plda_example_iris.png


Reproducing experiments
-----------------------

It is currently possible to reproduce all the experiments of the article
on both Labeled Faces in the Wild and Multi-PIE using the PLDA algorithm.
In particular, the value of the accuracy reported in Table 2, the 
Figure 2 and the HTER reported on Table 3 can be easily reproduced, by 
following the steps described below.

Be aware that all the scripts provide several optional arguments that
are very useful if you wish to use your own features or your own
parameters.

Keep in mind that the results published in the paper were obtained with
a pre-release of Bob (older than 1.0.0). You might hence observe slight 
differences when running the scripts with Bob 1.2.0.


Note for Grid Users
===================

At Idiap, we use the powerful Sun Grid Engine (SGE) to parallelize our 
job submissions as much as we can. At the Biometrics group, we have developed 
a little toolbox `gridtk <http://pypi.python.org/pypi/gridtk>`_ that can 
submit and manage jobs at the Idiap computing grid through SGE. 

The following sections will explain how to reproduce the paper results in 
single (non-gridified) jobs. If you are at Idiap, you could run the 
following commands on the SGE infrastructure, by applying the '--grid' 
flag to any command. This may also work on other locations with an SGE 
infrastructure, but will likely require some configuration changes in the 
gridtk utility.


Labeled Faces in the Wild dataset
=================================

The experiments of this section are performed on the LFW (Labeled Faces
in the Wild) protocol. The features are publicly available and will be
automatically downloaded from `this webpage 
<http://lear.inrialpes.fr/people/guillaumin/data.php>`_ if you follow the
instruction below. They were extracted on the LFW images aligned with the
funneling algorithm.


Getting the features and converting them into HDF5 format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following command will download a tarball with the SIFT features, 
extract the content of the archive and convert the features into a 
suitable HDF5 format for Bob::

  $ ./bin/lfw_features.py --output-dir /PATH/TO/LFW/DATABASE/


PCA+PLDA toolchain on LFW
~~~~~~~~~~~~~~~~~~~~~~~~~

Once the features have been extracted, the dimensionality is reduced
using Principal Component Analysis (PCA), before applying PLDA modeling.
These steps are combined in the following script, that will run the 
PCA+PLDA toolchain on the specified protocol::

  $ ./bin/toolchain_pcaplda.py --features-dir /PATH/TO/LFW/DATABASE/lfw_funneled --protocol view1 --output-dir /PATH/TO/LFW/OUTPUT_DIR/

To report the final performance on LFW, it is required to run 
10 experiments on view 2 in a leave-one-out cross validation scheme.
We provide the following script for this purpose::

  $ ./bin/experiment_pcaplda_lfw.py -features-dir /PATH/TO/LFW/DATABASE/lfw_funneled --output-dir /PATH/TO/LFW/OUTPUT_DIR/

.. note::

  The previous script is monothreaded and will run the 10 independent
  view 2 experiments in a sequence. If you have a multi-core CPU, you
  could split this script into several shorter jobs, by splitting the
  loop below, which will at the end be equivalent to the previous 
  command::

    $ for k in `seq 1 10`; do \
        ./bin/toolchain_pcaplda.py --features-dir /PATH/TO/LFW/DATABASE/lfw_funneled --protocol view2-fold${k} --output-dir /PATH/TO/LFW/OUTPUT_DIR/ ; \
      done


Summarizing the results as in Table 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the previous experiments have successfully completed, you can use 
the following script to plot Table 2, that will estimate the mean
accuracy as well as the standard error of the mean on the 10 experiments
of LFW view2::

  $ ./bin/plot_table2.py --output-dir /PATH/TO/LFW/OUTPUT_DIR/

.. note::

  Compared to the results published in the article, there are slight
  differences caused by both the order of the training files when applying
  PCA, and the lists used to split the LFW `training` set into a `training`
  set and a `validation` set (The validation set is use to select the 
  verification threshold to apply on the test set).


Multi-PIE dataset
=================

The experiments of this section are performed on the U protocol of the
Multi-PIE dataset. The filelists associated with this protocol can be found
on `this website <http://www.idiap.ch/resource/biometric>`_.


Getting the data
~~~~~~~~~~~~~~~~

You first need to buy and download the Multi-PIE database:
  http://multipie.org/
and to download the annotations available here:
  http://www.idiap.ch/resource/biometric/


Feature extraction
~~~~~~~~~~~~~~~~~~

The following command will extract Local Binary Patters (LBP) histograms 
features. You should set the paths to the data according to your own 
environment::

  $ ./bin/lbph_features.py --image-dir /PATH/TO/MULTIPIE/IMAGES --annotation-dir /PATH/TO/MULTIPIE/ANNOTATIONS --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  The output directory /PATH/TO/MULTIPIE/OUTPUT_DIR/ is a base directory
  for the output of all experiments on Multi-PIE. Make sure to use the 
  same directory for all the experiments below, otherwise the following
  commands might not work as expected. You can look at the options
  of the scripts if you need more flexibility or want to use alternate
  features vectors, etc.


Dimensionality reduction
~~~~~~~~~~~~~~~~~~~~~~~~

Once the features has been extracted, they are projected into a lower
dimensional subspace using Principal Component Analysis (PCA)::
  
  $ ./bin/pca_features.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands::

    $ ./bin/pca_train.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --pca-dir features --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/linear_project.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --algorithm-dir features --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/


Proposed system: PLDA modeling and scoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PLDA is then applied on the dimensionality reduced features.

This involves three different steps:
  1. Training
  2. Model enrollment
  3. Scoring

The following command will perform all these steps::

  $ ./bin/toolchain_plda.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands::

    $ ./bin/plda_train.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/plda_enroll.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/plda_scores.py --group dev --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/plda_scores.py --group eval --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

Then, the HTER on the evaluation set can be obtained using the 
evaluation script from the bob library as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/MULTIPIE/OUTPUT_DIR/U/plda/scores/scores-dev -t /PATH/TO/MULTIPIE/OUTPUT_DIR/U/plda/scores/scores-eval -x

The HTER on the evaluation set, when using the EER on the development
set as the criterion for the threshold, corresponds to the PLDA value reported
on Table 3 of the article mentioned above.

If you want to reproduce the Figure 2 of the article, you can run the 
following commands (instead of the previous one)::

  $ ./bin/experiment_plda_subworld.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
  $ ./bin/plot_figure2.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands. Be aware that the commands within the loop
  are independent and monothreaded. Furthermore, you could break
  the loop and call several of these commands at the same time
  if your CPU has several cores::

    $ for k in 2 4 6 8 10 14 19 29 38 48 57 67 76; do \
        ./bin/toolchain_plda.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/ --world-nshots $k --plda-dir plda_subworld_${k}; \
      done
    $ ./bin/plot_figure2.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

The previous commands will run the PLDA toolchain several times for a varying
number of training samples. Please note, that this will require a lot of time
to complete (a bit less than two days on a recent workstation such as one with an
Intel Core i7 CPU).

Then, the value of the HTER on Table 3 of the article (for the PLDA system) 
corresponds to the one, where the full training set is used, and might 
similarly be obtained as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/MULTIPIE/OUTPUT_DIR/U/plda_subworld_76/scores/scores-dev -t /PATH/TO/MULTIPIE/OUTPUT_DIR/U/plda_subworld_76/scores/scores-eval -x

.. note::

  If you compare your obtained figure with the Figure 2 of the published article, 
  you will observe slight differences. This does not affect at all the global
  trends and conclusions shown in the article. This is caused by two different 
  aspects:

  1. The features for the paper were generated using a version of Bob that is 
     unofficial (which means older than the first official release), whereas the 
     features currently generated rely on Bob 1.2.0. Many improvements were 
     performed in the implementations of the preprocessing techniques (Face 
     cropping and Tan Triggs algorithm) as well as in the LBP implementation. 

  2. The order of the files obtained (and now sorted) from the database API.
     For instance, when applying PCA, the input matrix will be different depending
     on the order of the file used to build this matrix.


Baseline 1: PCA on the LBP histograms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The LBP histogram features were used in combination with the PCA 
classification technique (commonly called Eigenfaces in the face 
recognition literature).

This involves three different steps:
  1. PCA subspace training
  2. Model enrollment
  3. Scoring (with an Euclidean distance)

The following command will perform all these steps::

  $ ./bin/toolchain_pca.py --n-outputs 2048 --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands::

    $ ./bin/pca_train.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --n-outputs 2048 --pca-dir pca_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/linear_project.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --algorithm-dir pca_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/meanmodel_enroll.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/pca_euclidean/lbph_projected --algorithm-dir pca_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/pca_euclidean/lbph_projected --algorithm-dir pca_euclidean --distance euclidean --group dev --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/pca_euclidean/lbph_projected --algorithm-dir pca_euclidean --distance euclidean --group eval --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

Then, the HTER on the evaluation set can be obtained using the 
evaluation script from the bob library as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/MULTIPIE/OUTPUT_DIR/U/pca_euclidean/scores/scores-dev -t /PATH/TO/MULTIPIE/OUTPUT_DIR/U/pca_euclidean/scores/scores-eval -x

This value corresponds to the one of the PCA baseline reported on 
Table 3 of the article (Once more, be aware of differences due 
to the implementation changes in the feature extraction process 
and algorithm parameters that have not been kept). These results 
are obtained for a PCA subspace of rank 2048, which was 
found to be the optimal PCA subspace size, when we tuned this
parameter using the LBPH features.

.. note::

  In contrast to what one sentence of the article suggests, we did not 
  apply the PCA baseline on the dimensionality-reduced PCA features.
  This would mean to apply consecutively twice, the same PCA 
  dimensionality reduction technique, which does not make much sense.
  In contrast, we apply this PCA technique to the LBPH features,
  tuning the PCA subspace size.


Baseline 2: LDA on the PCA projected LBP histograms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PCA projected LBP histogram features considered for the PLDA system
were also used in combination with the Fisher's Linear Discriminant 
Analysis (LDA) classification technique (commonly called Fisherfaces 
in the face recognition literature).

This involves three different steps:
  1. LDA subspace training
  2. Model enrollment
  3. Scoring (with an Euclidean distance)

The following command will perform all these steps::

  $ ./bin/toolchain_lda.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands::

    $ ./bin/lda_train.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph_projected --lda-dir lda_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/linear_project.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph_projected --algorithm-dir lda_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/meanmodel_enroll.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lda_euclidean/lbph_projected --algorithm-dir lda_euclidean --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lda_euclidean/lbph_projected --algorithm-dir lda_euclidean --distance euclidean --group dev --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lda_euclidean/lbph_projected --algorithm-dir lda_euclidean --distance euclidean --group eval --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

Then, the HTER on the evaluation set can be obtained using the 
evaluation script from the bob library as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lda_euclidean/scores/scores-dev -t /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lda_euclidean/scores/scores-eval -x

This value corresponds to the one of the LDA baseline reported on 
Table 3 of the PLDA article (Once more, be aware of slight 
differences due to the implementation changes in the feature 
extraction process). These results are obtained for a LDA subspace 
of rank 64, which was found to be the optimal LDA subspace size, 
when we tuned this parameter using the initial LBPH features.


Baseline 3: LBP histogram classification with Chi square scoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The LBP histogram features might be used in combination with a distance such
as the Chi Square distance, to obtain a face recognition system.

This involves two different steps:
  1. Model enrollment
  2. Scoring (with a chi square distance)

The following command will perform all these steps::

  $ ./bin/toolchain_lbph.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

.. note::

  Equivalently, this can also be achieved by running the following 
  individual commands::

    $ ./bin/meanmodel_enroll.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --algorithm-dir lbph_chisquare --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --algorithm-dir lbph_chisquare --distance chi_square --group dev --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/
    $ ./bin/distance_scores.py --features-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/U/features/lbph --algorithm-dir lbph_chisquare --distance chi_square --group eval --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/

Then, the HTER on the evaluation set can be obtained using the 
evaluation script from the bob library as follows::

  $ ./bin/bob_compute_perf.py -d /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lbph_chisquare/scores/scores-dev -t /PATH/TO/MULTIPIE/OUTPUT_DIR/U/lbph_chisquare/scores/scores-eval -x

This value corresponds to the one of the LBP histogram (chi square) 
baseline reported on Table 3 of article (Once more, be aware of 
slight differences due to the implementation changes on the feature 
extraction process).


Summarizing the results as in Table 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you successfully run all the previous experiments, you could
get a summary of the performances, as in Table 3, by running the
following command::

  $ ./bin/plot_table3.py --output-dir /PATH/TO/MULTIPIE/OUTPUT_DIR/


Reporting bugs
--------------

The package is open source and maintained via `github 
<http://www.github.com/bioidiap/xbob.paper.tpami2013>`_.

If you are facing technical issues to be able to run the scripts
of this package, please send a message on the `Bob's mailing list
<https://groups.google.com/forum/#!forum/bob-devel>`_.

If you find a problem wrt. this satelitte package, you can file
a ticket on the `github issue tracker
<http://www.github.com/bioidiap/xbob.paper.tpami2013/issues>`_  of this
satellite package.

If you find a problem wrt. the PLDA implementation, you can file
a ticket on `Bob's issue tracker <http://www.github.com/idiap/bob/issues>`_ .

Please follow `these guidelines 
<http://www.idiap.ch/software/bob/docs/releases/last/sphinx/html/TicketReportingDev.html>`_
when (or even better before) reporting any bug.
