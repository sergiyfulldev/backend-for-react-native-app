# Register

Used to register a new user, and receive a token for authentication

**URL** : `/auth/api/register`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "email": "[valid email address]",
    "password": "[password in plain text]",
    "name": "[Users name in plaintext]"
}
```

**Data example**

```json
{
    "email": "user@example.com",
    "password": "examplepassword1234",
    "name": "John Smith"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "Registration complete",
    "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response


<details>
    <summary>
        **Condition** : If no data has been included in the request
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "No data provided in request"
}
```
</p>
</details>

<details>
    <summary>
        **Condition** : If 'email' in email field has already been registered
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "This email has already been registered"
}
```
</p>
</details>

