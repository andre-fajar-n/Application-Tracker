package applicationtracker

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/go-openapi/errors"
	"github.com/rs/zerolog"
	"github.com/spf13/viper"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"gorm.io/gorm/schema"
)

func NewRuntime() *Runtime {
	rt := new(Runtime)

	rt = rt.config()

	rt = rt.db()

	rt = rt.logger()

	rt.runMigration()

	return rt
}

type Runtime struct {
	Db     *gorm.DB
	Cfg    *viper.Viper
	Logger zerolog.Logger
}

func (r *Runtime) db() *Runtime {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable TimeZone=Asia/Jakarta",
		r.Cfg.GetString("DB_HOST"),
		r.Cfg.GetString("DB_USER"),
		r.Cfg.GetString("DB_PASSWORD"),
		r.Cfg.GetString("DB_NAME"),
		r.Cfg.GetString("DB_PORT"),
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
			SingularTable: false,
		},
	}

	db, err := gorm.Open(postgres.Open(dsn), gormConfig)
	if err != nil {
		log.Panicf("Error connect to DB : %f", err)
	}

	r.Db = db

	return r
}

func (r *Runtime) config() *Runtime {
	cfg := viper.New()
	cfg.SetConfigFile(".env")
	err := cfg.ReadInConfig()
	if err != nil {
		log.Fatalf("Failed load config : %f", err)
	}
	
	r.Cfg = cfg

	return r
}

func (r *Runtime) logger() *Runtime {
	zerolog.SetGlobalLevel(zerolog.DebugLevel)
	zerolog.TimestampFieldName = "timestamp"
	zerolog.TimeFieldFormat = time.RFC3339Nano
	logger := zerolog.New(zerolog.ConsoleWriter{
		Out: os.Stdout,
	}).With().Timestamp().Caller().Logger()

	r.Logger = logger

	return r
}

func (r *Runtime) runMigration() {
	r.Db.AutoMigrate()
}

func (r *Runtime) SetError(code int, msg string, args ...interface{}) error {
	return errors.New(int32(code), msg, args...)
}

func (r *Runtime) GetError(err error) errors.Error {
	if v, ok := err.(errors.Error); ok {
		return v
	}

	return errors.New(http.StatusInternalServerError, err.Error())
}
