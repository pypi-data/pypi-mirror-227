from docarray import BaseDoc
from docarray.typing import AnyEmbedding, NdArray
# from .models import Namespace, Workspace
from docarray.documents import TextDoc
from docarray import DocList
from typing import Optional


class PreContext(BaseDoc):
    input: TextDoc
    output: TextDoc


class BaseContext(BaseDoc):
    input: str
    embedding: NdArray[384]
    output: Optional[str]
    # id: str
    # data: NdArray[384]
    # input: AnyEmbedding[512]
    # output: TextDoc


"""
class Context(BaseDoc):
    input: AnyEmbedding[512]
    context: AnyEmbedding[512]
    output: TextDoc


class QueryContext(BaseDoc):
    query: AnyEmbedding[512]
    input: AnyEmbedding[512]
    context: AnyEmbedding[512]
    output: TextDoc


class InstructContext(BaseDoc):
    instructions: AnyEmbedding[512]
    input: AnyEmbedding[512]
    context: AnyEmbedding[512]
    output: TextDoc


class Context(BaseDoc):
    namespace: str
    workspace: str
    ctx_id: str
    embedding: AnyEmbedding[512]
"""
