# Skills

Used to manage the skills available for users to define in their profile and on jobs.

**URL** : `/api/skills/`

**Method** : `POST` | `GET` | `DELETE`

**Auth required** : YES



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

