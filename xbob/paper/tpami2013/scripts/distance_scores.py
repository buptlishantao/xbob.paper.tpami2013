#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:56:53 CEST 2013
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
  """Compute scores using a distance approach"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config_multipie.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('-g', '--group', metavar='STR', type=str,
      dest='group', default='dev', help='Database group (\'dev\' or \'eval\') for which to retrieve models (defaults to "%(default)s").')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='output', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--features-dir', metavar='FILE', type=str,
      dest='features_dir', default=None, help='The directory where the features are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file, that is prepended by the given output directory and the protocol.')
  parser.add_argument('--algorithm-dir', metavar='FILE', type=str,
      dest='algorithm_dir', default='default_algorithm', help='The relative directory of the algorithm that will contain the models and the scores. It is appended to the given output directory and the protocol.')
  parser.add_argument('--distance', metavar='STR', type=str,
      dest='distance', default='euclidean', help='The distance to use, when computing scores.')
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
  # Directories containing the features and the PCA model
  if args.features_dir: features_dir = args.features_dir
  else: features_dir = os.path.join(args.output_dir, protocol, config.features_dir)
  if utils.check_string(args.group): groups = [args.group]
  else: groups = args.group

  # (sorted) list of models
  models_ids = sorted(config.db.model_ids(protocol=protocol, groups=args.group))

  # finally, if we are on a grid environment, just find what I have to process.
  probes_split_id = 0
  if args.grid:
    import math
    n_splits = 0
    found = False
    pos = int(os.environ['SGE_TASK_ID']) - 1
    for model_id in models_ids:
      n_probes_for_model = len(config.db.objects(groups=args.group, protocol=protocol, purposes='probe', model_ids=(model_id,)))
      n_splits_for_model = int(math.ceil(n_probes_for_model / float(config.n_max_probes_per_job)))
      if pos < n_splits + n_splits_for_model:
        models_ids = [model_id]
        probes_split_id = pos - n_splits
        found = True
        break
      n_splits += n_splits_for_model
    if found == False:
      raise RuntimeError("Grid request for job %d on a setup with %d jobs" % (pos, n_splits))


  sc_nonorm_filename = os.path.join(args.output_dir, protocol, args.algorithm_dir, config.scores_nonorm_dir, "scores-" + args.group)
  if args.force:
    print("Removing old scores file '%s'." % sc_nonorm_filename)
    utils.erase_if_exists(sc_nonorm_filename)
  elif not args.grid and os.path.exists(sc_nonorm_filename):
    print("Scores file '%s' already exists." % sc_nonorm_filename)
  else:
    # Loops over the model ids
    for model_id in models_ids:
      print("Computing score for model '%s'." % model_id)
      if args.grid:
        # Saves model_scores to text file
        sc_nonorm_filename = os.path.join(args.output_dir, protocol, args.algorithm_dir, config.scores_nonorm_dir, 
          args.group, str(model_id) + "_" + str(probes_split_id).zfill(4) + ".txt")
        if args.force:
          print("Removing old scores file '%s'." % sc_nonorm_filename)
          utils.erase_if_exists(sc_nonorm_filename)

      if args.grid and os.path.exists(sc_nonorm_filename):
        print("Scores file '%s' already exists." % sc_nonorm_filename)
      else:
        # Gets the probe sample list
        probe_filenames = sorted(config.db.objects(groups=args.group, protocol=protocol, purposes="probe", model_ids=(model_id,)), key=lambda f: f.path)
        
        # If we are on a grid environment, just keep the required split of samples
        if args.grid:
          probe_filenames_g = utils.split_list(probe_filenames, config.n_max_probes_per_job)
          probe_filenames = probe_filenames_g[probes_split_id]

        # Loads the probes
        (probe_tests, probe_client_ids) = utils.load_probes(probe_filenames, features_dir, config.features_ext)

        # Loads the client model
        model_path = os.path.join(args.output_dir, protocol, args.algorithm_dir, config.models_dir, str(model_id) + ".hdf5")
        model = utils.load_model(model_path)

        # Computes the scores of all the probes against the model and put them in A
        A = utils.compute_distance_scores(model, probe_tests, args.distance)

        # Saves model_scores to text file
        if args.grid:
          utils.save_scores_to_textfile(A, probe_filenames, model_id, sc_nonorm_filename)
        else:
          utils.save_scores_to_textfile(A, probe_filenames, model_id, sc_nonorm_filename, True)

if __name__ == "__main__": 
  main()
