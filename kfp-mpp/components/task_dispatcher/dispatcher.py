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
"""task_dispatcher component source code."""

import argparse
import json
from pathlib import Path


def dispatch_tasks(tasks_path):
  tasks = [
    {
      'task_id': task_id,
      'task-param1': 'task-'+str(task_id)+'-v1',
      'task-param2': 'task-' + str(task_id)+'-v2'
    }
    for task_id in range(5)
  ]

  # Write output to file
  task_json = json.dumps(tasks)
  Path(tasks_path).parent.mkdir(parents=True, exist_ok=True)
  Path(tasks_path).write_text(task_json)


def main(args):
  dispatch_tasks(args['tasks_path'])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--tasks-path", type=str)
  args = parser.parse_args()
  main(args)
