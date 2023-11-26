import itertools
from typing import Any, Iterator, List, Optional

from nltk_ext.pipelines.pipeline_module import PipelineModule


class Tee:
    """
    The tee module lets you split a pipeline into two separate paths
    The first path is the normal pipeline path, acting as an identity
    map.  The second path should be passed into the constructor.
    The iterators should be consumed roughly at the same rate or
    more memory will be used.
    """

    def __init__(self, module: PipelineModule) -> None:
        self.module = module

    def alternate(self) -> List[Any]:
        "get the alternate path"
        # TODO refactor these methods to use iterators instead of
        # consuming to a list.
        # return self.module.process_iterator(self.alt_stream)
        return list(self.module.process(list(self.alt_stream)))

    def process(self, source: Any, data: Optional[Any] = None) -> Iterator[str]:
        paths = itertools.tee(source)
        self.alt_stream = paths[1]
        return paths[0]
