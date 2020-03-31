# (Admin) User/Permissions

Used to manage the permissions attached to a user.

**URL** : `/api/admin/users/permissions/`

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

