package rest

import (
	"applicationtracker"
	"applicationtracker/gen/models"
	"applicationtracker/gen/restapi/operations"
	"applicationtracker/gen/restapi/operations/health"
	"applicationtracker/internal/handlers"

	"github.com/go-openapi/runtime/middleware"
)

func Route(rt *applicationtracker.Runtime, api *operations.ApplicationTrackerServerAPI, apiHandler handlers.Handler) {
	//  health
	api.HealthHealthHandler = health.HealthHandlerFunc(func(hp health.HealthParams) middleware.Responder {
		return health.NewHealthOK().WithPayload(&models.Success{
			Message: "Server up",
		})
	})

}
