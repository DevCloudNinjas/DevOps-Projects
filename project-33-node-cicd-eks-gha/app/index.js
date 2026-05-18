const http = require('http')
const qs = require('querystring')
const calculator = require('./calculator')

const maxBodyBytes = Number.parseInt(process.env.MAX_BODY_BYTES || `${1024 * 1024}`, 10)

function createServer() {
  return http.createServer(function(request, response) {
    if (request.method === 'GET' && request.url === '/healthz') {
      response.writeHead(200, {'Content-Type': 'application/json'})
      response.end(JSON.stringify({status: 'ok'}))
      return
    }

    if (request.method === 'POST') {
      var body = ''
      request.on('data', function(data) {
        body += data
        if (Buffer.byteLength(body) > maxBodyBytes) {
          response.writeHead(413, {'Content-Type': 'text/plain'})
          response.end('Request body too large')
          request.destroy()
        }
      })

      request.on('end', function() {
        if (response.writableEnded) {
          return
        }
        const post = qs.parse(body)
        const numbers = post.numbers
        const result = calculator.add(numbers)
        response.writeHead(200, {'Content-Type': 'text/html'})
        response.end('Result: ' + result)
      })
    } else {
      var html = `
            <html>
                <body>
                    <h3>Input comma separated integers to add.</h3>
                    <form method="post" action="/">Numbers: 
                        <input type="text" name="numbers" />
                        <input type="submit" value="Add" />
                    </form>
                </body>
            </html>`
      response.writeHead(200, {'Content-Type': 'text/html'})
      response.end(html)
    }
  })
}

if (require.main === module) {
  const port = Number.parseInt(process.env.PORT || '3000', 10)
  const host = '0.0.0.0'
  const server = createServer()
  server.listen(port, host)
  console.log(`Listening at http://${host}:${port}`)
}

module.exports = { createServer }
