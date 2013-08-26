#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Sun Aug 25 13:32:56 CEST 2013
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
import sys

def download(url, output_file):
  """Downloads an URL and saves it to file"""
  if sys.version_info[0] < 3:
    # python2 technique for downloading a file
    from urllib2 import urlopen
    with open(output_file, 'wb') as out_file:
      response = urlopen(url)
      out_file.write(response.read())
  else:
    # python3 technique for downloading a file
    from urllib.request import urlopen
    from shutil import copyfileobj
    with urlopen(url) as response:
      with open(output_file, 'wb') as out_file:
        copyfileobj(response, out_file)

def extract_tbz2(input_filename, output_dir):
  """Extracts a .tar.gz2 file with the tarfile module"""
  import tarfile
  tgz_file = tarfile.open(input_filename, 'r:bz2')
  tgz_file.extractall(output_dir)

def _parse_jeval(input_filename, output_filename):
  import csv
  with open(input_filename, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    dlist = []
    count = 0
    for row in spamreader:
      # Skip the first two lines
      if count < 2:
        count += 1
        continue
      # Only keep the features (Not the location/scale of the keypoints)
      # And concatenate them in a 
      else:
        dlist.extend(row[5:])
    dlist = map(float, dlist)
    import bob
    bob.io.save(dlist, output_filename)

def db_parse_jeval(input_dir):
  suffix = '.jpg.pts.sift16.jeval'
  suffix_len = len(suffix)
  for c_dir in os.listdir(input_dir):
    client_dir = os.path.join(input_dir, c_dir)
    for f in os.listdir(client_dir):
      filename = os.path.join(client_dir, f)
      if filename.endswith(suffix):
        filename_noext = filename[:-suffix_len]
        filename_hdf5 = filename_noext + '.hdf5'
        print("Converting '%s' into hdf5 format" % filename)
        _parse_jeval(filename, filename_hdf5)
