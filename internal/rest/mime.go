package rest

import (
	"applicationtracker/gen/restapi/operations"

	"github.com/go-openapi/runtime"
)

func Mime(api *operations.ApplicationTrackerServerAPI) {
	api.JSONConsumer = runtime.JSONConsumer()
	api.JSONProducer = runtime.JSONProducer()
}
