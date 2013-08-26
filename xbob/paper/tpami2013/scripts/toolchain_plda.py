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
  """PLDA toolchain"""

  # Parses options
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--nf', metavar='INT', type=int,
     dest='nf', default=0, help='The dimensionality of the F subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--ng', metavar='INT', type=int,
     dest='ng', default=0, help='The dimensionality of the G subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--world-nshots', metavar='INT', type=int,
     dest='world_nshots', default=0, help='The maximum number of samples per identity to use, to train the PLDA model. Default is to use all possible samples')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value \'lbph_features_dir\' in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--plda-model-filename', metavar='STR', type=str,
      dest='plda_model_filename', default=None, help='The (relative) filename of the PLDABase model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the plda directory.')
  parser.add_argument('-g', '--group', metavar='STR', type=str, nargs='+',
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to enroll models and compute scores.')
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
  if args.nf == 0: plda_nf = config.plda_nf
  else: plda_nf = args.nf
  if args.ng == 0: plda_ng = config.plda_ng
  else: plda_ng = args.ng
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features and the PLDA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)
  if args.plda_dir: plda_dir = args.plda_dir
  else: plda_dir = config.plda_dir
  if args.plda_model_filename: plda_model_filename = args.plda_model_filename
  else: plda_model_filename = config.model_filename
  if utils.check_string(args.group): groups = [args.group]
  else: groups = args.group

  # Let's create the job manager
  if args.grid:
    from gridtk.manager import JobManager
    jm = JobManager()

  # Trains the PLDABaseMachine
  cmd_pldabase = [ 
                  './bin/plda_train.py', 
                  '--config-file=%s' % args.config_file, 
                  '--nf=%d' % plda_nf,
                  '--ng=%d' % plda_ng,
                  '--world-nshots=%d' % args.world_nshots,
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--plda-dir=%s' % plda_dir,
                  '--plda-model-filename=%s' % plda_model_filename,
                  '--protocol=%s' % protocol,
                 ]
  if args.force: cmd_pldabase.append('--force')
  if args.grid: 
    cmd_pldabase.append('--grid')
    job_pldabase = utils.submit(jm, cmd_pldabase, dependencies=[], array=None, queue='q1d', mem='4G', hostname='!cicatrix')
    print('submitted: %s' % job_pldabase)
  else:
    print('Running PLDA training...')
    subprocess.call(cmd_pldabase)

  # Generates the models 
  job_enroll = []
  for group in groups:
    n_array_jobs = len(config.db.model_ids(protocol=protocol, groups=group))
    cmd_enroll = [
                  './bin/plda_enroll.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--plda-dir=%s' % plda_dir,
                  '--plda-model-filename=%s' % plda_model_filename,
                  '--protocol=%s' % protocol,
                 ]
    if args.force: cmd_enroll.append('--force')
    if args.grid: 
      cmd_enroll.append('--grid')
      job_enroll_int = utils.submit(jm, cmd_enroll, dependencies=[job_pldabase.id()], array=None, queue='q1d', mem='2G', hostname='!cicatrix')
      job_enroll.append(job_enroll_int.id())
      print('submitted: %s' % job_enroll_int)
    else:
      print('Running PLDA enrollment for %s...' % group)
      subprocess.call(cmd_enroll)

  # Compute raw scores (and A matrix for ZT-Norm)
  job_scores = []
  for group in groups:
    n_array_jobs = 0
    model_ids = sorted(config.db.model_ids(protocol=protocol, groups=group))
    for model_id in model_ids:
      n_probes_for_model = len(config.db.objects(groups=group, protocol=protocol, purposes='probe', model_ids=(model_id,)))
      n_splits_for_model = int(math.ceil(n_probes_for_model / float(config.n_max_probes_per_job)))
      n_array_jobs += n_splits_for_model
    cmd_scores = [
                  './bin/plda_scores.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--plda-dir=%s' % plda_dir,
                  '--plda-model-filename=%s' % plda_model_filename,
                  '--protocol=%s' % protocol,
                 ]
    if args.grid: 
      cmd_scores.append('--grid')
      deps = job_enroll
      job_scores_int = utils.submit(jm, cmd_scores, dependencies=deps, array=(1,n_array_jobs,1), queue='q1d', mem='3G', hostname='!cicatrix')
      job_scores.append(job_scores_int.id())
      print('submitted: %s' % job_scores_int)
    else:
      print('Running PLDA scoring for %s...' % group)
      subprocess.call(cmd_scores)

  # Concatenates the scores
  if args.grid:
    cmd_cat = [ 
                './bin/concatenate_scores.py', 
                '--config-file=%s' % args.config_file, 
                '--output-dir=%s' % args.output_dir,
                '--algorithm-dir=%s' % plda_dir,
                '--protocol=%s' % protocol,
                '--grid'
              ]
    job_cat = utils.submit(jm, cmd_cat, dependencies=job_scores, array=None)
    print('submitted: %s' % job_cat)

if __name__ == '__main__':
  main()
