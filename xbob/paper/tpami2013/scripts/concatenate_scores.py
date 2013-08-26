#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:58:03 CEST 2013
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
  """Concatenate scores after splitting the computation process using an SGE grid"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('-g', '--group', metavar='LIST', type=str,
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to retrieve models (defaults to "%(default)s").')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (features, models, scores, etc.).')
  parser.add_argument('--algorithm-dir', metavar='STR', type=str,
      dest='algorithm_dir', default='default_algorithm', help='The subdirectory where the data for the given algorithm are stored.')
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
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol

  N_MAX_SPLITS = 9999 # zfill is done with 4 zeros
  for group in args.group:
    # (sorted) list of models
    models_ids = sorted(config.db.model_ids(protocol=protocol, groups=group))

    sc_nonorm_filename = os.path.join(args.output_dir, protocol, args.algorithm_dir, config.scores_nonorm_dir, "scores-" + group)
    if args.force:
      print("Removing old scores file '%s'." % sc_nonorm_filename)
      utils.erase_if_exists(sc_nonorm_filename)
    
    if os.path.exists(sc_nonorm_filename):
      print("Scores file '%s' already exists." % sc_nonorm_filename)
    else:
      f = open(sc_nonorm_filename, 'w')
      # Concatenates the scores
      for model_id in models_ids:
        for split_id in range(0,N_MAX_SPLITS): 
          # Loads and concatenates
          split_path = os.path.join(args.output_dir, protocol, args.algorithm_dir, config.scores_nonorm_dir, group, str(model_id) + "_" + str(split_id).zfill(4) + ".txt")
          if split_id == 0 and not os.path.exists(split_path):
            raise RuntimeError("Cannot find file %s" % split_path)
          elif not os.path.exists(split_path):
            break
          f.write(open(split_path, 'r').read())
      f.close()

if __name__ == "__main__": 
  main()
