#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

import os, sys
import imp 
import argparse
from .. import utils

def main():

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it is being run using a parametric grid job. It orders all ids to be processed and picks the one at the position given by ${SGE_TASK_ID}-1')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)

  N_MAX_SPLITS = 9999 # zfill is done with 4 zeros
  for group in ['dev','eval']:
    # (sorted) list of models
    models_ids = sorted([model.id for model in config.db.models(protocol=config.protocol, groups=group)])

    sc_nonorm_filename = os.path.join(args.output_dir, config.protocol, config.scores_nonorm_dir, "scores-" + group)
    utils.erase_if_exists(sc_nonorm_filename)
    f = open(sc_nonorm_filename, 'w')
    # Concatenates the scores
    for model_id in models_ids:
      for split_id in range(0,N_MAX_SPLITS): 
        # Loads and concatenates
        split_path = os.path.join(args.output_dir, config.protocol, config.scores_nonorm_dir, group, str(model_id) + "_" + str(split_id).zfill(4) + ".txt")
        if split_id == 0 and not os.path.exists(split_path):
          raise RuntimeError("Cannot find file %s" % split_path)
        elif not os.path.exists(split_path):
          break
        f.write(open(split_path, 'r').read())
    f.close()

if __name__ == "__main__": 
  main()
