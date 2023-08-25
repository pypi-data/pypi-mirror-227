#  Copyright 2022-2023 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from th2_data_services.interfaces import ISourceAPI


class ILwDPSourceAPI(ISourceAPI):
    """Interface for Source API of lwdp-data-provider."""

class IHTTPSourceAPI(ILwDPSourceAPI):
    """Interface for Source API of lwdp-data-provider which works via HTTP."""
