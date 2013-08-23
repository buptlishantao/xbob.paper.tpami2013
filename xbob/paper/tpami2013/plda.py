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
import numpy
import os

def train(data, d, nf, ng, n_iter,
  seed, init_f_method, init_f_ratio, init_g_method, init_g_ratio, init_s_method, init_s_ratio):
  """Generates the PLDA base model from a list of Arraysets (one per identity),
     and a set of training parameters.
     Returns the trained PLDABaseMachine."""
  T = bob.trainer.PLDATrainer(n_iter)
  T.rng = bob.core.random.mt19937(seed)
  T.init_f_method = init_f_method
  T.init_f_ratio = init_f_ratio
  T.init_g_method = init_g_method
  T.init_g_ratio = init_g_ratio
  T.init_sigma_method = init_s_method
  T.init_sigma_ratio = init_s_ratio
  machine = bob.machine.PLDABase(d, nf, ng) 
  T.train(machine, data)
  return machine

def enroll_model(data, pldabase):
  """Enrols a PLDA Machine for a given identity using the provided arrayset
     and trained PLDABase."""
  machine = bob.machine.PLDAMachine(pldabase)
  trainer = bob.trainer.PLDATrainer()
  trainer.enrol(machine, data)
  return machine

def load_base_model(plda_model_filename):
  if not os.path.exists(plda_model_filename):
    raise RuntimeError("Cannot find PLDA Base Model %s" % (plda_model_filename))
  return bob.machine.PLDABase(bob.io.HDF5File(plda_model_filename))

def load_model(plda_model_filename, pldabase):
  if not os.path.exists(plda_model_filename):
    raise RuntimeError("Cannot find PLDAMachine %s" % (plda_model_filename))
  return bob.machine.PLDAMachine(bob.io.HDF5File(plda_model_filename), pldabase)

def compute_scores(machine, probe_tests):
  A = numpy.ndarray(shape=(len(probe_tests),), dtype=numpy.float64)
  for i in range(len(probe_tests)):
    A[i] = machine.forward(probe_tests[i])
  return A

