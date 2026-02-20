
# install package web.py from pip
import web

# install package redis from pip
from redis import Redis

urls = (
    '/add/(.*?)/(.*?)', 'add',
    '/stats', 'stats'
)

app = web.application(urls, globals())
redis = Redis(host= "redis", port=6379)

class add:
    def GET(self, a, b):
        redis.incr('additions')
        return "{0} + {1} = {2}".format(a, b, (int(a) + int(b)))



class stats:
    def GET(self):
        return 'We have calculated {0} additions' . format (redis.get( 'additions' ))

if __name__ == "__main__":
    app.run()