# Search API

Endpoints for handling search requests


- [GET: `/api/search/`](#get-apisearch)

## GET: `/api/search`

Submit credentials for registering a new user.

Param    | Description
-------- | ----------------
q        | Required. Query search string for matching a BreweryDb beer name.

**Example Usage**

```
GET /api/search/?q=big+hugs HTTP/1.1
Authorization: Token d8473d2b993b4ef19c21bcd71fe3f65fe7d6189d
```

**Example Response**

```
HTTP/1.0 200 OK
Content-Type: application/json
```

```json

{
  "status": "success",
  "currentPage": 1,
  "totalResults": 588,
  "data": [
    {
      "status": "verified",
      "available": {
        "description": "Limited availability.",
        "id": 2,
        "name": "Limited"
      },
      "isOrganic": "N",
      "labels": {
        "large": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-large.png",
        "medium": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-medium.png",
        "icon": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-icon.png"
      },
      "description": "Big HugsThis beer is a thug. Big and chock full of tender embrace.",
      "statusDisplay": "Verified",
      "createDate": "2012-12-07 11:54:25",
      "year": 2012,
      "style": {
        "category": {
          "createDate": "2012-03-21 20:06:45",
          "id": 3,
          "name": "North American Origin Ales"
        },
        "ogMin": "1.08",
        "description": "Black in color, American-style imperial stouts typically have a high alcohol content. Generally characterized as very robust. The extremely rich malty flavor and aroma are balanced with assertive hopping and fruity-ester characteristics. Bitterness should be moderately high to very high and balanced with full sweet malt character. Roasted malt astringency and bitterness can be moderately perceived but should not overwhelm the overall character. Hop aroma is usually moderately-high to overwhelmingly hop-floral, -citrus or -herbal. Diacetyl (butterscotch) levels should be absent.",
        "createDate": "2012-03-21 20:06:46",
        "ibuMin": "50",
        "categoryId": 3,
        "srmMax": "40",
        "ibuMax": "80",
        "abvMin": "7",
        "fgMin": "1.02",
        "fgMax": "1.03",
        "abvMax": "12",
        "id": 43,
        "srmMin": "40",
        "name": "American-Style Imperial Stout"
      },
      "updateDate": "2012-12-17 11:36:14",
      "abv": "10",
      "styleId": 43,
      "availableId": 2,
      "type": "beer",
      "id": "sHgBrJ",
      "name": "Big Hugs"
    },
    {}
  ],
  "numberOfPages": 12
}

```