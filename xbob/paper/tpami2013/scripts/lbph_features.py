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
import subprocess
from .. import utils

def main():
  """Call the LBP Histograms feature extraction"""
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
      dest='features_dir', default=None, help='The directory for the output features. It will overwrite the value in the configuration file if any. Default is the value in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('-p', '--protocol', metavar='STR', type=str,
      dest='protocol', default=None, help='The protocol of the database to consider. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it will split the jobs on the SGE grid.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.lbph_features_dir)

  # Let's create the job manager
  if args.grid:
    from gridtk.manager import JobManager
    jm = JobManager()

  # Extract the features
  cmd_lbph_extract = [ 
                      './bin/lbph_extraction.py', 
                      '--config-file=%s' % args.config_file, 
                      '--image-dir=%s' % args.img_input_dir,
                      '--image-ext=%s' % args.img_input_ext,
                      '--annotation-dir=%s' % args.pos_input_dir,
                      '--annotation-ext=%s' % args.pos_input_ext,
                      '--output-dir=%s' % args.output_dir,
                      '--features-dir=%s' % features_dir,
                      '--protocol=%s' % protocol,
                     ]
  if args.force: cmd_lbph_extract.append('--force')
  if args.grid: 
    cmd_lbph_extract.append('--grid')
    import math
    # Database python objects (sorted by keys in case of SGE grid usage)
    inputs_list = config.db.objects(protocol=protocol)
    # Number of array jobs
    n_array_jobs = int(math.ceil(len(inputs_list) / float(config.n_max_files_per_job)))  
    job_lbph_extract = utils.submit(jm, cmd_lbph_extract, dependencies=None, array=(1,n_array_jobs,1), queue='q1d', mem='2G', hostname='!cicatrix')
    print('submitted: %s' % job_lbph_extract)
  else:
    print('Running LBPH feature extraction...')
    subprocess.call(cmd_lbph_extract)

if __name__ == "__main__": 
  main()
