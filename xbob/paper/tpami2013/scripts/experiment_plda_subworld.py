#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Thu Aug 22 13:12:29 CEST 2013
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
  """PLDA experiments required to reproduce Figure 2 of the article"""

  # Parses options
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--nf', metavar='INT', type=int,
     dest='nf', default=0, help='The dimensionality of the F subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--ng', metavar='INT', type=int,
     dest='ng', default=0, help='The dimensionality of the G subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value \'lbph_features_dir\' in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--plda-model-filename', metavar='STR', type=str,
      dest='plda_model_filename', default=None, help='The (relative) filename of the PLDABase model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the plda directory.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='Run the script using the gridtk on an SGE infrastructure.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.nf == 0: plda_nf = config.plda_nf
  else: plda_nf = args.nf
  if args.ng == 0: plda_ng = config.plda_ng
  else: plda_ng = args.ng
  # Directories containing the features and the PLDA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, config.protocol, config.features_dir)
  if not args.plda_dir: plda_dir = config.plda_dir
  else: plda_dir = args.plda_dir
  if args.plda_model_filename: plda_model_filename = args.plda_model_filename
  else: plda_model_filename = config.model_filename

  # Run the PLDA toolchain for a varying number of training samples
  subworld_n = [2, 4, 6, 8, 10, 14, 19, 29, 38, 48, 57, 67, 76]
  for k in subworld_n:
    plda_dir_k = '%s_subworld_%d' % (plda_dir, k)
    cmd_plda = [ 
                './bin/toolchain_plda.py', 
                '--config-file=%s' % args.config_file, 
                '--nf=%d' % plda_nf,
                '--ng=%d' % plda_ng,
                '--world-nshots=%d' % k,
                '--output-dir=%s' % args.output_dir,
                '--features-dir=%s' % features_dir,
                '--plda-dir=%s' % plda_dir_k,
                '--plda-model-filename=%s' % plda_model_filename,
               ]
    if args.force: cmd_plda.append('--force')
    if args.grid: cmd_plda.append('--grid')
    subprocess.call(cmd_plda)

if __name__ == '__main__':
  main()
