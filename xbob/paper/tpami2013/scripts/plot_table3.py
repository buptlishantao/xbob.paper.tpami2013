#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Sat Aug 24 15:26:52 CEST 2013
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
from .. import utils

def main():
  """Plot Table 3 of the article, assuming that the required experiments have successfully completed"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for all the algorithms.')
  parser.add_argument('--algorithms-dir', metavar='STR', type=str, nargs='+',
      dest='algorithms_dir', default=['pca_euclidean', 'lda_euclidean', 'lbph_chisquare', 'plda'], help='The subdirectory where the algorithms data are stored.')
  parser.add_argument('--algorithms-name', metavar='STR', type=str, nargs='+',
      dest='algorithms_name', default=['PCA', 'LDA', 'LBPH', 'PLDA'], help='The name of the algorithm to display in the table.')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)

  # Read files containing the scores and compute HTER
  print('Table 3')
  print('Algorithm\t\tHTER')
  assert(len(args.algorithms_dir) == len(args.algorithms_name))
  for k in range(len(args.algorithms_dir)):
    scores_dir = os.path.join(args.output_dir, config.protocol, args.algorithms_dir[k], config.scores_nonorm_dir)
    filename_dev = os.path.join(scores_dir, 'scores-dev')
    filename_eval = os.path.join(scores_dir, 'scores-eval')
    hter_value = 100 * utils.compute_hter(filename_dev, filename_eval)
    print('%s\t\t\t%.2f %%' % (args.algorithms_name[k], hter_value))

if __name__ == "__main__": 
  main()
