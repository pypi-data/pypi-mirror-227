# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum

from . import errors

__all__ = [
    'APIType', 'convert_str_to_api_type', 'get_api_error',
    'get_base_url_for_api_type'
]


class APIType(enum.Enum):
    QIANFAN = 1
    YINIAN = 2


def convert_str_to_api_type(api_type_str: str) -> APIType:
    s = api_type_str.lower()
    if s == 'qianfan':
        return APIType.QIANFAN
    elif s == 'yinian':
        return APIType.YINIAN
    else:
        raise errors.UnsupportedAPITypeError(
            f"{repr(api_type_str)} cannot be recognized as an API type.")


def get_base_url_for_api_type(api_type: APIType) -> str:
    if api_type == APIType.QIANFAN:
        return "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop"
    elif api_type == APIType.YINIAN:
        return "https://aip.baidubce.com/rpc/2.0/ernievilg/v1"
    else:
        raise ValueError(f"Unrecoginzed API type: {api_type.name}")


def get_api_error(api_type: APIType, ecode: int, emsg: str) -> errors.APIError:
    if api_type == APIType.QIANFAN:
        if ecode == 2:
            return errors.ServiceUnavailableError(emsg)
        elif ecode == 6:
            return errors.PermissionError(emsg)
        elif ecode in (17, 18, 19):
            return errors.RequestLimitError(emsg)
        elif ecode == 110:
            return errors.InvalidTokenError(emsg)
        elif ecode == 111:
            return errors.TokenExpiredError(emsg)
        elif ecode == 336100:
            return errors.TryAgain(emsg)
        else:
            return errors.APIError(emsg)
    elif api_type == APIType.YINIAN:
        if ecode in (4, 13, 15, 17, 18):
            return errors.RequestLimitError(emsg)
        elif ecode == 110:
            return errors.InvalidTokenError(emsg)
        elif ecode == 111:
            return errors.TokenExpiredError(emsg)
        else:
            return errors.APIError(emsg)
    else:
        return errors.APIError(emsg)
