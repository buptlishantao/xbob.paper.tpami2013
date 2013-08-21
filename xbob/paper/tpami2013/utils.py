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
import numpy
import bob

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


def save_machine(machine, output_filename):
  """Saves a machine into an HDF5File"""
  ensure_dir(os.path.dirname(output_filename))
  machine.save(bob.io.HDF5File(output_filename, 'w'))


def split_list(input_list, nb_unit_per_sublist):
  """Splits a list into a list of sublists (assuming that the list is sorted)"""  
  res = []
  slist = []
  to_append = False
  for k in input_list:
    slist[k] = input_list[k] 
    to_append = True
    # checks if the subdictionary is full
    if(len(slist) == nb_unit_per_sublist):
      res.append(slist)
      to_append = False
      slist = []

  if(to_append == True):
    res.append(slist)
  
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
    f_scores.write(str(x.client_id) + " " + str(model_id) + " " + str(x.path) + " " + str(scores[i]) + "\n")
    i+=1
  f_scores.close()
