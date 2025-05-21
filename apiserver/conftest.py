# Copyright 2025 Google LLC
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
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(scope="session", autouse=True)
def mock_google_cloud_logging_client():
    mock_client_instance = MagicMock()

    with patch(
        "app.google.cloud.logging.Client", return_value=mock_client_instance
    ) as mock_class:
        yield mock_class
