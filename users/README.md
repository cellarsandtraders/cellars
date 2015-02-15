# User API

Endpoints for handling User Profile objects


- [GET: `/api/users`](#get-apiusers)
- [GET: `/api/users/:username`](#get-apiusersusername)
- [POST: `/api/users/:username`](#post-apiusersusername)
- [GET: `/api/users/:username/:collection`](#get-apiusersusernamecollection)
- [POST: `/api/users/:username/:collection`](#post-apiusersusernamecollection)
- [DELETE: `/api/users/:username/:collection/:item_id`](#delete-apiusersusernamecollection)

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
    "username": "adam",
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
{
  "username": "adam",
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

```

### POST: `/api/users/:username`

Update the user profile for the specified user. Note, the username must match the current authenticated user.

**Example Usage**

```
POST /api/users/adam HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
Content-Type: application/json
```
```json
{
  "username": "adam",
  "first_name":"Adam",
  "last_name": "Wonak",
  "email": "adam.wonak@gmail.com",
  "address": "123 N Main St.",
  "address2": "#100",
  "city": "Chicago",
  "state": "IL",
  "zipcode": "60647"
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
  "email": "adam.wonak@gmail.com",
  "address": "123 N Main St.",
  "address2": "#100",
  "city": "Chicago",
  "state": "IL",
  "zipcode": "60647"
}
```

If there are any missing fields or invalid fields, the server will respond with a HTTP 400 error response like the following:


**Example Invalid Usage**

```
POST /api/users/adam HTTP/1.1
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
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
```

```json
{
    "last_name": ["This field is required."],
    "email": ["Enter a valid email address."]
}
```


### GET: `/api/users/:username/:collection`

Get a list of all cellar items for the specified user and the specified collection (cellar / wishlist). All examples below use the collection `cellar` as the example and function identically for the collection `wishlist` when substuting the collection type in the url.

**Example Usage**

```
GET /api/users/adam/cellar HTTP/1.1
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
    "brewery_id": "lZfiot",
    "style": "American-Style Imperial Stout",
    "brewery_name": "Half Acre Beer Company",
    "created": "2015-01-11T23:20:14.361Z",
    "modified": "2015-01-11T23:20:21.853Z",
    "label": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-large.png",
    "willing_to_trade": true,
    "beer_name": "Big Hugs",
    "abv": 10,
    "year": "2012",
    "beer_id": "sHgBrJ",
    "quantity": 1
  }
]

```


### POST: `/api/users/:username/:collection`

Add or Update a collection item depending on the presence of the `pk` value in the request body data. The authorization token must match the username in the url, otherwise the server will respond with a 403 Forbidden error response.

**Example Usage**

```
POST /api/users/adam/cellar HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
```
```json
{
  "pk": 14,
  "beer_id": "sHgBrJ",
  "beer_name": "Big Hugs",
  "brewery_id": "lZfiot",
  "brewery_name": "Half Acre Beer Company",
  "style": "American-Style Imperial Stout",
  "abv": "10",
  "year": "2012",
  "quantity": "1",
  "willing_to_trade": false,
  "label": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-large.png"
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
    "item": {
        "brewery_id": "lZfiot",
        "style": "American-Style Imperial Stout",
        "brewery_name": "Half Acre Beer Company",
        "label": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-large.png",
        "willing_to_trade": false,
        "beer_name": "Big Hugs",
        "abv": 10,
        "year": "2012",
        "beer_id": "sHgBrJ",
        "quantity": 1
    },
    "pk": 14,
    "created": false
}

```

In this example, the cellar item was updated since a `pk` was provided. If it were `null` then the data would have been added as a new item and the `created` response field would have been `false`.


### DELETE: `/api/users/:username/:collection/:item_id`

Delete the specified collection item for the specified user. If the `pk` provided doesn't match an item for that user in that collection, the server will respond with a 404 Not Found error.

**Example Usage**

```
DELETE /api/users/adam/cellar/14 HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
```

**Example Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json
{}
```
