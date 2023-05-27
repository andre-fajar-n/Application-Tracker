.PHONY: generate build run doc validate spec clean help create-file-migration

all: clean spec generate build

validate:
	swagger validate ./api/application-tracker/index.yml

spec:
	swagger flatten ./api/application-tracker/index.yml -o=./api/application-tracker/result.yml --format=yaml --with-flatten=full

build: 
	CGO_ENABLED=0 GOOS=linux go build -o ./application-tracker -v -installsuffix cgo ./cmd/cli
	
run:
	./application-tracker api --port=8080 --host=0.0.0.0

run-local:
	go run cmd/application-tracker/main.go api --port=8080 --host=0.0.0.0

doc: validate
	swagger serve api/application-tracker/index.yml --no-open --host=0.0.0.0 --port=8080 --base-path=/

clean:
	# remove all files inside /gen/models except custom_fields_valuer_scanner.go
	find ./gen/models -mindepth 1 -name custom_fields_valuer_scanner.go -prune -o -exec rm -rf {} +
	rm -rf application-tracker
	rm -rf ./gen/rest
	go clean -i .

generate: validate
	swagger generate server --exclude-main -A server -t gen -f ./api/application-tracker/result.yml --principal models.Principal

create-file-migration:
	go run cmd/cli/main.go migration create $(Arguments)

migrate-up:
	go run cmd/cli/main.go migration up

migrate-down:
	go run cmd/cli/main.go migration down

migrate-force:
	go run cmd/cli/main.go migration force

help:
	@echo "make: compile packages and dependencies"
	@echo "make validate: OpenAPI validation"
	@echo "make spec: OpenAPI Spec"
	@echo "make clean: remove object files and cached files"
	@echo "make build: Generate Server and Client API"
	@echo "make doc: Serve the Doc UI"
	@echo "make run: Serve binary file"
	@echo "make run-local: Serve main.go"
	@echo "make create-file-migration: Create new file migration"
	@echo "make migrate-up: Migrate up"
	@echo "make migrate-down: Migrate down"
	@echo "make migrate-force: Fix dirty migration"

Arguments := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
