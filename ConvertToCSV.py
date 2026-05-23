########################################################################################################################
# Copyright (c) Martin Bustos @FronkonGames <fronkongames@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
########################################################################################################################
__author__ = "Martin Bustos <fronkongames@gmail.com>"
__copyright__ = "Copyright 2022, Martin Bustos"
__license__ = "MIT"
__version__ = "1.1.0"
__email__ = "fronkongames@gmail.com"

import sys
import os
import json
import argparse

def ProgressBar(count, total):
  bar_len = 50
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '█' * filled_len + '░' * (bar_len - filled_len)

  sys.stdout.write(f'{bar} {percents}%\r')
  sys.stdout.flush()

def WriteString(app, key, default = ''):
  value = default
  if key in app and app[key] != None and app[key] != '':
    value = str(app[key]).replace('"', '').replace('\n', ' ').replace('\r', ' ').strip()
  return f'"{value}"'

def WriteRawValue(app, key):
  if key in app and app[key] != None:
    value = str(app[key]).replace('"', '').replace('\n', ' ').replace('\r', ' ').strip()
    return f'"{value}"'
  return '""'

print(f'Convert JSON to CSV {__version__} by {__author__}.')
parser = argparse.ArgumentParser(description='Convert JSON to CSV.')
parser.add_argument('-f', '--file', type=str, default='games.json', help='Dataset file name')
args = parser.parse_args()

dataset = {}

filename = args.file
if os.path.exists(filename):
  print('Loading dataset.')
  with open(filename, 'r', encoding='utf-8') as fin:
    text = fin.read()
    if len(text) > 0:
      dataset = json.loads(text)

  print(f'Dataset with {len(dataset)} games loaded.')

  with open('games.csv', 'w', encoding="utf-8") as fin:
    # Included ReleaseDate as a separate column header
    header = [
      'AppID',
      'Title',
      'ReleaseDate',
      'GameType',
      'BasePrice',
      'ReviewClass'
    ]

    fin.write(','.join(header) + '\n')

    count = 0
    total = len(dataset)
    for appID in dataset:
      app = dataset[appID]

      # Maps strictly to the raw properties inside games.json
      data = f"{appID},"
      data += f"{WriteString(app, 'name')},"
      data += f"{WriteRawValue(app, 'release_date')}," # Drops in the raw release date string directly
      data += f"{WriteRawValue(app, 'type')},"         
      data += f"{WriteRawValue(app, 'price')},"        
      data += f"{WriteString(app, 'reviews_class')}"
      data += "\n"

      fin.write(data)
      count += 1
      ProgressBar(count, total)
  
  print('\nDone. Successfully generated un-filtered games.csv mirror with Release Dates!')
else:
  print(f'Dataset file \'{args.file}\' not found.')