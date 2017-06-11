import heapq
import itertools
import simplejson as json
from tornado import gen, ioloop, web, httpclient

HOTEL_PROVIDERS = ['expedia', 'orbitz', 'priceline', 'travelocity', 'hilton']


class ResultsHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        client= httpclient.AsyncHTTPClient()
        futures = []
        for provider in HOTEL_PROVIDERS:
            futures.append(
                client.fetch("http://127.0.0.1:9000/scrapers/{}".format(provider))
            )

        responses = yield gen.multi(futures)
        results = []
        for response in responses:
            # Put each hotel into a  2-tuple where the first value is it's ecstasy
            # and the second is the full hotel data
            # Sort by smalles ecstasy to greatest to use pythons merge heapq.merge
            results.append(list(reversed(
                [(hotel['ecstasy'], hotel) for hotel in json.loads(response.body)['results']]
            )))

        # Merge all the lists of results together and reverse the result so largest is first
        sorted_hotels = [hotel[1] for hotel in reversed(list(heapq.merge(*results)))]
        self.write({
            'results': sorted_hotels
        })


ROUTES = [
    (r"/hotels/search", ResultsHandler),
]


def run():
    app = web.Application(
        ROUTES,
        debug=True,
    )

    app.listen(8000)
    print "Server (re)started. Listening on port 8000"

    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run(
)
