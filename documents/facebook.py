import datetime
from typing import Any, Dict

from nltk_ext.documents.document import Document


class FacebookDocument(Document):
    BodyAttribute = "message"

    def time_to_int(self, time: datetime.datetime) -> int:
        return (time.hour * 60) + time.minute

    def __init__(self, data: Dict[str, Any]) -> None:
        self.length = 0
        data["created_time"] = datetime.datetime.strptime(
            data["created_time"], "%Y-%m-%dT%H:%M:%S+0000"
        ) + datetime.timedelta(hours=-8)
        time_as_int = self.time_to_int(data["created_time"])
        # print data["created_time"]
        d = {}
        d["time_as_int"] = time_as_int
        if "message" in data:
            d["message"] = data["message"]
            self.length = len(data["message"])
        d["metadata"] = data.copy()  # type: ignore[assignment]
        self.document = d.copy()  # type: ignore[assignment]
        if "id" in data:
            self.doc_id = data["id"]
        # super(FacebookDocument, self).__init__(data)
        Document.__init__(self, data)
        self.body_attribute = FacebookDocument.BodyAttribute
