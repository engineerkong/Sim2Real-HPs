from __future__ import absolute_import
from enum import Enum
from collections import namedtuple

class TrainFrequencyUnit(Enum):
    STEP = u"step"
    EPISODE = u"episode"

TrainFreq = namedtuple("TrainFreq", ["frequency", "unit"])
