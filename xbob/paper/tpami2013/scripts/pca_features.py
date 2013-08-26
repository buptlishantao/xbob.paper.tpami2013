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
  """Reduce the dimensionality of a feature set using PCA"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--n-outputs', metavar='INT', type=int,
     dest='n_outputs', default=None, help='The rank of the PCA subspace. It will overwrite the value in the configuration file if any. Default is the value in the configuration file')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value \'lbph_features_dir\' in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--features-projected-dir', metavar='STR', type=str,
      dest='features_projected_dir', default=None, help='The subdirectory where the projected features will be stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then preprended by the given output directory, the protocol and the pca directory.')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is appended to the given output directory and the protocol.')
  parser.add_argument('--pca-model-filename', metavar='STR', type=str,
      dest='pca_model_filename', default=None, help='The (relative) filename of the PCA model. It will overwrite the value in the configuration file if any. Default is the value in the configuration file. It is then appended to the given output directory, the protocol and the pca directory.')
  parser.add_argument('--eigenvalues', metavar='FILE', type=str,
      dest='eig_filename', default=None, help='The file for storing the eigenvalues.')
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
  if args.n_outputs: pca_n_outputs = args.n_outputs
  else: pca_n_outputs = config.pca_n_outputs
  if args.protocol: protocol = args.protocol
  else: protocol = config.protocol
  # Directories containing the features and the PCA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.lbph_features_dir)
  if args.pca_dir: pca_dir = args.pca_dir
  else: pca_dir = config.features_base_dir
  if args.features_projected_dir: features_projected_dir = args.features_projected_dir
  else: features_projected_dir = config.features_projected_dir
  if args.pca_model_filename: pca_model_filename = args.pca_model_filename
  else: pca_model_filename = config.model_filename

  # Let's create the job manager
  if args.grid:
    from gridtk.manager import JobManager
    jm = JobManager()

  # Trains the LinearMachine
  cmd_pcatrain = [ 
                  './bin/pca_train.py', 
                  '--n-outputs=%d' % pca_n_outputs,
                  '--config-file=%s' % args.config_file, 
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--pca-dir=%s' % pca_dir,
                  '--pca-model-filename=%s' % pca_model_filename,
                  '--protocol=%s' % protocol,
                 ]
  if args.eig_filename: cmd_pcatrain.append('--eigenvalues=%s' % args.eig_filename)
  if args.force: cmd_pcatrain.append('--force')
  if args.grid: 
    cmd_pcatrain.append('--grid')
    job_pcatrain = utils.submit(jm, cmd_pcatrain, dependencies=[], array=None, queue='q1d', mem='8G', hostname='!cicatrix')
    print('submitted: %s' % job_pcatrain)
  else:
    print('Running PCA training...')
    subprocess.call(cmd_pcatrain)

  # Project the data
  cmd_pcaproject = [ 
                    './bin/linear_project.py', 
                    '--config-file=%s' % args.config_file, 
                    '--output-dir=%s' % args.output_dir,
                    '--features-dir=%s' % features_dir,
                    '--features-projected-dir=%s' % features_projected_dir,
                    '--algorithm-dir=%s' % pca_dir,
                    '--model-filename=%s' % pca_model_filename,
                    '--protocol=%s' % protocol,
                   ]
  if args.force: cmd_pcaproject.append('--force')
  if args.grid: 
    cmd_pcaproject.append('--grid')
    import math
    # Database python objects (sorted by keys in case of SGE grid usage)
    inputs_list = config.db.objects(protocol=protocol)
    # Number of array jobs
    n_array_jobs = int(math.ceil(len(inputs_list) / float(config.n_max_files_per_job)))  
    job_pcaproject = utils.submit(jm, cmd_pcaproject, dependencies=[job_pcatrain.id()], array=(1,n_array_jobs,1), queue='q1d', mem='2G', hostname='!cicatrix')
    print('submitted: %s' % job_pcaproject)
  else:
    print('Running PCA projection...')
    subprocess.call(cmd_pcaproject)

if __name__ == "__main__": 
  main()
