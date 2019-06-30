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
"""Pipeline workflow definition."""

import json
import kfp
import kfp.dsl as dsl

# Initialize component store
component_store = kfp.components.ComponentStore(
  local_search_paths=['components'])

# Create component factories
task_op = component_store.load_component('task')
task_manager_op = component_store.load_component('task_manager')

# Define pipeline
@dsl.pipeline(
  name='Tasks MPP',
  description='An example to show how to use KFP as an MPP executor'
)
def pipeline(

):

  dispatch_step = task_manager_op(
    operation='dispatch', task_id='dispatch-tasks')

  tasks_json = str(dispatch_step.outputs['tasks'].value)
  tasks_json = '{}' if tasks_json == 'None' else tasks_json
  tasks = json.loads(tasks_json)

  for task_id, task_args in tasks.items():
    task_step = task_op(task_id=task_id, task_args=task_args)
    task_step.set_display_name('Task: {}'.format(task_id))
    ack_step = task_manager_op(operation='ack', task_id=task_id)
    ack_step.set_display_name('Ack: {}'.format(task_id))