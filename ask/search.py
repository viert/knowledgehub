from glasskit import ctx
from glasskit.uorm.db import ObjectsCursor, ObjectId
from glasskit.uorm.models.base_model import BaseModel
from elasticsearch.serializer import JSONSerializer


def search_posts_generic(query_string, start=0, limit=100):
    query = {
        "from": start, "size": limit,
        "_source": ["shard_id", "stream_id", "root_id", "body", "title", "type"],
        "query": {
            "multi_match": {
                "fields": ["body", "title"],
                "query": query_string
            }
        }
    }
    return ctx.es.search(index="posts", body=query)


def search_posts_by_tags(tag, start=0, limit=100):
    query = {
        "from": start, "size": limit,
        "_source": ["shard_id", "stream_id", "root_id"],
        "query": {
            "match": {
                "tags": tag
            }
        }
    }
    return ctx.es.search(index="posts", doc_type="post", body=query)


class MongoJSONSerializer(JSONSerializer):

    def default(self, data):

        if isinstance(data, ObjectId):
            return str(data)
        if isinstance(data, (ObjectsCursor, set)):
            return list(data)
        if isinstance(data, BaseModel):
            return data.to_dict()

        return JSONSerializer.default(self, data)
