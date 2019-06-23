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
  local_search_paths='../components',
  url_search_prefixes='https://raw.githubusercontent.com/kubeflow/pipelines/3b938d664de35db9401c6d198439394a9fca95fa/components/gcp')

# Create component factories
helloworld_op = component_store.load_component('components/helloworld')
byeworld_op = component_store.load_component('components/byeworld')


# Define pipeline
@dsl.pipeline(
  name='Hello World CI pipeline',
  description='Basic sample to show how to do CI with KFP using CloudBuild'
)
def pipeline(
  name: str='world',
  iterations: int=1,
  skip_bye: bool=False
):

  helloworld_step = helloworld_op(name=name, iterations=iterations)
  with kfp.dsl.Condition(skip_bye == False):
    byeworld_step = byeworld_op(name=name, iterations=iterations)

  steps = [
    helloworld_step,
    byeworld_step
  ]



