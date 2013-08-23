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

import os
import bob
import numpy
from . import utils

def _parse_annotations(pos_input_k):
  """Parse annotations in Multi-PIE format"""

  if not os.path.exists(pos_input_k):
    raise IOError("The annotation file '%s' was not found" % pos_input_k)

  f = open(pos_input_k, 'r')
  annotations = {}
  count = int(f.readline())

  if count == 16:
    # frontal image annotations
    labels = ['reye', 'leye', 'reyeo', 'reyei', 'leyei', 'leyeo', 'nose', 'mouthr', 'mouthl', 'lipt', 'lipb', 'chin', 'rbrowo', 'rbrowi', 'lbrowi', 'lbrowo']
  else:
    raise ValueError("The number %d of annotations in file '%s' is not handled." % (count, file_name))

  for i in range(count):
    line = f.readline()
    positions = line.split()
    assert len(positions) == 2
    annotations[labels[i]] = (float(positions[1]), float(positions[0]))

  rh = annotations['reye'][0]
  rw = annotations['reye'][1]
  lh = annotations['leye'][0]
  lw = annotations['leye'][1]

  return (rh, rw, lh, lw)

def extract_lbph(inputs_list, # File objects from the database
                 img_input_dir, img_input_ext, # images
                 pos_input_dir, pos_input_ext, # annotations
                 features_dir, features_ext,   # features (output)
                 crop_eyes_d, crop_h, crop_w, crop_oh, crop_ow,       # cropping
                 gamma, sigma0, sigma1, size, threshold, alpha,       # Tan Triggs
                 radius, p_n, circular, to_average, add_average_bit,  # LBP
                 uniform, rot_inv,
                 block_h, block_w, block_oh, block_ow,                # Histogram
                 force):

  # Initializes cropper and destination array
  fen = bob.ip.FaceEyesNorm( crop_eyes_d, crop_h, crop_w, crop_oh, crop_ow)
  cropped_img = numpy.ndarray(shape=(crop_h,crop_w), dtype=numpy.float64)

  # Initializes the Tan and Triggs preprocessing
  tt = bob.ip.TanTriggs( gamma, sigma0, sigma1, size, threshold, alpha)
  preprocessed_img = numpy.ndarray(shape=(crop_h, crop_w), dtype=numpy.float64)

  # Initializes LBPHS processor
  lbphs = bob.ip.LBPHSFeatures( block_h, block_w, block_oh, block_ow, radius, p_n, circular, to_average, add_average_bit, uniform, rot_inv)

  # Processes the 'dictionary of files'
  for k in inputs_list: # Loops over the database File objects
    img_input_k = k.make_path(directory=img_input_dir, extension=img_input_ext)
    pos_input_k = k.make_path(directory=pos_input_dir, extension=pos_input_ext)
    features_k = k.make_path(directory=features_dir, extension=features_ext)
    if force == True and os.path.exists(features_k):
      print("Remove old features %s." % (features_k))
      os.remove(features_k)

    if os.path.exists(features_k):
      print("Features for sample %s already exists."  % (img_input_k))
    else:
      print("Computing features from sample %s." % (img_input_k))

      # Loads image file
      img_unk = bob.io.load( str(img_input_k) )
      
      # Converts to grayscale
      if(img_unk.ndim == 3):
        img = bob.ip.rgb_to_gray(img_unk)
      else:
        img = img_unk

      # Parse annotations
      rh, rw, lh, lw = _parse_annotations(pos_input_k)

      # Extracts and crops a face 
      fen(img, cropped_img, rh, rw, lh, lw) 
       
      # Preprocesses a face using Tan and Triggs
      tt(cropped_img, preprocessed_img)
      preprocessed_img_s = bob.core.convert(preprocessed_img, dtype=numpy.uint8, source_range=(-threshold,threshold))

      # Computes LBP histograms
      lbphs_blocks = lbphs(preprocessed_img_s)
      lbphs_array = numpy.hstack(lbphs_blocks).astype(numpy.float64)

      # Saves to file
      utils.ensure_dir(os.path.dirname(str(features_k)))
      bob.io.save(lbphs_array, str(features_k))


