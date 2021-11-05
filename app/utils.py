import random
from typing import List, Sequence


def create_password(symbols: Sequence[str] = [],
                    size: int = 5) -> List[str]:
    return random.choices(symbols, k=size)
