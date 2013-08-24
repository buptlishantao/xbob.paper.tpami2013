#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Wed Aug 21 16:57:27 CEST 2013
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
import xbob.db.multipie

# Directories and extensions
## features
features_base_dir = 'features'
lbph_features_dir = os.path.join(features_base_dir, 'lbph')
features_projected_dir = 'lbph_projected'
features_dir = os.path.join(features_base_dir, features_projected_dir)
features_ext = '.hdf5'
## models and scores
model_filename = 'model.hdf5'
models_dir = 'models'
scores_nonorm_dir = 'scores'
## Algorithms
## PCA
pca_dir = 'pca'
## PLDA
plda_dir = 'plda'
## LDA
lda_dir = 'lda'


# Database/protocol to use
db = xbob.db.multipie.Database()
protocol = 'U'

# Features
## Cropping
crop_eyes_d = 33
crop_h = 80
crop_w = 64
crop_oh = 16
crop_ow = 32
## Tan Triggs
gamma = 0.2
sigma0 = 1.
sigma1 = 2.
size = 5
threshold = 10.
alpha = 0.1
## LBP histogram
radius = 2
p_n = 8
circular = True
to_average = False
add_average_bit = False
uniform = True
rot_inv = False
block_h = 10
block_w = 10
block_oh = 4
block_ow = 4

# PCA
pca_n_outputs = 500

# LDA
lda_n_outputs = 64

# PLDA
plda_nf = 128 
plda_ng = 64
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

