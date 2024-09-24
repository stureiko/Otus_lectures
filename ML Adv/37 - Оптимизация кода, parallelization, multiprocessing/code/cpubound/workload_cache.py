import os
import re
from functools import lru_cache
from pymorphy3 import MorphAnalyzer

regexp = re.compile(r'\w+')
morph = MorphAnalyzer()

@lru_cache
def get_normal_form(world: str) -> str:
    return morph.parse(world)[0].normal_form

def process_text(text: str) -> str:
    return ' '.join(
        map(
            lambda x: get_normal_form(str(x)), \
            regexp.findall(text)
        )
    )