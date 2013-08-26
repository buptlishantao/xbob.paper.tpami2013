#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Aug 26 18:03:11 CEST 2013
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
import subprocess
import imp
import argparse
from .. import utils

def main():
  """PLDA experiments required to reproduce first value in Table 2 of the article (on LFW)"""
  # Parses options
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_lfw.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--pca-n-outputs', metavar='INT', type=int,
     dest='pca_n_outputs', default=None, help='The rank of the PCA subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--plda-nf', metavar='INT', type=int,
     dest='plda_nf', default=None, help='The dimensionality of the F subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--plda-ng', metavar='INT', type=int,
     dest='plda_ng', default=None, help='The dimensionality of the G subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value \'sift_features_dir\' in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--pca-model-filename', metavar='STR', type=str,
      dest='pca_model_filename', default=None, help='The (relative) filename of the PCA model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the pca directory.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--plda-model-filename', metavar='STR', type=str,
      dest='plda_model_filename', default=None, help='The (relative) filename of the PLDABase model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the plda directory.')
  parser.add_argument('-g', '--group', metavar='STR', type=str, nargs='+',
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to enroll models and compute scores.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='Run the script using the gridtk on an SGE infrastructure.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.pca_n_outputs: pca_n_outputs = args.pca_n_outputs
  else: pca_n_outputs = config.pca_n_outputs
  if args.plda_nf: plda_nf = args.plda_nf
  else: plda_nf = config.plda_nf
  if args.plda_ng: plda_ng = args.plda_ng
  else: plda_ng = config.plda_ng
  # Directories containing the features and the PLDA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = config.sift_features_dir
  if args.pca_dir: pca_dir = args.pca_dir
  else: pca_dir = config.pca_dir
  if args.pca_model_filename: pca_model_filename = args.pca_model_filename
  else: pca_model_filename = config.model_filename
  if args.plda_dir: plda_dir = args.plda_dir
  else: plda_dir = config.plda_dir
  if args.plda_model_filename: plda_model_filename = args.plda_model_filename
  else: plda_model_filename = config.model_filename
  if utils.check_string(args.group): groups = [args.group]
  else: groups = args.group

  # Run the PLDA toolchain for the 10 folds protocols
  for k in range(1,11):
    protocol = 'view2-fold%s' % k
    cmd_plda = [ 
                './bin/toolchain_pcaplda.py',
                '--config-file=%s' % args.config_file, 
                '--pca-n-outputs=%d' % pca_n_outputs,
                '--plda-nf=%d' % plda_nf,
                '--plda-ng=%d' % plda_ng,
                '--output-dir=%s' % args.output_dir,
                '--features-dir=%s' % features_dir,
                '--pca-dir=%s' % pca_dir,
                '--pca-model-filename=%s' % pca_model_filename,
                '--plda-dir=%s' % plda_dir,
                '--plda-model-filename=%s' % plda_model_filename,
                '--protocol=%s' % protocol,
               ]
    sgroups = ['--group']
    sgroups.extend(groups)
    cmd_plda.extend(sgroups)
    if args.force: cmd_plda.append('--force')
    if args.grid: cmd_plda.append('--grid')
    subprocess.call(cmd_plda)

if __name__ == '__main__':
  main()
