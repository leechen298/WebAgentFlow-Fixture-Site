# Fixture Contract

## Site URL

Default frontend dev URL:

```text
http://127.0.0.1:5175
```

Default fixture API dev URL:

```text
http://127.0.0.1:8002
```

Browser-facing API path remains:

```text
/validation-api
```

## Stable Routes

```text
/
/login
/dashboard
/users
/runtime-observation
/runtime-observation/basic/login
/runtime-observation/basic/register
/runtime-observation/basic/sms-login
/runtime-observation/basic/search
/runtime-observation/basic/detail
/runtime-observation/basic/settings
/runtime-observation/basic/confirm
```

## Stable API

```text
POST /validation-api/login
GET /validation-api/users
GET /validation-api/users/{user_id}
GET /validation-api/users/meta/options
```

## Purpose

This site is an internal deterministic fixture for WebAgentFlow validation and regression.

It may contain:

- authored specs
- fixture seed data
- stable test IDs
- stable route surfaces
- deterministic local backend behavior

It is not a product-like black-box validation site.
