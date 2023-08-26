from typing import Optional
from ptrlib.arch.linux import *


def which(s: str) -> Optional[str]:
    # TODO: Separate Windows support based on running OS
    return which_linux(s)
