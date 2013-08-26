#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:55:55 CEST 2013
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
import argparse
import imp
from .. import linear, utils
import bob
import numpy

def main():
  """Project features using a trained (either with PCA or LDA) LinearMachine"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file, that is appended to the given output directory and protocol.')
  parser.add_argument('--features-projected-dir', metavar='STR', type=str,
      dest='features_projected_dir', default=None, help='The subdirectory where the projected features will be stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the algorithm directory.')
  parser.add_argument('--algorithm-dir', metavar='STR', type=str,
      dest='algorithm_dir', default='pca', help='The subdirectory where the algorithm data are stored. It is appended to the given output directory and the protocol.')
  parser.add_argument('--model-filename', metavar='STR', type=str,
      dest='model_filename', default=None, help='The (relative) filename of the Linear model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the algorithm directory.')
  parser.add_argument('-p', '--protocol', metavar='STR', type=str,
      dest='protocol', default=None, help='The protocol of the database to consider. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it is being run using a parametric grid job. It orders all ids to be processed and picks the one at the position given by ${SGE_TASK_ID}-1')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features, the PCA model and the projected features
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)
  if args.features_projected_dir: features_projected_dir_ = args.features_projected_dir
  else: features_projected_dir_ = config.features_projected_dir
  features_projected_dir = os.path.join(args.output_dir, protocol, args.algorithm_dir, features_projected_dir_)
  if args.model_filename: model_filename = args.model_filename
  else: model_filename = config.model_filename
  model_filename = os.path.join(args.output_dir, protocol, args.algorithm_dir, model_filename) 

  # Database python objects (sorted by keys in case of SGE grid usage)
  inputs_list = sorted(config.db.objects(protocol=protocol), key=lambda f: f.path) 

  # finally, if we are on a grid environment, just find what I have to process.
  if args.grid:
    import math
    pos = int(os.environ['SGE_TASK_ID']) - 1
    n_jobs = int(math.ceil(len(inputs_list) / float(config.n_max_files_per_job)))
    
    if pos >= n_jobs:
      raise RuntimeError("Grid request for job %d on a setup with %d jobs" % (pos, n_jobs))
    inputs_list_g = utils.split_list(inputs_list, config.n_max_files_per_job)[pos]
    inputs_list = inputs_list_g

  # Checks that the base directory for storing the features exists
  utils.ensure_dir(features_projected_dir)

  # Loads the machine (linear projection matrix)
  machine = linear.load_model(model_filename)

  # Allocates an array for the projected data
  img_out = numpy.ndarray(shape=(machine.shape[1],), dtype=numpy.float64)

  for k in inputs_list:
    input_features_k = str(k.make_path(directory=features_dir, extension=config.features_ext))
    output_features_k = str(k.make_path(directory=features_projected_dir, extension=config.features_ext))
    if args.force == True and os.path.exists(output_features_k):
      print("Removing old features %s." % (output_features_k))
      os.remove(output_features_k)

    if os.path.exists(output_features_k):
      print("Projected features %s already exists."  % (output_features_k))
    else:
      print("Computing projected features from sample %s." % (input_features_k))
      # Loads the data
      img_in = bob.io.load( input_features_k )
      # Projects the data
      linear.project(img_in, machine, img_out)
      # Saves the projected data
      utils.ensure_dir(os.path.dirname(str(output_features_k)))
      bob.io.save(img_out, output_features_k)

if __name__ == "__main__": 
  main()
