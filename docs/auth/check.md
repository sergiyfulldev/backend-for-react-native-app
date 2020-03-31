# Check

Used to check if an authentication token is still valid.

**URL** : `/auth/api/check/<token>/`

**Method** : `GET`

**Auth required** : NO

**Data constraints**
'token' type is string

**Data example**

```
GET :: /auth/api/check/93144b288eb1fdccbe46d6fc0f241a51766ecd3d/
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "Token is valid"
}
```

## Error Response

<details>
    <summary>
        **Condition** : If 'token' is not.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "No token provided"
}
```
</p>
</details>


<details>
    <summary>
        **Condition** : If 'token' is expired / invalid.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "Invalid / Expired Token"
}
```
</p>
</details>