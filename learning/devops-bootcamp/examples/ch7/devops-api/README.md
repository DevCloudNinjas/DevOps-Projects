# DevOps API

This documentation is used to get a better understanding of the DevOps API to be used for the custom terraform provider and see how the CRUD operations work.

API is composed of 4 resources:

```markdown
1. Engineer - an individual engineer
    - id (unique numeric or alphanumeric identifier)
    - name (string)
    - valid email address(string)

2. Dev - collection of developer engineers
    - id (unique numeric or alphanumeric identifier)
    - name (string)
    - engineers (list of engineer resources)

3. Ops - collections of operations engineers
    - id (unique numeric or alphanumeric identifier)
    - name (string)
    - engineers (list of engineer resources)

4. DevOps - combination of a collection of developer and operations engineers
    - id (unique numeric or alphanumeric identifier)
    - Devs (list of Dev resources)
    - Ops (list of Ops resources)
```

## How to start the API:

Run it on locally:
- This will build, test, and run the API in the foreground.
```bash
make run
```

Running it as a docker container:
- This will build, test the go code and then build the docker image then run it as a daemon process.
```bash
make docker-run
```

## How to use crud operations:

To make things a bit simpler we provided some scripts that go through CRUD operations for the resources.

These scripts are located in the `scripts` directory of this current directory.

All the scripts execute curl requests that the api receives.
Feel free to investigate and tinker with the scripts to have a better understanding client-side requests for the terraform custom provider.

Example call to creating new engineer resources from the script:

From current directory:
```bash
scripts/engineer.sh post
```

From scripts directory:
```bash
./engineer.sh post
```

This should send a POST request to the API that it will receive and return json pertaining to the new engineer made:

Example response:
- This is how the response from the api will look like when you create a new engineer resource.
```bash
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Date: Fri, 09 Dec 2022 17:16:21 GMT
Content-Length: 68

{
    "name": "bob",
    "id": "D7SJA",
    "email": "bob@bob.com"
}
```
