#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .consumer import Consumer  # noqa F401
from .producer import Producer  # noqa F401

import logging

__version__ = '2.2308.2'

logging.getLogger('pika').propagate = False
