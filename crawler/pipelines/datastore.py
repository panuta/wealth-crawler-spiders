import uuid

from google.cloud import datastore


class DatastorePipeline:
    KIND_NAME = 'MutualFund'
    DATASTORE_BATCH_LIMIT = 500

    def __init__(self, crawler):
        self.item_count = None
        self.batches = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.item_count = 0
        self.client = datastore.Client()
        self.batches = [self.client.batch(), ]
        self.batches[0].begin()

    def process_item(self, item, spider):
        self.item_count += 1
        current_batch = self.batches[int((self.item_count - 1) / DatastorePipeline.DATASTORE_BATCH_LIMIT)]

        item_dict = dict(item)
        entity = datastore.Entity(self.client.key(self.KIND_NAME, str(uuid.uuid4())),
                                  exclude_from_indexes=item.exclude_from_indexes)
        entity.update(item_dict)
        current_batch.put(entity)

        if self.item_count % DatastorePipeline.DATASTORE_BATCH_LIMIT == 0:
            current_batch.commit()

            new_batch = self.client.batch()
            new_batch.begin()
            self.batches.append(new_batch)

        return item

    def close_spider(self, spider):
        if self.item_count % DatastorePipeline.DATASTORE_BATCH_LIMIT != 0:
            self.batches[-1].commit()
