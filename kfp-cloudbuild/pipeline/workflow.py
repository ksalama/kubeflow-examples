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

# Create component factories
add_op = component_store.load_component('my_add')
divide_op = component_store.load_component('my_divide')

# Define pipeline
@dsl.pipeline(
  name='A Simple CI pipeline',
  description='Basic sample to show how to do CI with KFP using CloudBuild'
)
def pipeline(
  x_value: int=1,
  y_value: int=1,
  z_value: int=1,
):

  add_step = add_op(x_value=x_value, y_value=y_value)
  add_step.set_display_name('Add x and y')
  add_result = add_step.outputs
  sum_value = add_result['sum']
  with kfp.dsl.Condition(sum_value != 0):
    divide_step = divide_op(x_value=sum_value, y_value=z_value)
    divide_step.set_display_name('Divide sum by z')
    add_step2 = add_op(
      x_value=divide_step.outputs['quotient'],
      y_value=divide_step.outputs['remainder'])
    add_step2.set_display_name('Add quotient and remainder')



