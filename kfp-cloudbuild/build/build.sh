#!/usr/bin/env bash
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
"""Execute the cloud build steps."""

# Create the kfp-util docker container image
docker build -t gcr.io/ml-cicd-template/kfp-util:latest .
gcloud docker -- push gcr.io/ml-cicd-template/kfp-util:latest

# Set substitutions
SUBSTITUTIONS=\
_REPO_URL='https://source.developers.google.com/p/ml-cicd-template/r/kfp-helloworld',\
_REPO_NAME='kfp-helloworld',\
_PROJECT_ID='ml-cicd-template',\
_COMPUTE_ZONE='europe-west1-b',\
_CLUSTER_NAME='kubeflow-cluster',\
_GCS_LOCATION='ml-cicd-template/helloworld/pipelines',\
_EXPERIMENT_NAME='helloworld-dev',\
_TAG='latest'

# Submit the build job
gcloud builds submit --no-source --config cloudbuild.yaml \
--substitutions $SUBSTITUTIONS