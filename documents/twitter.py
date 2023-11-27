from dateutil import parser
from typing import Any, Dict

from nltk_ext.documents.document import Document


class TwitterDocument(Document):
    """Represents a tweet"""

    BodyAttribute = "text"

    def __init__(self, data: Dict[str, Any]) -> None:
        self.length = 0
        d = {}
        if "created_at" in data:
            # , "%Y-%m-%dT%H:%M:%S+0000") + \
            # data["created_time"] = datetime.datetime.strptime(
            #    data["created_at"]) + datetime.timedelta(hours=-8)
            data["created_time"] = parser.parse(data["created_at"])
            # time_as_int = self.time_to_int(data["created_time"])
            d["created_time"] = data["created_time"]
        # print data["created_time"]
        # d["time_as_int"] = time_as_int
        if "text" in data:
            d["text"] = data["text"]
            self.length = len(data["text"])
        d["metadata"] = data.copy()
        self.document = d.copy()
        if "id" in data:
            self.doc_id = str(data["id"])
        self.body_attribute = TwitterDocument.BodyAttribute
        Document.__init__(self, data)
