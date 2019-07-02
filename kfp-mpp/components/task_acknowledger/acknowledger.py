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
"""task_acknowledger component source code."""

import argparse

def acknowledge_task(task_id):
  print("Task {} succeeded.".format(task_id))


def main(args):
  print('Acknowledge task...')
  acknowledge_task(args.task_id)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--task-id", type=str)
  args = parser.parse_args()
  main(args)
