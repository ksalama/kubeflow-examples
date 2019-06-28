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
"""Helper module to deploy and run pipelines."""

import yaml
import os
import pathlib
import kfp
import fire
from datetime import datetime

SETTINGS_FILENAME = 'settings.yaml'
HOST_URL = 'https://{}.endpoints.{}.cloud.goog/pipeline'
OUTPUT_PACKAGE_PATH = 'pipeline.tar.gz'
NAMESPACE = 'kubeflow'
EXPERIMENT_NAME = 'default-experiment'
PIPELINE_NAME = 'helloworld-pipeline'


def update_component_spec(repo_url, image_tag):
  """Update the image in the component.yaml files given the repo_url and image_tag."""

  for spec_path in pathlib.Path('components').glob('*/component.yaml'):
    spec = yaml.safe_load(pathlib.Path(spec_path).read_text())
    image_name = str(spec_path).split('/')[1]
    full_image_name = '{}/{}:{}'.format(repo_url, image_name, image_tag)
    spec['implementation']['container']['image'] = full_image_name
    pathlib.Path(spec_path).write_text(yaml.dump(spec))
    print('Component {} specs updated. Image:{}'.format(
      image_name, full_image_name))

def read_settings():
  """Read all the parameter values from the settings.yaml file."""
  settings_file = os.path.join(os.path.dirname(__file__), SETTINGS_FILENAME)
  flat_settings = dict()
  setting_sections = yaml.safe_load(pathlib.Path(settings_file).read_text())
  for sections in setting_sections:
      flat_settings.update(setting_sections[sections])
  return flat_settings


def deploy_pipeline(
  kfp_package_path, version, experiment_name, namespace, run):
 """Deploy and run the givne kfp_package_path."""

 pipeline_name = PIPELINE_NAME+"-"+version

 client = kfp.Client(namespace=namespace)

 pipeline = client.upload_pipeline(
   pipeline_package_path=kfp_package_path,
   pipeline_name=pipeline_name)
 pipeline_id = pipeline.id

 if run:
   run_id = 'run-' + datetime.now().strftime('%Y%m%d-%H%M%S')
   experiment = client.create_experiment(name=experiment_name)
   settings=read_settings()
   client.run_pipeline(
     experiment.id,
     job_name=run_id,
     pipeline_id=pipeline_id,
     params=settings)


def main(operation, **args):

  # Update Component Specs
  if operation == 'update-specs':
    print('Setting images to the component spec...')
    if 'repo_url' not in args:
      raise ValueError('repo_url has to be supplied.')
    repo_url = args['repo_url']
    image_tag = "latest"
    if 'image_tag' in args:
      image_tag = args['image_tage']
    update_component_spec(repo_url, image_tag)

  # Deploy Pipeline
  elif operation == 'deploy-pipeline':
    print('Running Kubeflow pipeline...')
    if 'package_path' not in args:
      raise ValueError('package_path has to be supplied.')
    package_path = args['package_path']

    if 'version' not in args:
      raise ValueError('version has to be supplied.')
    version = args['version']

    namespace = NAMESPACE
    if 'namespace' in args:
      namespace = args['namespace']

    experiment_name = EXPERIMENT_NAME
    if 'experiment' in args:
      experiment_name = args['experiment']

    run = 'run' in args

    deploy_pipeline(package_path, version, experiment_name, namespace, run)

  else:
    raise ValueError(
      'Invalid operation name: {}. Valid operations: update-specs | deploy-pipeline'.format(operation))


if __name__ == '__main__':
  fire.Fire(main)
