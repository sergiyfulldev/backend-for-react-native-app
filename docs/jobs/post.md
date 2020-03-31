# Post

Used to post a new job listing.

**URL** : `/api/jobs/post/`

**Method** : `POST`

**Auth required** : YES

**Data constraints**
```json
```

**Data example**

```json
{
  "title": "Walking my Dog",
  "description": "Scruffy really likes being walked while I'm at work; Will pay 20$",
  "longitude": "-63.1315222",
  "latitude": "46.2356426",
  "skills_required": [ //Note that this field is optional.
    {"id": 1, "min_years_experience": 1}
  ]
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success",
  "message": "Job listing posted",
  "job": {
      "title": "Walking my Dog",
      "description": "Scruffy really likes being walked while I'm at work; Will pay 20$",
      "longitude": "-63.1315222",
      "latitude": "46.2356426",
      "owner_id": "1002",
      "skills_required": [{"id": 1, "min_years_experience": 1}]
  }
}
```

## Error Response

<details>
    <summary>
        **Condition** : No body of data was submitted via the post request.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Response Content**

```json
{
  "status": "error",
  "message": "No data provided"
}
```
</p>
</details>

<details>
    <summary>
        **Condition** : Any of the fields were empty / invalid.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content Submitted**

```json
{
  "title": "",
  "description": "",
  "longitude": "-63.1315222",
  "latitude": "46.2356426"
}
```

**Response Content**

```json
{
  "status": "error",
  "message": "Invalid Field Input",
  "fields": [
    "title",
    "description"
  ]
}
```
</p>
</details>

<details>
    <summary>
        **Condition** : Unable to locate user who made request
    </summary>
<p>

Note: This error should not happen (ever); If it happens, run test suite and confirm its source.

**Code** : `401 UNAUTHORIZED`

**Response Content**

```json
{
  "status": "error",
  "message": "Unable to validate user"
}
```
</p>
</details>