import re
from typing import Dict, Any, List, Tuple
from glasskit import ctx
from glasskit.uorm.db import ObjectsCursor, ObjectId
from glasskit.uorm.models.base_model import BaseModel
from elasticsearch.serializer import JSONSerializer
from ask.models.post import BasePost
from ask.models.tag import TAG_NAME_EXPRESSION

TAG_SEARCH_EXPR = re.compile(r"\[(" + TAG_NAME_EXPRESSION + r")\]")


class SearchCursor:

    class Iterator:
        def __init__(self, data):
            self.data = data
            self.idx = 0

        def __next__(self):
            if self.idx >= len(self.data):
                raise StopIteration

            while True:
                doc = self.data[self.idx]
                post = BasePost.find_one({"_id": ObjectId(doc["_id"])})
                self.idx += 1
                if post:
                    break
                if self.idx >= len(self.data):
                    raise StopIteration

            post._score = doc["_score"]
            return post

    def __init__(self, index, query):
        self.index = index
        self.query = query
        self._from = None
        self._limit = None
        self._response = None
        self._idx = 0

    def skip(self, num: int):
        if self._response:
            ctx.log.warn("search call has already been performed, may be a misuse of skip()")
            self._response = None
        self._from = num
        return self

    def limit(self, num: int):
        if self._response:
            ctx.log.warn("search call has already been performed, may be a misuse of limit()")
            self._response = None
        if self._response:
            self._response = None
        self._limit = num
        return self

    def _request(self):
        attrs = {
            "index": self.index,
            "body": self.query
        }
        if self._from:
            attrs["from_"] = self._from
        if self._limit:
            attrs["size"] = self._limit

        self._response = ctx.es.search(**attrs)

    def count(self) -> int:
        if self._response is None:
            self._request()
        return self._response["hits"]["total"]["value"]

    def __iter__(self):
        if self._response is None:
            self._request()
        return SearchCursor.Iterator(self._response["hits"]["hits"])


def search_posts_generic(query_string, tags=None):
    query: Dict[str, Any] = {
        "query": {
            "bool": {
                "should": {
                    "multi_match": {
                        "fields": ["body", "title"],
                        "query": query_string
                    }
                }
            }
        }
    }

    if tags:
        query["query"]["bool"]["filter"] = [{"term": {"tags": tag}} for tag in tags]

    return SearchCursor("posts", query)


def parse_query(query_string) -> Tuple[str, List[str]]:
    tags = TAG_SEARCH_EXPR.findall(query_string)
    query_string = TAG_SEARCH_EXPR.sub("", query_string).strip()
    return query_string, tags


def search_posts(query_string):
    query_string, tags = parse_query(query_string)
    return search_posts_generic(query_string, tags)


class MongoJSONSerializer(JSONSerializer):

    def default(self, data):

        if isinstance(data, ObjectId):
            return str(data)
        if isinstance(data, (ObjectsCursor, set)):
            return list(data)
        if isinstance(data, BaseModel):
            return data.to_dict()

        return JSONSerializer.default(self, data)
