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

import os
import imp
import argparse
from .. import plda, utils

def main():

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-c', '--config-file', metavar='FILE', type=str,
      dest='config_file', default='xbob/paper/tpami2013/config.py', help='Filename of the configuration file to use to run the script on the grid (defaults to "%(default)s")')
  parser.add_argument('-g', '--group', metavar='STR', type=str,
      dest='group', default='dev', help='Database group (\'dev\' or \'eval\') for which to retrieve models (defaults to "%(default)s").')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='/idiap/temp/lelshafey/plda-multipie', help='The base output directory for everything (models, scores, etc.).')
  parser.add_argument('--pca-dir', metavar='STR', type=str,
      dest='pca_dir', default=None, help='The subdirectory where the PCA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--plda-dir', metavar='STR', type=str,
      dest='plda_dir', default=None, help='The subdirectory where the PLDA data are stored. It will overwrite the value in the configuration file if any. Default is the value in the configuration file.')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='If set, assumes it is being run using a parametric grid job. It orders all ids to be processed and picks the one at the position given by ${SGE_TASK_ID}-1')
  args = parser.parse_args()

  # Loads the configuration 
  config = imp.load_source('config', args.config_file)

  # Directories containing the features and the PCA model
  if args.pca_dir: pca_dir_ = args.pca_dir
  else: pca_dir_ = config.pca_dir
  features_projected_dir = os.path.join(args.output_dir, config.protocol, pca_dir_, config.features_projected_dir)
  if args.plda_dir: plda_dir_ = args.plda_dir
  else: plda_dir_ = config.plda_dir
  plda_model_filename = os.path.join(args.output_dir, config.protocol, plda_dir_, config.plda_model_filename)

  # (sorted) list of models
  models_ids = sorted([model.id for model in config.db.models(protocol=config.protocol, groups=args.group)])

  # finally, if we are on a grid environment, just find what I have to process.
  probes_split_id = 0
  if args.grid:
    import math
    n_splits = 0
    found = False
    pos = int(os.environ['SGE_TASK_ID']) - 1
    for model_id in models_ids:
      n_probes_for_model = len(config.db.objects(groups=args.group, protocol=config.protocol, purposes='probe', model_ids=(model_id,)))
      n_splits_for_model = int(math.ceil(n_probes_for_model / float(config.n_max_probes_per_job)))
      if pos < n_splits + n_splits_for_model:
        models_ids = [model_id]
        probes_split_id = pos - n_splits
        found = True
        break
      n_splits += n_splits_for_model
    if found == False:
      raise RuntimeError("Grid request for job %d on a setup with %d jobs" % (pos, n_splits))
  else:
    sc_nonorm_filename = os.path.join(args.output_dir, config.protocol, config.scores_nonorm_dir, "scores-" + args.group)
    utils.erase_if_exists(sc_nonorm_filename)

  # Loads the PLDABase
  pldabase = plda.load_base_model(plda_model_filename)
  
  # Loops over the model ids
  for model_id in models_ids:
    print("%s" % model_id)
    # Gets the probe sample list
    probe_filenames = config.db.objects(groups=args.group, protocol=config.protocol, purposes="probe", model_ids=(model_id,))
    
    # If we are on a grid environment, just keep the required split of samples
    if args.grid:
      probe_filenames_g = utils.split_list(probe_filenames, config.n_max_probes_per_job)
      probe_filenames = probe_filenames_g[probes_split_id]

    # Loads the probes
    (probe_tests, probe_client_ids) = utils.load_probes(probe_filenames, features_projected_dir, config.features_projected_ext)

    # Loads the client model
    model_path = os.path.join(args.output_dir, config.protocol, config.models_dir, str(model_id) + ".hdf5")
    machine = plda.load_model(model_path, pldabase)

    # Computes the scores of all the probes against the model and put them in A
    A = plda.compute_scores(machine, probe_tests)

    if args.grid:
      # Saves model_scores to text file
      sc_nonorm_filename = os.path.join(args.output_dir, config.protocol, config.scores_nonorm_dir, 
        args.group, str(model_id) + "_" + str(probes_split_id).zfill(4) + ".txt")
      utils.save_scores_to_textfile(A, probe_filenames, model_id, sc_nonorm_filename)
    else:
      sc_nonorm_filename = os.path.join(args.output_dir, config.protocol, config.scores_nonorm_dir, "scores-" + args.group)
      utils.save_scores_to_textfile(A, probe_filenames, model_id, sc_nonorm_filename, True)

if __name__ == "__main__": 
  main()
