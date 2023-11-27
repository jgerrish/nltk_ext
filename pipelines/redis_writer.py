import redis
from typing import Any, Callable, List, Optional, Tuple

from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class RedisWriter(PipelineModule):
    """
    Module to write data to a Redis key-value store
    Accepts an Redis operation to write the value,
    and a transform method to transform the data for writing.
    """

    def __init__(
        self,
        operation: str,
        custom_transform: Callable[[str], str],
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ) -> None:
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        if not operation:
            raise Exception("RedisWriter requires an operation")
        self.operation = operation
        if not custom_transform:
            raise Exception(
                "RedisWriter requires a transform method to transform the data for writing"  # noqa E501
            )
        self.custom_transform = custom_transform

    def _operation_to_redis_method(self, operation: str) -> Optional[Any]:
        "small set of restricted operations"
        if operation == "hset":
            return self.redis.hset
        elif operation == "sadd":
            return self.redis.sadd
        return None

    def apply(self, op: Callable[[Any], Any], args: Tuple[List[Any]]) -> None:
        for arg in args:
            op(arg)

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for s in elements:
            op = self._operation_to_redis_method(self.operation)
            if self.custom_transform:
                args = self.custom_transform(str(s))
            else:
                args = str(s)
            # args.insert(0, self.redis)
            # TODO Add a test for the below
            self.apply(op, tuple(args))  # type: ignore[arg-type]
            yield s
