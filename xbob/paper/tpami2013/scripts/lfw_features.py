#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Sun Aug 25 13:38:00 CEST 2013
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
from .. import utils, lfw_features

def main():
  """Download, extract and converts the features into HDF5"""
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('--input-url', metavar='FILE', type=str,
      dest='input_url', default='http://lear.inrialpes.fr/people/guillaumin/data/lfw/lfw_funneled_sfd.tar.bz2', help='The URL of the LFW SIFT features to download.')
  parser.add_argument('--output-dir', metavar='FILE', type=str,
      dest='output_dir', default='database', help='The base output directory for everything (features, models, scores, etc.).')
  parser.add_argument('-f', '--force', dest='force', action='store_true',
      default=False, help='Force to erase former data if already exist')
  parser.add_argument('--grid', dest='grid', action='store_true',
      default=False, help='It is currently not possible to paralellize this script, and hence useless for the time being.')
  args = parser.parse_args()

  # Loads the configuration
  utils.ensure_dir(args.output_dir)
  dl_filename = os.path.join(args.output_dir, 'lfw_funneled_sfd.tar.bz2')
  lfw_features.download(args.input_url, dl_filename)
  lfw_features.extract_tbz2(dl_filename, args.output_dir)
  lfw_features.db_parse_jeval(os.path.join(args.output_dir, 'lfw_funneled'))

if __name__ == "__main__": 
  main()
