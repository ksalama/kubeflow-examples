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
"""My_divide component unit tests."""

import unittest
import my_divide


class TestMyDivide(unittest.TestCase):

    def test_divide(self):
        result = my_divide.divide(10, 3)
        self.assertEqual(result.quotient, 3)
        self.assertEqual(result.remainder, 1)


if __name__ == '__main__':
    unittest.main()
