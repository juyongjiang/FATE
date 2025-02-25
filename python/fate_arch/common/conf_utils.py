#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
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
#

import os
import filelock
from fate_arch.common import file_utils

SERVICE_CONF = "service_conf.yaml"
TRANSFER_CONF = "transfer_conf.yaml"


def conf_realpath(conf_name):
    conf_path = f"conf/{conf_name}"
    return os.path.join(file_utils.get_project_base_directory(), conf_path)


def get_base_config(key, default=None, conf_name=SERVICE_CONF):
    base_config = file_utils.load_yaml_conf(conf_path=conf_realpath(conf_name=conf_name)) or dict()
    return base_config.get(key, default)


def update_config(key, value, conf_name=SERVICE_CONF):
    conf_path = conf_realpath(conf_name=conf_name)
    if not os.path.isabs(conf_path):
        conf_path = os.path.join(file_utils.get_project_base_directory(), conf_path)
    with filelock.FileLock(os.path.join(os.path.dirname(conf_path), ".lock")):
        config = file_utils.load_yaml_conf(conf_path=conf_path) or dict()
        config[key] = value
        file_utils.rewrite_yaml_conf(conf_path=conf_path, config=config)
