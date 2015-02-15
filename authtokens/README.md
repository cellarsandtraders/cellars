# AuthTokens API

Endpoints for handling registration, logging in, logging out and authentication tokens. All POST data will be raw JSON. Once a user has authenticated, they will be identified by the HTTP Header Authentication, which contains their assigned session token.

Requests that result in errors have a response that will contain a JSON object with a single attribute, `error`.

**Example Error Response**

```
HTTP/1.0 400 BAD REQUEST
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json

{"error": "Invalid Data: column username is not unique"}
```


- [POST: `/api/register/`](#post-apiregister)
- [POST: `/api/login/`](#post-apilogin)
- [POST: `/api/logout/`](#post-apilogout)

### POST: `/api/register`

Submit credentials for registering a new user.

Param    | Description
-------- | ----------------
username | Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
password | Required. Raw passwords can be arbitrarily long and can contain any character.

**Example Usage**

```
POST /api/register/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{"username": "AzureDiamond", "password":"hunter2"}
```

**Example Response**

```
HTTP/1.0 201 CREATED
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json
```
```json
{
    "token": "d96163b8bc9127d8c5d5839018580123c64a324b",
    "user":   {
        "username": "AzureDiamond",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_active": true,
        "is_superuser": false,
        "is_staff": false,
        "last_login": "2015-01-04T22:51:35.144Z",
        "cellar": [1, 2, 3],
        "wants": [4, 5],
        "address": "123 N Main St.",
        "address2": "#100",
        "city": "Chicago",
        "state": "IL",
        "zipcode": "60647",
        "created": "2015-01-04T22:51:35.238Z",
        "modified": "2015-01-04T22:51:35.238Z",
        "date_joined": "2015-01-04T22:51:35.144Z"
    }
}
```


### POST: `/api/login`

Submit credentials authenticating an existing user.

Param    | Description
-------- | ----------------
username | Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
password | Required. Raw passwords can be arbitrarily long and can contain any character.

**Example Usage**

```
POST /api/login/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{"username": "AzureDiamond", "password":"hunter2"}
```

**Example Response**

```
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json
```
```json
{
    "token": "d96163b8bc9127d8c5d5839018580123c64a324b",
    "user":   {
        "username": "AzureDiamond",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_active": true,
        "is_superuser": false,
        "is_staff": false,
        "last_login": "2015-01-04T22:51:35.144Z",
        "cellar": [1, 2, 3],
        "wants": [4, 5],
        "address": "123 N Main St.",
        "address2": "#100",
        "city": "Chicago",
        "state": "IL",
        "zipcode": "60647",
        "created": "2015-01-04T22:51:35.238Z",
        "modified": "2015-01-04T22:51:35.238Z",
        "date_joined": "2015-01-04T22:51:35.144Z"
    }
}
```


### POST: `/api/logout`

Request to destroy the current authenticated session. Note the Authorization header is required. The logout request expects no body content.

**Example Usage**

```
POST /api/logout/ HTTP/1.1
Host: localhost:8000
Content-Length: 0
Authorization: Token d96163b8bc9127d8c5d5839018580123c64a324b
Content-Type: text/plain;charset=UTF-8

```

**Example Response**

```
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json

{"status": "success"}
```







