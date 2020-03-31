# Login

Used to collect a Token for a registered User.

**URL** : `/auth/api/login/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "email": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "email": "user@example.com",
    "password": "examplepassword1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "status": "success",
    "message": "Login Successful",
    "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response

<details>
    <summary>
        **Condition** : If 'username' and 'password' combination is wrong.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "Invalid login credentials"
}
```
</p>
</details>


<details>
    <summary>
        **Condition** : If 'username' and 'password' field are blank.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "status": "error",
    "message": "No data was present in the request"
}
```
</p>
</details>
