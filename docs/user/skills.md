# Skills

Manage a users skills.

**URL** : `/api/users/skills/`

**Methods** : `GET, POST, DELETE`

**Auth required** : YES

**Data constraints**
'token' type is string

**Data example**

1. Get Request (_Retrieve skills. Refer to content returned_)

2. Post Request (Add skills to a user)
```json
{
  "skills": [
    {"id": 1, "experience_in_years": 0},
    {"id": 2, "experience_in_years": 1}
  ]
}
```

3. Delete Request (remove skills from a user)
```json
{
  "skills": [1,6]
}
```

## Success Response

**Code** : `200 OK`

**Content example**
<details>
    <summary>
        **METHOD** : POST (ADD SKILLS TO USER)
    </summary>
<p>

```json
{
    "status": "success",
    "message": "User skills added"
}
```
</p>
</details>

<details>
    <summary>
        **METHOD** : GET (LIST USER SKILLS)
    </summary>
<p>

```json
{
    "status": "success",
    "message": "",
    "skills": [
      {"id": 1, "experience_in_years": 0},
      {"id": 3, "experience_in_years": 1}
    ]
}
```
</p>
</details>
<details>
    <summary>
        **METHOD** : DELETE (REMOVE USER SKILLS)
    </summary>
<p>

```json
{
    "status": "success",
    "message": "Skills deleted"
}
```
</p>
</details>


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