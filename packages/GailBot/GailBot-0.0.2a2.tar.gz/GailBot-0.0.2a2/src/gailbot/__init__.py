# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 14:55:34
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-28 14:34:58


__version__ = "0.0.2a2"

from .api import GailBot
from .core.engines import Engine, Watson, WatsonAMInterface, WatsonLMInterface
from .plugins import Plugin, Methods
from .services import GBPluginMethods, UttDict, UttObj
