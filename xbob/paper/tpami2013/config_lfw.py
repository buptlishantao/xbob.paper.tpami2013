#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Sun Aug 25 15:16:16 CEST 2013
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
import bob
import xbob.db.verification.filelist

# Directories and extensions
## features
features_base_dir = 'database'
sift_features_dir = os.path.join(features_base_dir, 'lfw_funneled')
features_projected_dir = 'features'
## PCA
pca_dir = 'pca'
features_dir = os.path.join(pca_dir, features_projected_dir)
features_ext = '.hdf5'
## models and scores
model_filename = 'model.hdf5'
models_dir = 'models'
scores_nonorm_dir = 'scores'
## Algorithms
## PLDA
plda_dir = 'plda'


# Database/protocol to use
protocol = 'view1'
db = xbob.db.verification.filelist.Database('xbob/paper/tpami2013/protocol/lfw/', use_dense_probe_file_list=False)

# PCA
pca_n_outputs = 200

# PLDA
plda_nf = 48 
plda_ng = 48
plda_n_iter = 200 
plda_seed = 0
plda_init_f_method = bob.trainer.PLDATrainer.BETWEEN_SCATTER
plda_init_f_ratio = 1.
plda_init_g_method = bob.trainer.PLDATrainer.WITHIN_SCATTER
plda_init_g_ratio = 1.
plda_init_s_method = bob.trainer.PLDATrainer.VARIANCE_DATA
plda_init_s_ratio = 1.

# Grid options
n_max_files_per_job = 500
n_max_probes_per_job = 5000

