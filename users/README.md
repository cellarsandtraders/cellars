# User API

Endpoints for handling User Profile objects


- [GET: `/api/users/`](#get-apiusers)
- [GET: `/api/users/:username`](#get-apiusersusername)
- [POST: `/api/users/:username`](#post-apiusersusername)

### GET: `/api/users`

Get a list of all active users.

**Example Usage**

```
GET /api/users HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
```

**Example Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json
[
  {
    "fields": {
      "username": "adam",
      "first_name": "",
      "last_name": "",
      "email": "",
      "is_active": true,
      "is_superuser": false,
      "is_staff": false,
      "last_login": "2015-01-04T22:51:35.144Z",
      "cellar": [ ],
      "wants": [ ],
      "groups": [ ],
      "user_permissions": [ ],
      "created": "2015-01-04T22:51:35.238Z",
      "modified": "2015-01-04T22:51:35.238Z",
      "date_joined": "2015-01-04T22:51:35.144Z"
    },
    "model": "users.userprofile",
    "pk": 1
  }
]

```


### GET: `/api/users/:username`

Get all details for a single specified user

**Example Usage**

```
GET /api/users/adam HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
```

**Example Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json
[
  {
    "fields": {
      "username": "adam",
      "first_name": "",
      "last_name": "",
      "email": "",
      "is_active": true,
      "is_superuser": false,
      "is_staff": false,
      "last_login": "2015-01-04T22:51:35.144Z",
      "cellar": [ ],
      "wants": [ ],
      "groups": [ ],
      "user_permissions": [ ],
      "created": "2015-01-04T22:51:35.238Z",
      "modified": "2015-01-04T22:51:35.238Z",
      "date_joined": "2015-01-04T22:51:35.144Z"
    },
    "model": "users.userprofile",
    "pk": 1
  }
]

```

### POST: `/api/users/:username`

Update the user profile for the specified user. Note, the username must match the current authenticated user.

**Example Usage**

```
POST /api/users/adam/ HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
Content-Type: application/json
```
```json
{
  "username": "adam",
  "first_name":"Adam",
  "last_name": "Wonak",
  "email": "adam.wonak@gmail.com"
}
```

**Example Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json
{
  "username": "adam",
  "first_name": "Adam",
  "last_name": "Wonak",
  "email": "adam.wonak@gmail.com"
}
```

If there are any missing fields or invalid fields, the server will respond with a HTTP 400 error response like the following:


**Example Invalid Usage**

```
POST /api/users/adam/ HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
Content-Type: application/json
```
```json
{
  "username": "adam",
  "first_name":"Adam",
  "email": "xxinvalidxx"
}
```

**Example Error Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json
{
    "last_name": ["This field is required."],
    "email": ["Enter a valid email address."]
}
```
