import redis
from nltk_ext.pipelines.pipeline_module import PipelineModule

class RedisWriter(PipelineModule):
    """
    Module to write data to a Redis key-value store
    Accepts an Redis operation to write the value,
    and a transform method to transform the data for writing.
    """
    def __init__(self, operation, custom_transform,
                 host='localhost', port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        if not operation:
            raise Exception("RedisWriter requires an operation")
        self.operation = operation
        if not custom_transform:
            raise Exception("RedisWriter requires a transform method to transform the data for writing")
        self.custom_transform = custom_transform

    def _operation_to_redis_method(self, operation):
        "small set of restricted operations"
        if operation == "hset":
            return self.redis.hset
        elif operation == "sadd":
            return self.redis.sadd

    def process(self, data=None):
        for s in data:
            op = self._operation_to_redis_method(self.operation)
            if self.custom_transform:
                args = self.custom_transform(s)
            else:
                args = data
            #args.insert(0, self.redis)
            apply(op, tuple(args))
            yield s
