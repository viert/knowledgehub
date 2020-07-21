from datetime import datetime

from glasskit.commands import Command
from glasskit import ctx

from ask.models.post import BasePost
from ask import force_init_app


POST_INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "normalizer": {
                "lower": {
                    "type": "custom",
                    "char_filter": [],
                    "filter": ["lowercase"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "russian",
            },
            "body": {
                "type": "text",
                "analyzer": "russian",
            },
            "tags": {
                "type": "keyword",
                "normalizer": "lower",
            },
            "type": {
                "type": "text",
            }
        }
    }
}


class Elastic(Command):

    def init_argument_parser(self, parser):
        subparsers = parser.add_subparsers(
            help="action to perform with index",
            dest="action"
        )
        idx = subparsers.add_parser("index", help="index documents")
        idx.add_argument("--all", "-a", action="store_true", default=False,
                         help="re-index from scratch")
        idx.add_argument("--drop", "-d", action="store_true", default=False,
                         help="drop existing index before re-indexing")

    @staticmethod
    def drop():
        t1 = datetime.now()
        ctx.es.indices.delete(index="posts", ignore=[400, 404])
        t2 = datetime.now()
        dt = (t2 - t1).total_seconds()
        ctx.log.info("Index dropped in %.3f seconds", dt)

    @staticmethod
    def prepare():
        t1 = datetime.now()
        ctx.es.indices.create(index="posts", body=POST_INDEX_SETTINGS)
        t2 = datetime.now()
        dt = (t2 - t1).total_seconds()
        ctx.log.info("Index set up in %.3f seconds", dt)

    def reindex(self):
        if self.args.all:

            if self.args.drop:
                self.drop()
                self.prepare()

            t1 = datetime.now()
            updated = 0
            created = 0
            for post in BasePost.find():
                doc = post.get_indexer_document()
                if doc is None:
                    continue
                resp = ctx.es.index(index="posts", id=post._id, body=doc)
                if resp["result"] == "created":
                    created += 1
                elif resp["result"] == "updated":
                    updated += 1
            t2 = datetime.now()
            dt = (t2 - t1).total_seconds()
            ctx.log.info("Posts full reindexing completed. Created %d, updated %d documents in %.3f seconds",
                         created, updated, dt)
        else:
            raise NotImplementedError("partial reindex is not implemented")

    def run(self):
        force_init_app()
        if ctx.es is None:
            ctx.log.error("elasticsearch is not configured properly, giving up")
            return
        if self.args.action == 'index':
            self.reindex()
