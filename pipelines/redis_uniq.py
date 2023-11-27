import redis
from typing import Iterator, List, Optional, Union

from nltk_ext.documents.document import Document


class RedisUniq(object):
    """
    Module to return uniq elements given a list of elements
    This module is backed by a Redis set object
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        set_name: str = "nltkext_uniqset",
    ) -> None:
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.set_name = set_name
        self.redis.delete(self.set_name)

    def __del__(self) -> None:
        self.redis.delete(self.set_name)

    def process(
        self,
        data: Union[List[str], List[Document]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, Document]]:
        for s in data:
            if not self.redis.sismember(self.set_name, str(s)):
                self.redis.sadd(self.set_name, str(s))
                yield s
