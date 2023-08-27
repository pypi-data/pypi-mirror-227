# from ..models import Namespace, Workspace, Context
from ctxdb.models import BaseContext
from ctxdb.core.config import settings
# from docarray.index import RedisDocumentIndex, InMemoryExactNNIndex
# from docarray.index import InMemoryExactNNIndex
#from ctxdb.transformers import transformer
# from docarray import DocList
#from typing import List


class ContextDB:

    def __init__(self, db_type: str = "in_memory"):
        self.setup_backend(db_type)
        print("Hello World")

    def setup_backend(self, db_type):
        if db_type == "in_memory":
            try:
                from docarray.index import InMemoryExactNNIndex
                self._ctx_idx = InMemoryExactNNIndex[BaseContext]()
            except ImportError:
                raise ImportError(
                    "Please install docarray[index] to use ContextDB")
        elif db_type == "redis":
            try:
                from docarray.index import RedisDocumentIndex
                self._ctx_idx = RedisDocumentIndex[BaseContext](
                    host=settings.host,
                    port=settings.port,
                    password=settings.password)
            except ImportError:
                raise ImportError(
                    "Please install docarray[redis] to use ContextDB")
        else:
            raise NotImplementedError(f"{db_type} is not supported")

    def add_context(self, ctx: BaseContext):
        if isinstance(ctx, BaseContext):
            self._ctx_idx.index(ctx)
        else:
            raise TypeError(f"{type(ctx)} is not supported")

    def get_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            return self._ctx_idx[ctx_id]
        else:
            raise TypeError(f"{type(ctx_id)} is not supported")

    def delete_context(self, ctx_id: str):
        if isinstance(ctx_id, str):
            del self._ctx_idx[ctx_id]
        else:
            raise TypeError(f"{type(ctx_id)} is not supported")

    def search_context(self,
                       query: BaseContext,
                       search_field: str,
                       limit: int = 10):
        if isinstance(query, BaseContext):
            return self._ctx_idx.find(query, search_field, limit)
        else:
            raise TypeError(f"{type(query)} is not supported")


"""


    def add_context(self, idx: str | List[str]):
        if isinstance(idx, str):
            self._ctx_idx.idx_ctx_(
                Context(idx=idx, ctx=transformer.encode(idx)))

    def get_context(self, idx: str | List[str]):
        if isinstance(idx, str):
            return self._ctx_idx[idx]
        elif isinstance(idx, list):
            return self._ctx_idx[idx[0:]]
        else:
            raise TypeError(f'{idx} is not a valid type')
        # return self._ctx_idx.get(idx)

    def delete_context(self, idx: str | List[str]):
        if isinstance(idx, str):
            del self._ctx_idx[idx]
            return True
        elif isinstance(idx, list):
            del self._ctx_idx[idx[0:]]
            return True
        else:
            raise TypeError(f'{idx} is not a valid type')
            return False

        # self._ctx_idx.delete(idx)

    def update_context(self, idx: str | List[str], ctx: Context):
        ctx.idx = idx
        self._ctx_idx.idx_ctx_(ctx)
        pass
        # self._ctx_idx.update(idx)

    def query(self, query: str, k: int = 5):
        matches, scores = self._ctx_idx.find(Context(
            idx=query, ctx=transformer.encode(query)),
                                             search_field='ctx',
                                             limit=k)
"""
