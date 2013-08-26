#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Aug 26 18:12:46 CEST 2013
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
import numpy
import math
import argparse
from .. import utils

def main():
  """Plot Figure 2 of the article, assuming that the required experiments have successfully completed"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if not args.plda_dir: plda_dir = config.plda_dir
  else: plda_dir = args.plda_dir

  # Read files containing the scores and compute mean accuracy on the 10 folds
  print('Table 2')
  print('Method\t\t\tAccuracy')
  ac_values = []
  for k in range(1,11):
    scores_dir = os.path.join(args.output_dir, 'view2-fold%d' % k, plda_dir, config.scores_nonorm_dir)
    filename_dev = os.path.join(scores_dir, 'scores-dev')
    filename_eval = os.path.join(scores_dir, 'scores-eval')
    ac_values.append(1. - utils.compute_hter(filename_dev, filename_eval))

  # Computes standard error of the mean as explained in LFW reference
  ac_values = numpy.array(ac_values)
  accuracy_mean = numpy.mean(ac_values)
  std_error = math.sqrt(numpy.square(ac_values - accuracy_mean).sum() / 9.) / math.sqrt(10)
  print('SIFT PLDA funneled\t%.4f +/- %.4f' % (accuracy_mean, std_error))
  print('SIFT PLDA funneled [2]\t0.862  +/- 0.0012')
  print('SIFT LDML funneled [3]\t0.832  +/- 0.0004')

if __name__ == "__main__": 
  main()
