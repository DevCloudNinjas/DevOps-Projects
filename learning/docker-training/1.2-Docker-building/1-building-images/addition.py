import web

urls = (
    '/add/(.*?)/(.*?)', 'add'
)
app = web.application(urls, globals())



class add:        
    def GET(self, a, b):
        return "{0} + {1} = {2}".format(a, b, (int(a) + int(b)))

if __name__ == "__main__":
    app.run()
