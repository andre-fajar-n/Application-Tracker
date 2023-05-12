package rest

import (
	"applicationtracker"
	"applicationtracker/gen/models"
	"applicationtracker/gen/restapi/operations"
	"applicationtracker/internal/utils/jwt"
	"time"

	"github.com/go-openapi/errors"
)

func parseToken(rt *applicationtracker.Runtime, token string) (*jwt.Payload, error) {
	secret := rt.Cfg.JwtSecret
	maker, err := jwt.NewJWTMaker(secret)
	if err != nil {
		return nil, err
	}

	payload, err := maker.VerifyToken(token)
	if err != nil {
		return nil, rt.SetError(401, "Unauthorized: invalid API key token: %v", err)
	}

	return payload, nil
}

func verifySingleRole(payload *jwt.Payload, role string) (*models.Principal, error) {
	if payload.Role != role {
		return nil, errors.New(403, "Forbidden: insufficient API key privileges")
	}

	return &models.Principal{
		UserID:    payload.UserID,
		ExpiredAt: payload.ExpiredAt.Format(time.RFC3339),
		Email:     payload.Email,
	}, nil
}

func checkHasRole(rt *applicationtracker.Runtime, role, token string) (*models.Principal, error) {
	payload, err := parseToken(rt, token)
	if err != nil {
		return nil, err
	}

	p, err := verifySingleRole(payload, role)
	if err != nil {
		return nil, err
	}

	return p, nil
}

func Authorization(rt *applicationtracker.Runtime, api *operations.ApplicationTrackerServerAPI) {
	// api.HasRoleSuperAdminAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleSuperAdmin, token)
	// }

	// api.HasRoleAdminPartnerAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleAdminPartner, token)
	// }

	// api.HasRoleCustomerPersonalAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleCustomerPersonal, token)
	// }

	// api.HasRoleCustomerCorporateAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleCustomerCorporate, token)
	// }

	// api.HasRoleDriverPersonalAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleDriverPersonal, token)
	// }

	// api.HasRoleDriverCorporateAuth = func(token string) (*models.Principal, error) {
	// 	return checkHasRole(rt, auth.RoleDriverCorporate, token)
	// }
}
