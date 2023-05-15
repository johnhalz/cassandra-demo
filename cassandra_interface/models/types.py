from enum import Enum

class TMDSetting(Enum):
    '''TMD settings'''
    ON = 'ON'
    OFF = 'OFF'

class HardwareType(Enum):
    '''Hardware types'''
    AU = 'AU'
    MGC = 'MGC'
    VCM = 'VCM'
    INIT_SENSOR = 'Init Sensor'
    LEAF_SPRING = 'Leaf Spring'
    TMD = 'TMD'

class Mirror(Enum):
    '''Mirror number'''
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4
    M5 = 5
    M6 = 6
    M7 = 7
    M8 = 8
    RSFM = 9
    UNKNOWN = 'Unknown'

    def __str__(self) -> str:
        return self.name

class VCMSize(Enum):
    '''VCM sizes'''
    NORMAL = 'N'
    LARGE = 'L'
    UNKNOWN = 'Unknown'

class VCMPosition(Enum):
    '''VCM positions'''
    POSITION_1 = 1
    POSITION_2 = 2
    UKNOWN = 'Unknown'

class MGCSize(Enum):
    '''MGC sizes'''
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    UNKNOWN = 'Unknown'