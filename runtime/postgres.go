package runtime

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/golang-migrate/migrate/v4"
	migratepg "github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"gorm.io/gorm/schema"
)

func (r *Runtime) db() *Runtime {
	r.Logger.Info().Msg("Initiate connection to DB...")
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=disable TimeZone=Asia/Jakarta",
		r.Cfg.DBHost,
		r.Cfg.DBUser,
		r.Cfg.DBPassword,
		r.Cfg.DBName,
		r.Cfg.DBPort,
	)

	dbLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
		logger.Config{
			SlowThreshold: time.Second, // Slow SQL threshold
			LogLevel:      logger.Info, // Log level
			Colorful:      true,        // Disable color
		},
	)

	gormConfig := &gorm.Config{
		// enhance performance config
		PrepareStmt:            true,
		SkipDefaultTransaction: true,
		Logger:                 dbLogger,
		NamingStrategy: schema.NamingStrategy{
			SingularTable: true,
		},
	}

	db, err := gorm.Open(postgres.Open(dsn), gormConfig)
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error connect to DB")
		log.Fatalf("Error connect to DB : %v", err)
	}

	r.Db = db

	r.Logger.Info().Msg("DB successfully connected")

	return r
}

func (r *Runtime) MigrateUp() {
	r.prepareMigration("up")
}

func (r *Runtime) MigrateDown() {
	r.prepareMigration("down")
}

func (r *Runtime) prepareMigration(migrationType string) error {
	r.Logger.Info().Msgf("Initiate db migration %s", migrationType)

	m, err := r.prepareMigrator()
	if err != nil {
		return err
	}
	defer m.Close()

	switch migrationType {
	case "up":
		err = m.Up()
	case "down":
		err = m.Down()
	}
	if err != nil && err != migrate.ErrNoChange {
		r.Logger.Error().Err(err).Msgf("Error migration %s", migrationType)
		return err
	}
	if err == migrate.ErrNoChange {
		r.Logger.Info().Msg("No change migration")
		return nil
	}

	r.Logger.Info().Msgf("Migrating %s db has been done", migrationType)
	return nil
}

func (r *Runtime) ForceLastestVersion() error {
	m, err := r.prepareMigrator()
	if err != nil {
		return err
	}
	defer m.Close()

	version, _, err := m.Version()
	if err != nil {
		r.Logger.Error().Err(err).Msg("error get version")
		return err
	}

	err = m.Force(int(version))
	if err != nil {
		r.Logger.Error().Err(err).Msgf("error force version %d", version)
		return err
	}

	return nil
}

func (r *Runtime) prepareMigrator() (*migrate.Migrate, error) {
	sqlDB, err := r.Db.DB()
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error return sql.DB")
		return nil, err
	}
	defer sqlDB.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	sqlConn, err := sqlDB.Conn(ctx)
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error return connection db")
		return nil, err
	}
	defer sqlConn.Close()

	driver, err := migratepg.WithConnection(ctx, sqlConn, &migratepg.Config{})
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error create driver with connection")
		return nil, err
	}
	defer driver.Close()

	m, err := migrate.NewWithDatabaseInstance("file://./internal/migrations", "postgres", driver)
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error create new migrator")
		return nil, err
	}

	return m, nil
}

func (r *Runtime) CreateFileMigration(name string) error {
	version := time.Now().UTC().Format("20060102150405")
	nameWithVersion := version + "_" + name

	migrationTypes := []string{"up", "down"}
	for _, v := range migrationTypes {
		if err := r.createFile(nameWithVersion, v); err != nil {
			r.Logger.Error().Err(err).Msgf("error create file migration %s", v)
			return err
		}
	}

	return nil
}

func (r *Runtime) createFile(name, migrationType string) error {
	f, err := os.Create(fmt.Sprintf("./internal/migrations/%s.%s.sql", name, migrationType))
	if err != nil {
		r.Logger.Error().Err(err).Msg("Error create file")
		return err
	}
	defer f.Close()

	fmt.Println("Generated new migration files...", f.Name())
	return nil
}
