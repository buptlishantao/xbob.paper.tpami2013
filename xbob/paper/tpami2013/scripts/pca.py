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

import argparse
import imp 
from .. import utils

def main():

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='STR', type=str,
      dest='features_dir', default=None, help='The subdirectory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--eigenvalues', metavar='FILE', type=str,
      dest='eig_filename', default=None, help='The file for storing the eigenvalues.')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)
  # Update command line options if required
  if not args.features_dir: features_dir = config.features_dir
  else: features_dir = args.features_dir
  if not args.pca_dir: pca_dir = config.pca_dir
  else: pca_dir = args.pca_dir


  # Let's create the job manager
  if args.grid:
    from gridtk.manager import JobManager
    jm = JobManager()

  # Trains the LinearMachine
  cmd_pcatrain = [ 
                  './bin/pca_train.py', 
                  '--config-file=%s' % args.config_file, 
                  '--output-dir=%s' % args.output_dir,
                  '--features-dir=%s' % features_dir,
                  '--pca-dir=%s' % pca_dir,
                 ]
  if args.eig_filename: cmd_pcatrain.append('--eigenvalues=%s' % args.eig_filename)
  if args.force: cmd_pcatrain.append('--force')
  if args.grid: 
    job_pcatrain = utils.submit(jm, cmd_pcatrain, dependencies=[], array=None, queue='q1d', mem='8G', hostname='!cicatrix')
    print('submitted: %s' % job_pcatrain)
  else:
    print('Running PCA training...')
    subprocess.call(cmd_pcatrain)


  # Project the data
  cmd_pcaproject = [ 
                    './bin/pca_project.py', 
                    '--config-file=%s' % args.config_file, 
                    '--output-dir=%s' % args.output_dir,
                    '--features-dir=%s' % features_dir,
                    '--pca-dir=%s' % pca_dir,
                   ]
  if args.force: cmd_pcaproject.append('--force')
  if args.grid: 
    job_pcaproject = utils.submit(jm, cmd_pcaproject, dependencies=[job_pcatrain.id()], array=None, queue='q1d', mem='2G', hostname='!cicatrix')
    print('submitted: %s' % job_pcaproject)
  else:
    print('Running PCA training...')
    subprocess.call(cmd_pcaproject)

if __name__ == "__main__": 
  main()
