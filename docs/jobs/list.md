# List

Used to retrieve a list of all the jobs.

**URL** : `/api/jobs/list` | `/api/jobs/list/<filter>`

**< filter >**:

| Value      | Result                             |
|------------|------------------------------------|
| all        | Retrieve all available jobs        |
| applied    | Retrieve all jobs applied for.     |
| notapplied | Retrieve all jobs not applied for. |


**Method** : `GET`

**Auth required** : YES

**Data example**

```
GET :: /api/jobs/list
```
or
```
GET :: /api/jobs/list/all
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "",
    "jobs": [{
      "id": "1",
      "title": "Job Listing Title",
      "description": "Job Listing Description",
      "owner_id": "1002",
      "longitude": "-63.1315222",
      "latitude": "46.2356426",
      "applied": false, //only visible if they're not the owner.
      "skills_required": [{"id": 1, "min_years_experience": 1}]
    }]
}
```

## Error Response

Will not error unless user is unauthenticated.