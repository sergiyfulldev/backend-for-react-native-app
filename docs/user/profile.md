# Profile

Retrieve a users information

**URL** : `/api/users/`

**Methods** : `GET`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "",
    "user": {
      "id": 1,
      "email": "test@test.com",
      "name": "Test User",
      "jobs_posted": [
        {}
      ]
    }
}
```

## Error Response

<details>
    <summary>
        **Condition** : DELETE - No Json Data Passed with Request
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

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
        **Condition** : DELETE - No Skill id's in the data submitted.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "No skills provided"
}
```
</p>
</details>