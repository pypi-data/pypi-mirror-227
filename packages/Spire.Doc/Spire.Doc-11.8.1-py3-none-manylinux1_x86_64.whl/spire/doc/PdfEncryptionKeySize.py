from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfEncryptionKeySize(Enum):
    """
    <summary>
        Specifies length of the encryption key for encryption.
    </summary>
    """
    Key40Bit = 1
    Key128Bit = 2
    Key256Bit = 3

