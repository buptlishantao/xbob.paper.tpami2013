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
from .. import pca, utils
import bob
import numpy

def main():

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The subdirectory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it is being run using a parametric grid job. It orders all ids to be processed and picks the one at the position given by ${SGE_TASK_ID}-1')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)

  # Directories containing the features, the PCA model and the projected features
  if args.features_dir: features_dir_ = args.features_dir
  else: features_dir_ = config.features_dir
  features_dir = os.path.join(args.output_dir, config.protocol, features_dir_)
  if args.pca_dir: pca_dir_ = args.pca_dir
  else: pca_dir_ = config.pca_dir
  pca_model_filename = os.path.join(args.output_dir, config.protocol, pca_dir_, config.pca_model_filename)
  features_projected_dir = os.path.join(args.output_dir, config.protocol, pca_dir_, config.features_projected_dir)

  # Database python objects (sorted by keys in case of SGE grid usage)
  inputs_list = config.db.objects(protocol=config.protocol)
  inputs_list.sort(key=lambda x: x.id)

  # finally, if we are on a grid environment, just find what I have to process.
  if args.grid:
    import math
    pos = int(os.environ['SGE_TASK_ID']) - 1
    n_jobs = int(math.ceil(len(inputs_list) / float(config.n_fax_files_per_job)))
    
    if pos >= n_total:
      raise RuntimeError("Grid request for job %d on a setup with %d jobs" % (pos, n_total))
    inputs_list_g = utils.split_list(inputs_list, config.n_fax_files_per_job)[pos]
    inputs_list = input_list_g

  # Checks that the base directory for storing the features exists
  utils.ensure_dir(features_projected_dir)

  # Loads the machine (linear projection matrix)
  machine = pca.load_model(pca_model_filename)

  # Allocates an array for the projected data
  img_out = numpy.ndarray(shape=(machine.shape[1],), dtype=numpy.float64)

  for k in inputs_list:
    input_features_k = str(k.make_path(directory=features_dir, extension=config.features_ext))
    output_features_k = str(k.make_path(directory=features_projected_dir, extension=config.features_projected_ext))
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
      pca.project(img_in, machine, img_out)
      # Saves the projected data
      utils.ensure_dir(os.path.dirname(str(output_features_k)))
      bob.io.save(img_out, output_features_k)

if __name__ == "__main__": 
  main()
