# Apply

Used to apply to a job listing.

**URL** : `/api/jobs/apply/`

**Method** : `POST`

**Auth required** : YES

**Data example**

```json
{
  "job_id": "1"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success",
  "message": "Applied to job"
}
```

## Error Response

<details>
    <summary>
        **Condition** : An Application for this job has already been submitted
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Response Content**

```json
{
  "status": "error",
  "message": "An application has already been submitted for this job."
}
```
</p>
</details>

<details>
    <summary>
        **Condition** : No Job ID Provided
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Response Content**

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
        **Condition** : Invalid Job ID.
    </summary>
<p>

**Code** : `400 BAD REQUEST`

**Content Submitted**

```json
{
  "id": "1"
}
```

**Response Content**

```json
{
  "status": "error",
  "message": "Invalid Job ID"
}
```
</p>
</details>