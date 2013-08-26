#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:57:04 CEST 2013
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
from .. import plda, utils

def main():
  """Train a PLDA model"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--nf', metavar='INT', type=int,
     dest='nf', default=None, help='The rank of the F subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--ng', metavar='INT', type=int,
     dest='ng', default=None, help='The rank of the G subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--world-nshots', metavar='INT', type=int,
     dest='world_nshots', default=0, help='The maximum number of samples per identity to use, to train the PLDA model. Default is to use all possible samples')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--plda-model-filename', metavar='STR', type=str,
      dest='plda_model_filename', default=None, help='The (relative) filename of the PLDABase model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the plda directory.')
  parser.add_argument('-p', '--protocol', metavar='STR', type=str,
      dest='protocol', default=None, help='The protocol of the database to consider. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.nf: plda_nf = config.plda_nf
  else: plda_nf = args.nf
  if args.ng: plda_ng = config.plda_ng
  else: plda_ng = args.ng
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features and the PLDA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)
  if args.plda_dir: plda_dir_ = args.plda_dir
  else: plda_dir_ = config.plda_dir
  if args.plda_model_filename: plda_model_filename_ = args.plda_model_filename
  else: plda_model_filename_ = config.model_filename
  plda_model_filename = os.path.join(args.output_dir, protocol, plda_dir_, plda_model_filename_)

  # Remove old file if required
  if args.force:
    print("Removing old PLDA base model.")
    utils.erase_if_exists(plda_model_filename)

  if os.path.exists(plda_model_filename):
    print("PLDA base model already exists.")
  else:
    print("Training PLDA base model.")

    # Get list of list of filenames to load
    training_filenames = []
    train_models = sorted(config.db.model_ids(groups='world', protocol=protocol))
    nfiles = 0
    for model_id in train_models:
      if args.world_nshots != 0: train_data_m = config.db.objects(protocol=protocol, groups='world', model_ids=(model_id,), world_nshots=args.world_nshots) 
      else: train_data_m = config.db.objects(protocol=protocol, groups='world', model_ids=(model_id,)) 
      nfiles = nfiles + len(train_data_m)
      training_filenames.append(train_data_m)
    print("Number of identities: %d" % len(training_filenames))
    print("Number of training files: %d" % nfiles)
    
    # Loads training data
    training_data = utils.load_data_by_client(training_filenames, features_dir, config.features_ext)

    # Trains a PLDABaseMachine
    machine = plda.train(training_data, training_data[0].shape[1], 
                         plda_nf, plda_ng, config.plda_n_iter,
                         config.plda_seed, config.plda_init_f_method, config.plda_init_f_ratio, 
                         config.plda_init_g_method, config.plda_init_g_ratio, 
                         config.plda_init_s_method, config.plda_init_s_ratio)

    # Saves the machine
    utils.save_machine(machine, plda_model_filename)

if __name__ == "__main__": 
  main()
