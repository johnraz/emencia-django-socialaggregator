import feedparser
from datetime import datetime

from django.conf import settings
from django.utils.text import slugify
from generic import GenericAggregator


class Aggregator(GenericAggregator):

    ACCESS_TOKEN = settings.EDSA_FB_FANPAGE_ACCESS_TOKEN

    datetime_format = "%a, %d %b %Y %H:%M:%S +0000"

    def init_connector(self):
        pass

    def search(self, query):
        res = feedparser.parse(query)
        datas = []
        for feed in res['entries']:
            date = datetime.strptime(feed['published'],
                                     self.datetime_format)
            content = feed['content'][0]
            if content['language']:
                language = content['language']
            else:
                language = ''
            data = {'social_id': feed['id'],
                    'name': feed['title'],
                    'slug': slugify(feed['title']),
                    'ressource_date': date,
                    'description': content['value'],
                    'language': language,
                    'media_url': feed['link'],
                    'media_url_type': 'url',
                    'author': feed['author'],
                    }
            datas.append(data)

        return datas