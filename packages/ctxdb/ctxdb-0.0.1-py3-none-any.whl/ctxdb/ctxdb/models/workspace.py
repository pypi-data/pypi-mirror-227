from docarray import BaseDoc
from .models import Namespace


class Workspace(BaseDoc):
    namespace: Namespace
    name: str
    description: str
