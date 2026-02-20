# makefile for devops api project this is required for building and running
.PHONY: clean

export GIN_MODE=release

run: clean main.go build
	./devops-api

build: main.go tidy fmt test
	go build

tidy: main.go
	go mod tidy

fmt: main.go
	go fmt

test: main.go
	go test -v

docker: fmt test
	docker build . -t devops-api:v1

docker-run: docker
	docker run -d -p 8080:8080 -t devops-api:v1

clean:
	rm -rf devops-api
