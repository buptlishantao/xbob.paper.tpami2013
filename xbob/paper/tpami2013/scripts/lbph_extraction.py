#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:58:13 CEST 2013
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
from .. import features, utils

def main():
  """Run the LBP Histograms feature extraction"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--image-dir', metavar='STR', type=str,
      dest='img_input_dir', default='/idiap/resource/database/Multi-Pie/data', help='The directory containing the input images.')
  parser.add_argument('--image-ext', metavar='STR', type=str,
      dest='img_input_ext', default='.png', help='The extension of the input images.')
  parser.add_argument('--annotation-dir', metavar='STR', type=str,
      dest='pos_input_dir', default='/idiap/group/biometric/annotations/multipie', help='The directory containing the input annotations.')
  parser.add_argument('--annotation-ext', metavar='STR', type=str,
      dest='pos_input_ext', default='.pos', help='The extension of the input annotations.')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The subdirectory for the output features. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-p', '--protocol', metavar='STR', type=str,
      dest='protocol', default=None, help='The protocol of the database to consider. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it is being run using a parametric grid job. It orders all ids to be processed and picks the one at the position given by ${SGE_TASK_ID}-1')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)

  # Database python objects (sorted by keys in case of SGE grid usage)
  inputs_list = sorted(config.db.objects(protocol=protocol), key=lambda f: f.path)

  # finally, if we are on a grid environment, just find what I have to process.
  if args.grid:
    import math
    pos = int(os.environ['SGE_TASK_ID']) - 1 
    n_jobs = int(math.ceil(len(inputs_list) / float(config.n_max_files_per_job)))
    
    if pos >= n_jobs:
      raise RuntimeError("Grid request for job %d on a setup with %d jobs" % (pos, n_jobs))
    inputs_lits_g = utils.split_list(inputs_list, config.n_max_files_per_job)[pos]
    inputs_list = inputs_lits_g

  # Checks that the directories for storing the features exists
  utils.ensure_dir(features_dir)

  features.extract_lbph(inputs_list, args.img_input_dir, args.img_input_ext, args.pos_input_dir, args.pos_input_ext, features_dir, config.features_ext,
                        # Cropping
                        config.crop_eyes_d, config.crop_h, config.crop_w, config.crop_oh, config.crop_ow,
                        # Tan Triggs
                        config.gamma, config.sigma0, config.sigma1, config.size, config.threshold, config.alpha,
                        # LBP
                        config.radius, config.p_n, config.circular, config.to_average, config.add_average_bit, config.uniform, config.rot_inv,
                        config.block_h, config.block_w, config.block_oh, config.block_ow, 
                        force = args.force)

if __name__ == "__main__": 
  main()
 
