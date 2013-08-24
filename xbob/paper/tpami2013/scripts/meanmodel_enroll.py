#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Thu Aug 22 17:52:05 CEST 2013
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
import imp
import argparse
import bob
from .. import utils

def main():

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('-g', '--group', metavar='LIST', type=str, nargs='+',
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to retrieve models.')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='FILE', type=str,
      dest='features_dir', default=None, help='The relative directory that contains the features to use.')
  parser.add_argument('--algorithm-dir', metavar='FILE', type=str,
      dest='algorithm_dir', default='default_algorithm', help='The relative directory of the algorithm that will contain the models and the scores.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Directories containing the features and the PLDA model
  if args.features_dir: features_dir_ = args.features_dir
  else: features_dir_ = config.features_dir
  if utils.check_string(args.group): groups = [args.group]
  else: groups = args.group

  # (sorted) list of models
  models_ids = sorted([model.id for model in config.db.models(protocol=config.protocol, groups=groups)])

  # Enrols all the client models
  print("Enrolling generic mean models...")
  for model_id in models_ids:
    # Path to the model
    model_path = os.path.join(args.output_dir, config.protocol, args.algorithm_dir, config.models_dir, str(model_id) + ".hdf5")

    # Remove old file if required
    if args.force:
      print("Removing old generic mean model")
      erase_if_exists(model_path)

    if os.path.exists(model_path):
      print("Generic mean model already exists")
    else:
      # List of enrollment filenames
      enroll_files = config.db.objects(protocol=config.protocol, model_ids=(model_id,), purposes='enrol')
      # Loads enrollment files
      features_dir = os.path.join(args.output_dir, config.protocol, args.features_dir)
      data = utils.load_data(enroll_files, features_dir, config.features_ext)
    
      # Enrols
      model = utils.enroll_mean_model(data)

      # Saves the machine
      utils.save_model(model, model_path)

if __name__ == "__main__": 
  main()
