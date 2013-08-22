#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El-Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Aug 19 14:48:06 CEST 2013
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

"""Trains and executes PLDA on the Fisher Iris Flower Dataset
"""

import bob
import numpy
import matplotlib.pyplot as mpl
import argparse

def split_iris_data():
  """Split the iris data into training, enrolment and test"""
  # Getting Iris flowers data
  data = bob.db.iris.data()
  # Splitting data into training, enrollment and test
  keys = data.keys() # 3 classes in this dataset
  # Training data consists of the 30 first samples of the first two classes
  data_train = dict((k,data[k][:30]) for k in keys[0:2])
  # Enrolment data consists of the 10 first samples of the third class
  data_enrol = data[keys[2]][:10]
  # Test data (positive) consists of the 40 last samples of the third class
  data_test_pos = data[keys[2]][10:]
  # Test data (negative) consists of the 20 last samples of the first two classes
  data_test_neg = numpy.vstack([data[k][30:] for k in data.keys()[0:2]])
  return (data_train, data_enrol, data_test_pos, data_test_neg)


def train(data, dim_f, dim_g):
  """Trains a new PLDABase given the input data
  
  Keyword parametes:

    data
      The data set, a python dictionary with the data for each class properly
      labelled by a string. The values of each entry of the dictionary
      correspond to a numpy.ndarray of floats with features in columns. Every
      row corresponds to a single example.

    dim_f
      Rank of the subspace F

    dim_g
      Rank of the subspace G

  Returns a new trained bob.machine.PLDABase.
  """
  
  print("Training your PLDA machine...")
  pldabase = bob.machine.PLDABase(data.values()[0].shape[1], dim_f, dim_g)
  trainer = bob.trainer.PLDATrainer()
  trainer.train(pldabase, data.values())
  print("Training done.")
  return pldabase

def enrol(data, pldabase):
  """Enrolls a class-specific PLDA model, given a trained bob.machine.PLDABase
  
  Keyword parametes:

    data
      The data set, a python list with the enrollment data for the class

    pldabase
      A trained PLDA model

  Returns a new trained class-specific bob.machine.PLDAMachine
  """

  print("Enrolling a class-specific PLDA model given the data...")
  machine = bob.machine.PLDAMachine(pldabase)
  trainer = bob.trainer.PLDATrainer()
  trainer.enrol(machine, data)
  print("Class-specific model enrolled.")
  return machine

def compute_scores(data, machine):
  """Computes (verification) scores given a bob.machine.PLDAMachine and test samples
  
  Keyword parametes:

    data
      The data set, a python list with the test samples

    machine
      A class-specific trained PLDA model

  Returns a new trained class-specific bob.machine.PLDAMachine
  """

  print("Computing true-access scores for a class-specific PLDA model...")
  A = numpy.ndarray(shape=(len(data),), dtype=numpy.float64)
  for i in range(len(data)):
    A[i] = machine.forward(data[i])
  return A

def plot(scores_pos, scores_neg, dbname, output_filename):
  """Saves a png histogram of the scores distribution

  Keyword parametes:

    scores_pos
      The scores for the positive trials

    scores_neg
      The scores for the negative trials
  """

  print("Plotting...")
  scores = [scores_pos, scores_neg]
  colors = ['green', 'red']
  labels = ['positive', 'negative']
  smin = int(min(scores_pos.min(),scores_neg.min()))
  smax = int(max(scores_pos.max(),scores_neg.max())+1)
  hrange= (smin, smax)
  for k in range(2):
    mpl.hist(scores[k], color=colors[k], bins=40, range = hrange,
      label=labels[k].capitalize(), alpha=0.5)

  # Plot "perfectioning"
  mpl.legend()
  mpl.grid(True)
  mpl.title("Scores distribution on the %s dataset using PLDA modeling" % dbname.capitalize())
  mpl.xlabel("Score values")
  mpl.ylabel("Count")
  mpl.savefig(output_filename)
  print("Saved your plot at '%s'... Bye!" % output_filename)

def main():
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('--output-img', metavar='FILE', type=str,
      dest='output_img', default='plda_example_iris.png', help='The path to the output image with the resulting scores distributions.')
  args = parser.parse_args()

  # Get data
  data_train, data_enrol, data_test_pos, data_test_neg = split_iris_data()

  # PLDA training
  dim_f = 1
  dim_g = 2
  plda_base = train(data_train, dim_f, dim_g)

  # PLDA enrollment
  plda_machine = enrol(data_enrol, plda_base)

  # PLDA scoring
  scores_pos = compute_scores(data_test_pos, plda_machine)
  scores_neg = compute_scores(data_test_neg, plda_machine)

  # Plot scores distributions
  plot(scores_pos, scores_neg, 'iris', args.output_img)

if __name__ == "__main__": 
  main()
