#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:56:10 CEST 2013
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

def main():
  """Train a LDA model"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--n-outputs', metavar='INT', type=int,
     dest='n_outputs', default=None, help='The rank of the LDA subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The subdirectory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--lda-dir', metavar='STR', type=str,
      dest='lda_dir', default=None, help='The subdirectory where the LDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--lda-model-filename', metavar='STR', type=str,
      dest='lda_model_filename', default=None, help='The (relative) filename of the LDA model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the algorithm directory.')
  parser.add_argument('--eigenvalues', metavar='FILE', type=str,
      dest='eig_filename', default=None, help='The file for storing the eigenvalues.')
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
  if args.n_outputs: lda_n_outputs = args.n_outputs
  else: lda_n_outputs = config.lda_n_outputs
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features and the LDA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)
  if args.lda_dir: lda_dir_ = args.lda_dir
  else: lda_dir_ = config.lda_dir
  if args.lda_model_filename: lda_model_filename_ = args.lda_model_filename
  else: lda_model_filename_ = config.model_filename
  lda_model_filename = os.path.join(args.output_dir, protocol, lda_dir_, lda_model_filename_)

  # Remove old file if required
  if args.force:
    print("Removing old LDA base model.")
    utils.erase_if_exists(lda_model_filename)

  if os.path.exists(lda_model_filename):
    print("LDA base model already exists.")
  else:
    print("Training LDA base model.")

    # Get list of list of filenames to load
    training_filenames = []
    train_models = sorted(config.db.model_ids(groups='world', protocol=protocol))
    nfiles = 0
    for model_id in train_models:
      train_data_m = sorted(config.db.objects(protocol=protocol, groups='world', model_ids=(model_id,)), key=lambda f: f.path)
      nfiles = nfiles + len(train_data_m)
      training_filenames.append(train_data_m)
    print("Number of identities: %d" % len(training_filenames))
    print("Number of training files: %d" % nfiles) 
 
    # Loads training data
    training_data = utils.load_data_by_client(training_filenames, features_dir, config.features_ext)

    # Trains a LDAMachine
    (machine, eig_vals) = linear.lda_train(training_data, lda_n_outputs)
    
    # Saves the machine
    utils.save_machine(machine, lda_model_filename)
    if args.eig_filename:
      import numpy
      eig_vals_s = numpy.ndarray(shape=(lda_n_outputs,), dtype=numpy.float64)
      eig_vals_s = eig_vals[0:lda_n_outputs]
      import bob
      bob.io.save(eig_vals_s, args.eig_filename)
    
if __name__ == "__main__": 
  main()
