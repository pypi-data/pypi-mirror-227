#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

from dataclasses import dataclass, field
from typing import List, Optional

import bbutil
from bbutil.app.module import Module
from bbutil.utils import get_attribute

__all__ = [
    "ModuleManager"
]


@dataclass
class ModuleManager(object):

    module_path: str = ""
    modules: List[Module] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)

    def init(self) -> bool:

        try:
            _commands = get_attribute(self.module_path, "__all__")
        except ImportError as e:
            bbutil.log.error("Unable to find commands: {0:s}".format(self.module_path))
            return False

        for _name in _commands:
            _module = Module()

            check = _module.init(self.module_path, _name)
            if check is False:
                continue

            self.commands.append(_module.command)
            self.modules.append(_module)
        return True

    def has_command(self, command: str) -> bool:
        if command in self.commands:
            return True
        return False

    def get_command(self, command_id: str) -> Optional[Module]:

        for _module in self.modules:
            if _module.command == command_id:
                return _module
        return None
