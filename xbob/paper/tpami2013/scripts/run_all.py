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


"""Submits all feature creation jobs to the Idiap grid"""

import os
import sys
import math
import subprocess
import argparse
from .. import utils

def submit(job_manager, command, dependencies=[], array=None, queue=None, memfree=None, hostname=None, pe_opt=None):
  """Submits one job using our specialized shell wrapper. We hard-code certain
  parameters we like to use. You can change general submission parameters
  directly at this method."""

  from gridtk.tools import make_shell, random_logdir
  name = os.path.splitext(os.path.basename(command[0]))[0]
  logdir = os.path.join('logs', random_logdir())
  use_command = make_shell(sys.executable, command)
  return job_manager.submit(use_command, deps=dependencies, cwd=True,
      queue=queue, memfree=memfree, hostname=hostname, pe_opt=pe_opt, 
      stdout=logdir, stderr=logdir, name=name, array=array)

def main():
  """The main entry point, control here the jobs options and other details"""

  # Parses options
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--nf', metavar='INT', type=int,
     dest='nf', default=0, help='The dimensionality of the F subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--ng', metavar='INT', type=int,
     dest='ng', default=0, help='The dimensionality of the G subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--world-nshots', metavar='INT', type=int,
     dest='world_nshots', default=0, help='The maximum number of samples per identity to use, to train the PLDA model. Default is to use all possible samples')
  parser.add_argument('--output-dir', metavar='STR', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('-g', '--group', metavar='STR', type=str, nargs='+',
      dest='group', default=['dev','eval'], help='Database group (\'dev\' or \'eval\') for which to enrol models and compute scores.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='Run the script using the gridtk on an SGE infrastructure.')
  args = parser.parse_args()

  # Loads the configuration 
  import imp
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if args.nf == 0: plda_nf = config.plda_nf
  else: plda_nf = args.nf
  if args.ng == 0: plda_ng = config.plda_ng
  else: plda_ng = args.ng
  if not args.output_dir: output_dir = config.base_output_dir
  else: output_dir = args.output_dir
  if not args.pca_dir: pca_dir = config.pca_dir
  else: pca_dir = args.pca_dir
  if not args.plda_dir: plda_dir = config.plda_dir
  else: plda_dir = args.plda_dir
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
                  '--output-dir=%s' % output_dir,
                  '--pca-dir=%s' % pca_dir,
                  '--plda-dir=%s' % plda_dir,
                ]
  if args.force: cmd_pldabase.append('--force')
  if args.grid: 
    job_pldabase = submit(jm, cmd_pldabase, dependencies=[], array=None, queue='q1d', memfree='3G', hostname='!cicatrix')
    print('submitted: %s' % job_pldabase)
  else:
    print('Running PLDA training...')
    subprocess.call(cmd_pldabase)

  # Generates the models 
  job_models = []
  for group in groups:
    n_array_jobs = len(config.db.models(protocol=config.protocol, groups=group))
    cmd_models = [
                  './bin/plda_models.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % output_dir,
                  '--pca-dir=%s' % pca_dir,
                  '--plda-dir=%s' % plda_dir,
                  ]
    if args.force: cmd_models.append('--force')
    if args.grid: cmd_models.append('--grid')
    if args.grid: 
      job_models_int = submit(jm, cmd_models, dependencies=[job_pldabase.id()], array=None, queue='q1d', memfree='3G', hostname='!cicatrix')
      job_models.append(job_models_int.id())
      print('submitted: %s' % job_models_int)
    else:
      print('Running PLDA enrollment for %s...' % group)
      subprocess.call(cmd_models)

  # Compute raw scores (and A matrix for ZT-Norm)
  job_scores = []
  for group in groups:
    n_array_jobs = 0
    model_ids = sorted([model.id for model in config.db.models(protocol=config.protocol, groups=group)])
    for model_id in model_ids:
      n_probes_for_model = len(config.db.objects(groups=group, protocol=config.protocol, purposes='probe', model_ids=(model_id,)))
      n_splits_for_model = int(math.ceil(n_probes_for_model / float(config.n_max_probes_per_job)))
      n_array_jobs += n_splits_for_model
    cmd_scores = [
                  './bin/plda_scores.py',
                  '--config-file=%s' % args.config_file, 
                  '--group=%s' % group,
                  '--output-dir=%s' % output_dir,
                  '--pca-dir=%s' % pca_dir,
                  '--plda-dir=%s' % plda_dir,
                  ]
    if args.grid: cmd_scores.append('--grid')
    if args.grid: 
      deps = job_models
      job_scores_int = submit(jm, cmd_scores, dependencies=deps, array=(1,n_array_jobs,1), queue='q1d', memfree='3G', hostname='!cicatrix')
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
                '--output-dir=%s' % output_dir,
                '--plda-dir=%s' % plda_dir,
                '--grid'
              ]
    job_cat = submit(jm, cmd_cat, dependencies=job_scores, array=None)
    print('submitted: %s' % job_cat)

if __name__ == '__main__':
  main()
