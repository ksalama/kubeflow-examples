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

import kfp
import kfp.dsl as dsl

# Initialize component store
component_store = kfp.components.ComponentStore(
  local_search_paths=['components'])

# Create component ops
task_dispatcher_op = component_store.load_component('task_dispatcher')
exec_task_op = component_store.load_component('task')
task_acknowledger_op = component_store.load_component('task_acknowledger')


def get_index_of_last_element(list_json: str) -> int:
  import json
  return len(json.loads(list_json)) - 1


get_index_of_last_element_op = kfp.components.func_to_container_op(
  get_index_of_last_element)


def get_element_by_index(tasks_json: str, index: int) -> str:
  import json
  data_list = json.loads(tasks_json)
  return json.dumps(data_list[index])


get_element_by_index_op = kfp.components.func_to_container_op(
  get_element_by_index)


def decrement(number: int) -> int:
  return number - 1


decrement_op = kfp.components.func_to_container_op(decrement)


# Define the loop
@dsl.graph_component
def loop(task_index_ref, tasks_json_ref):

  # Get task_args at task_index from the tasks_json
  task_args = get_element_by_index_op(tasks_json_ref, task_index_ref).output
  # Execute the task using the task_args
  task_step = exec_task_op(task_args=task_args)
  # Acknowledge the executed task
  task_acknowledger_op(task_id=task_step.output)
  # Decrement the task_index
  next_task_index_ref = decrement_op(task_index_ref).output
  # Check that the index is not less than 0
  with kfp.dsl.Condition(next_task_index_ref >= 0):
    # Iterate
    loop(next_task_index_ref, tasks_json_ref)


# Define pipeline
@dsl.pipeline(
  name='Tasks MPP',
  description='An example to show how to use KFP as an MPP executor'
)
def loop_pipeline(

):

  # Dispatch tasks from tasks source
  dispatch_step = task_dispatcher_op()

  # Get task arguments as list of maps
  tasks_json_ref = dispatch_step.outputs['tasks']
  # Point to the index of the last task in the list
  task_index_ref = get_index_of_last_element_op(tasks_json_ref).output
  # Execute the tasks by index, starting from the last one, and descending
  loop(task_index_ref, tasks_json_ref)
