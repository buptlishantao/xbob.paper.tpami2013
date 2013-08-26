#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:57:16 CEST 2013
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
import math
import imp
import subprocess
import argparse
from .. import utils

def main():
  """LBPH chi square toolchain"""
  # Parses options
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('-g', '--group', metavar='STR', type=str, nargs='+',
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to enroll models and compute scores.')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value \'lbph_features_dir\' in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--lbph-dir', metavar='FILE', type=str,
      dest='lbph_dir', default='lbph_chisquare', help='The relative directory of the LBPH that will contain the models and the scores. It is appended to the given output directory and the protocol.')
  parser.add_argument('--distance', metavar='STR', type=str,
      dest='distance', default='chi_square', help='The distance to use, when computing scores.')
  parser.add_argument('-p', '--protocol', metavar='STR', type=str,
      dest='protocol', default=None, help='The protocol of the database to consider. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='Run the script using the gridtk on an SGE infrastructure.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.lbph_features_dir)
  if utils.check_string(args.group): groups = [args.group]
  else: groups = args.group

  # Let's create the job manager
  if args.grid:
    from gridtk.manager import JobManager
    jm = JobManager()

  # Generates the models 
  job_enroll = []
  for group in groups:
    n_array_jobs = len(config.db.model_ids(protocol=protocol, groups=groups))
    cmd_enroll = [
                  './bin/meanmodel_enroll.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--algorithm-dir=%s' % args.lbph_dir,
                  '--protocol=%s' % protocol,
                 ]
    if args.force: cmd_enroll.append('--force')
    if args.grid: 
      cmd_enroll.append('--grid')
      job_enroll_int = utils.submit(jm, cmd_enroll, dependencies=None, array=None, queue='q1d', mem='2G', hostname='!cicatrix')
      job_enroll.append(job_enroll_int.id())
      print('submitted: %s' % job_enroll_int)
    else:
      print('Running enrollment for %s...' % group)
      subprocess.call(cmd_enroll)

  # Compute raw scores
  job_scores = []
  for group in groups:
    n_array_jobs = 0
    model_ids = sorted(config.db.model_ids(protocol=protocol, groups=group))
    for model_id in model_ids:
      n_probes_for_model = len(config.db.objects(groups=group, protocol=protocol, purposes='probe', model_ids=(model_id,)))
      n_splits_for_model = int(math.ceil(n_probes_for_model / float(config.n_max_probes_per_job)))
      n_array_jobs += n_splits_for_model
    cmd_scores = [
                  './bin/distance_scores.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--algorithm-dir=%s' % args.lbph_dir,
                  '--distance=%s' % args.distance,
                  '--protocol=%s' % protocol,
                 ]
    if args.grid: 
      cmd_scores.append('--grid')
      deps = job_enroll
      job_scores_int = utils.submit(jm, cmd_scores, dependencies=deps, array=(1,n_array_jobs,1), queue='q1d', mem='3G', hostname='!cicatrix')
      job_scores.append(job_scores_int.id())
      print('submitted: %s' % job_scores_int)
    else:
      print('Running scoring for %s...' % group)
      subprocess.call(cmd_scores)

  # Concatenates the scores
  if args.grid:
    cmd_cat = [ 
                './bin/concatenate_scores.py', 
                '--config-file=%s' % args.config_file, 
                '--output-dir=%s' % args.output_dir,
                '--algorithm-dir=%s' % args.lbph_dir,
                '--protocol=%s' % protocol,
                '--grid'
              ]
    job_cat = utils.submit(jm, cmd_cat, dependencies=job_scores, array=None)
    print('submitted: %s' % job_cat)

if __name__ == '__main__':
  main()
