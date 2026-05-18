const http = require('http')
const { createServer } = require('./index')

test('GET /healthz returns ok payload', async () => {
  const server = createServer()
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve))
  const { port } = server.address()

  const response = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${port}/healthz`, resolve).on('error', reject)
  })
  const body = await new Promise((resolve) => {
    let data = ''
    response.on('data', (chunk) => { data += chunk })
    response.on('end', () => resolve(data))
  })
  server.close()

  expect(response.statusCode).toBe(200)
  expect(response.headers['content-type']).toBe('application/json')
  expect(JSON.parse(body)).toEqual({ status: 'ok' })
})
