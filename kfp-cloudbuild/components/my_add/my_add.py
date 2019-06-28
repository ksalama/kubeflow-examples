# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""My_add component source code."""

import argparse
from pathlib import Path


def add(x: int, y: int) -> int:
  """Returns the sum of x and y."""
  result = x +  y
  return result


def main(args):
  x = int(args.x_value)
  y = int(args.y_value)
  result = add(x, y)
  print("Result: {}".format(result))

  # Write output to file
  Path(args.result_path).parent.mkdir(parents=True, exist_ok=True)
  Path(args.result_path).write_text(str(result))



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--x-value", type=int)
  parser.add_argument("--y-value", type=int)
  parser.add_argument("--result-path", type=str)
  args = parser.parse_args()
  main(args)