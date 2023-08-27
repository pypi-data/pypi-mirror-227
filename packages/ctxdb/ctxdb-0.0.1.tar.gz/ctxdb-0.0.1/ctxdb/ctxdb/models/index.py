from docarray import BaseDoc
from typing import List


class Index(BaseDoc):
    idx: str | List[str]
