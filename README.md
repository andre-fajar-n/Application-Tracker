# Application-Tracker-BE

Backend Service of Application Tracker

# Built With

- [Go](https://go.dev/)
- [Go-Swagger](https://github.com/go-swagger/go-swagger)
- [Gorm](https://gorm.io/)

## Getting Started

1. Install Go and Go-Swagger on you device
2. Clone repository
3. Setup env file
4. Run the project 

## Running the app

```bash
$ make run
```

## Adding API

1. Edit swagger.yml File in api/swagger.yml. If you need help with swagger docs use the [Editor](https://swagger.io/docs/open-source-tools/swagger-editor/) and read the [Documentation](https://swagger.io/docs/specification/about/).
2. To Generate Routes and Validation from Swagger API run `make build`.

## Migrate table
1. Create definition of table in api/swagger.yml
2. Migrate table is using AutoMigrate from gorm
3. Add struct table to AutoMigrate in config/connector.go

## Seeder

- Create seeder file

    ```shell
    go run internal/seed/seeder.go filename
    ```

- Run below command to seed up

    ```shell
    cat ./internal/seed/*.sql | psql -h 127.0.0.1 -U root -d db_name
    ```