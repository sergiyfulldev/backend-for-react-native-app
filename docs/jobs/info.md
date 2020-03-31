# Info

Used to retrieve listing information for a specific job via id.

**URL** : `/api/jobs/info/<id>/`

**Method** : `GET`

**Auth required** : YES

**Data constraints**
'id' type is int

**Data example**

```
GET :: /api/jobs/info/1/
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "",
    "job": {
      "id": "1",
      "title": "Job Listing Title",
      "description": "Job Listing Description",
      "owner_id": "1002",
      "longitude": "-63.1315222",
      "latitude": "46.2356426",
      "applied": false, //variable only visible if user != owner
      "skills_required": [{"id": 1, "min_years_experience": 1}]
    }
}
```

## Error Response

<details>
    <summary>
        **Condition** : If 'id' is not defined or invalid.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "Invalid Job ID"
}
```
</p>
</details>