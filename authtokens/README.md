# AuthTokens API

Endpoints for handling registration, logging in, logging out and authentication tokens. All POST data will be raw JSON. Errors simply contain a JSON object with a single attribute, `error`.

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

## POST: `/api/register`

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
Cache-Control: no-cache

{"username": "AzureDiamond", "password":"hunter2"}
```

**Example Response**

```
HTTP/1.0 201 CREATED
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json

{"username": "AzureDiamond", "token": "d96163b8bc9127d8c5d5839018580123c64a324b"}
```


## POST: `/api/login`

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
Cache-Control: no-cache

{"username": "AzureDiamond", "password":"hunter2"}
```

**Example Response**

```
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
Content-Type: application/json

{"username": "AzureDiamond", "token": "d96163b8bc9127d8c5d5839018580123c64a324b"}
```


## POST: `/api/logout`

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







