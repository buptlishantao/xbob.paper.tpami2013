#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

import os
import math
import numpy
import bob
import sys

def ensure_dir(dirname):
  """ Creates the directory dirname if it does not already exist,
      taking into account concurrent 'creation' on the grid.
      An exception is thrown if a file (rather than a directory) already 
      exists. """
  try:
    # Tries to create the directory
    os.makedirs(dirname)
  except OSError:
    # Check that the directory exists
    if os.path.isdir(dirname): pass
    else: raise


def erase_if_exists(filename):
  """Erases the file with the given filename if it exists."""
  if os.path.exists(filename):
    try:
      # Removes the file
      os.remove(filename)
    except OSError:
      # Checks that the file exists (in case of concurrent deletion)
      if os.path.exists(filename): pass
      else: raise


def check_string(var):
  """Make sure that the passed argument is a tuple or a list"""
  from six import string_types
  return isinstance(var, string_types)


def submit(job_manager, command, dependencies=[], array=None, queue=None, mem=None, hostname=None, pe_opt=None):
  """Submits one job using our specialized shell wrapper. We hard-code certain
  parameters we like to use. You can change general submission parameters
  directly at this method."""

  from gridtk.tools import make_shell, random_logdir
  name = os.path.splitext(os.path.basename(command[0]))[0]
  logdir = os.path.join('logs', random_logdir())
  use_command = make_shell(sys.executable, command)
  return job_manager.submit(use_command, deps=dependencies, cwd=True,
      queue=queue, mem=mem, hostname=hostname, pe_opt=pe_opt, 
      stdout=logdir, stderr=logdir, name=name, array=array)


def load_data(filenames, features_dir, features_ext):
  """Loads the data (arrays) from a list of filenames, and put them in a
     2D NumPy array."""
  # Loads files
  data = []
  for kf in filenames:
    # Loads the file
    feat = bob.io.load( str(kf.make_path(directory=features_dir, extension=features_ext)) )
    # Appends in the arrayset
    data.append(feat)
  # Returns the Arrayset
  return numpy.vstack(data)


def load_data_by_client(filenames_by_client, features_dir, features_ext):
  """Loads the data (arrays) from a list of list of filenames, 
     one list for each client, and put them in a list of Arraysets."""
  # Initializes an arrayset for the data
  data = []
  for kc in filenames_by_client:
    # Arrayset for this client
    data_client = []
    for kf in kc:
      # Loads the file
      img = bob.io.load( str(kf.make_path(directory=features_dir, extension=features_ext) ) )
      # Appends in the arrayset
      data_client.append(img)
    data.append(numpy.vstack(data_client))
  # Returns the list of Arraysets
  return data


def enroll_mean_model(data):
  """Enroll a generic mean model as the mean of the enrollment samples"""
  return data.mean(axis=0)


def compute_distance_scores(model, probe_tests, distance):
  """Compute scores between a model and probe samples using a distance"""
  A = numpy.ndarray(shape=(len(probe_tests),), dtype=numpy.float64)
  import scipy.spatial.distance
  if distance == 'euclidean':
    dist = scipy.spatial.distance.euclidean
  elif distance == 'chi_square':
    dist = bob.math.chi_square
  elif distance == 'cosine':
    dist = scipy.spatial.distance.cosine
  else:
    raise RuntimeError("Unknow distance '%s' for computing scores." % distance)
  for i in range(len(probe_tests)):
    A[i] = -dist(model, probe_tests[i])
  return A


def save_machine(machine, output_filename):
  """Saves a machine into an HDF5File"""
  ensure_dir(os.path.dirname(output_filename))
  machine.save(bob.io.HDF5File(output_filename, 'w'))


def save_model(model, output_filename):
  """Saves a mean model into an HDF5File"""
  ensure_dir(os.path.dirname(output_filename))
  bob.io.save(model, output_filename)

def load_model(input_filename):
  """Loads a mean model fron an HDF5File"""
  if not os.path.exists(input_filename):
    raise RuntimeError("Cannot find model %s" % (input_filename))
  return bob.io.load(input_filename)


def split_list(input_list, nb_unit_per_sublist):
  """Splits a list into a list of sublists (assuming that the list is sorted)"""  
  res = []
  n_splits = int(math.ceil(len(input_list) / float(nb_unit_per_sublist)))
  for k in range(n_splits):
    res.append(input_list[k*nb_unit_per_sublist:(k+1)*nb_unit_per_sublist])
  
  return res 


def load_probes(probe_objects, features_dir, features_ext):
  """Loads the probes from a list of Database.objects, returns them,
     as well as their corresponding client_ids."""
  # Loads files
  probe_tests = []
  probe_clients_ids = []
  for k in probe_objects:
    p = bob.io.load(str(k.make_path(directory=features_dir, extension=features_ext)))
    probe_tests.append(p)
    probe_clients_ids.append(k.client_id)
  return (probe_tests,probe_clients_ids)


def save_scores_to_textfile(scores, probe_filenames, model_id, output_filename, append=False):
  """Saves an array of scores associated to some probe_objects, into an ASCII file
     with the four column format."""
  ensure_dir(os.path.dirname(output_filename))
  if append: f_scores = open(output_filename, 'a')
  else: f_scores = open(output_filename, 'w')
  i = 0 
  for x in probe_filenames:
    if hasattr(x, 'claimed_id'):
      f_scores.write(str(x.claimed_id) + " " + str(model_id) + " " + str(x.path) + " " + str(scores[i]) + "\n")
    else:
      f_scores.write(str(x.client_id) + " " + str(model_id) + " " + str(x.path) + " " + str(scores[i]) + "\n")
    i+=1
  f_scores.close()


def compute_hter(filename_dev, filename_eval):
  """Computes the HTER on the evaluation set, setting the threshold
     at the EER on development set, given both the scores on the 
     development and the evaluation set"""
  dev_neg, dev_pos = bob.measure.load.split_four_column(filename_dev)
  eval_neg, eval_pos = bob.measure.load.split_four_column(filename_eval)

  thres = bob.measure.eer_threshold(dev_neg, dev_pos)

  eval_far, eval_frr = bob.measure.farfrr(eval_neg, eval_pos, thres)
  return (eval_far + eval_frr) / 2.


