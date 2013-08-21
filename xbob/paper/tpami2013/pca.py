#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

import bob
import os

def train(data, n_outputs):
  """Generates the PCA covariance matrix"""
  print("Training LinearMachine using PCA (SVD)")
  T = bob.trainer.PCATrainer()
  machine, eig_vals = T.train(data)
  # Machine: get shape, then resize
  machine.resize(machine.shape[0], n_outputs)
  return (machine, eig_vals)

def project(data_in, machine, data_out):
  """Projects the data using the provided covariance matrix"""
  # Projects the data
  machine(data_in, data_out)

def load_model(pca_model_filename):
  if not os.path.exists(pca_model_filename):
    raise RuntimeError("Cannot find Linear PCA Machine %s" % (pca_model_filename))
  return bob.machine.LinearMachine(bob.io.HDF5File(pca_model_filename))

