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
"""Byeworld component source code."""

import argparse


def greetings(name="world"):
  """Returns a Goodbye greeting message with the given name."""
  return "Goodbye {}!!".format(name)


def main(args):
  for i in range(args.iterations):
    print(i+1,':', greetings(args.name))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--name", type=str)
  parser.add_argument("--iterations", type=int)
  args = parser.parse_args()
  main(args)