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
"""Transcript audio file using Speech-to-text API."""

import argparse
import json
from pathlib import Path

# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types


def transcript_audio_file(gcs_uri, model):
  """Transcribes the audio file specified by the gcs_uri."""

  client = speech.SpeechClient()
  audio = types.RecognitionAudio(uri=gcs_uri)
  config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=16000,
    language_code='en-US',
    model=model
  )

  response = client.recognize(config, audio)
  return response.results

def upload_to_gcs(transcption_results, output_path):
  pass

def main(args):

  # # Get audio transcription
  # transcption_results=transcript_audio_file(
  #   gcs_uri=args.input_file, model=args.model)
  # # Upload transcription text to GCS
  # upload_to_gcs(transcption_results, args.output_path)

  task_args = json.loads(args.task_args)
  task_id = task_args.pop('task_id')
  print("Processing task {}...".format(task_id))
  for key, value in task_args.items():
    print("{} = {}".format(key, value))
  print("Task complete.")

  # Write output to file
  Path(args.task_id_path).parent.mkdir(parents=True, exist_ok=True)
  Path(args.task_id_path).write_text(task_id)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--task-args", type=str)
  parser.add_argument("--task-id-path", type=str)
  args = parser.parse_args()
  main(args)