import feedparser
import ssl
import time
import datetime
import threading


# For use in News.refresh() ONLY
PORTALS = {
    'coindesk': {'url': 'https://feeds.feedburner.com/CoinDesk',
                 'feed': []},
    'cointelegraph': {'url': 'https://cointelegraph.com/rss',
                      'feed': []},
    'cryptocurrencynews': {'url': 'https://cryptocurrencynews.com/feed/',
                           'feed': []},
    'ccn': {'url': 'https://cryptocurrencynews.com/feed/',
            'feed': []},
    'newsbtc': {'url': 'https://www.newsbtc.com/rss',
                'feed': []},
    'bitcoinist': {'url': 'http://bitcoinist.net/feed/',
                   'feed': []}
    }
ALL_FEEDS = []


class News():

    def __init__(self):
        # Starting feedparser properly
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        self.PORTALS = [
            'coindesk', 'cointelegraph', 'cryptocurrencynews',
            'ccn', 'newsbtc', 'bitcoinist'
            ]
        self.coindesk = []
        self.cointelegraph = []
        self.cryptocurrencynews = []
        self.ccn = []
        self.newsbtc = []
        self.bitcoinist = []
        self.all = (self.coindesk + self.cointelegraph
                    + self.cryptocurrencynews + self.ccn
                    + self.newsbtc + self.bitcoinist)

        self.refresh()

    def collect_feed(self, portal):
        global PORTALS
        global ALL_FEEDS
        feed_raw = feedparser.parse(PORTALS[portal]['url'])['entries']
        feed_parsed = []
        for entry in feed_raw:
            feed_parsed.append({
                'authors': [x['name'] for x in entry['authors']],
                'link': entry['link'],
                'title': entry['title'],
                'summary': entry['summary'],
                'tags': [x['term'] for x in entry['tags']],
                'time': datetime.datetime.fromtimestamp(time.mktime(
                    entry.published_parsed))
                })
        ALL_FEEDS.extend(feed_parsed)
        PORTALS[portal]['feed'] = feed_parsed

    def refresh(self):
        for portal in PORTALS:
            thread = threading.Thread(target=self.collect_feed,
                                      args=[portal])
            thread.start()
        while any([len(PORTALS[x]['feed']) == 0 for x in PORTALS]):
            continue
        self.coindesk = PORTALS['coindesk']['feed']
        self.cointelegraph = PORTALS['cointelegraph']['feed']
        self.cryptocurrencynews = PORTALS['cryptocurrencynews']['feed']
        self.ccn = PORTALS['ccn']['feed']
        self.newsbtc = PORTALS['newsbtc']['feed']
        self.bitcoinist = PORTALS['bitcoinist']['feed']
        self.all = sorted(ALL_FEEDS, key=lambda k: k['time'], reverse=True)
