# Best Practices

---
## Cloud Native applications

- Case: Start app that requires access to database

#### Solution

1. Start up script that waits for db to be accessible
1. Start the actual application
1. Handle missing database gracefully!

---
# Patterns

---
## Microservice chassis
#### Must have in service

- Externalized configuration |
- Logging |
- Health checks |
- Metrics |
- Distributed tracing |

---
## API Gateway / Backend for Front-End

---
## Circuit Breaker

---
## Access Token

---
## Health check API / Canary API

--- 
## Service instance per Container

---
## Questions