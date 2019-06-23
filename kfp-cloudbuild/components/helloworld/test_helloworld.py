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
"""Helloworld component unit tests."""

import unittest
import helloworld


class TestSum(unittest.TestCase):

    def test_greetings(self):
        self.assertEqual(helloworld.greetings('Google'), "Hello Google!!")


if __name__ == '__main__':
    unittest.main()
