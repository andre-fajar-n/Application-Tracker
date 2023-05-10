.PHONY: generate build run doc validate spec clean help

all: clean generate build

validate:
	swagger validate ./api/application-tracker/swagger.yml

spec:
	swagger generate spec -o ./api/application-tracker/swagger-gen.yml

build: 
	CGO_ENABLED=0 GOOS=linux go build -v -installsuffix cgo ./cmd/application-tracker-server
	
run:
	./application-tracker-server --port=7070 --host=0.0.0.0 --config=./configs/app.yaml

run-local:
	go run cmd/application-tracker-server/main.go --port=7070

doc: validate
	swagger serve api/application-tracker/swagger.yml --no-open --host=0.0.0.0 --port=7070 --base-path=/

clean:
	rm -rf application-tracker-server
	go clean -i .

generate: validate
	go generate ./...

help:
	@echo "make: compile packages and dependencies"
	@echo "make validate: OpenAPI validation"
	@echo "make spec: OpenAPI Spec"
	@echo "make clean: remove object files and cached files"
	@echo "make build: Generate Server and Client API"
	@echo "make doc: Serve the Doc UI"
	@echo "make run: Serve binary file"
	@echo "make run-local: Serve main.go"