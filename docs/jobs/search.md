# Search

Used to search (filter) job listings.

**URL** : `/api/jobs/search/`

**Method** : `POST`

**Auth required** : YES

**Data example**

To complete a search either the "radius" and "long" / "lat" fields must be filled, or the match_skills field set to true.
You can use both to filter by radius and skills, or just skills, however one option (and depended fields) must be defined.

```json
{
  "search": {
    "radius": 5, // Radius in km
    "long": -1,
    "lat": 1,
    "match_skills": true
  }
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success",
  "message": "",
  "jobs": [/*...*/]
}
```

## Error Response

<details>
    <summary>
        **Condition** : No search settings defined
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Response Content**

```json
{
  "status": "error",
  "message": "Please check your search settings and try again"
}
```
</p>
</details>

