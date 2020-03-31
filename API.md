# REST API Documentation

Full documentation on the REST Api.

## Open Endpoints

Open endpoints require no Authentication.

* [Login](docs/auth/login.md) : `POST /api/auth/login/`
* [Register](docs/auth/register.md) : `POST /api/auth/register/`
* [Token Check](docs/auth/check.md) : `GET /api/auth/check/<token>`

## Endpoints that require Authentication

Closed endpoints require a valid Token to be included in the header of the
request. A Token can be acquired from the Login view or registration view above.

### Authentication Server Endpoints

Each endpoint is a part of the authentication flow for our application.

* [Login](docs/auth/login.md) : `POST /api/auth/login/`
* [Register](docs/auth/register.md) : `POST /api/auth/register/`
* [Token Check](docs/auth/check.md) : `GET /api/auth/check/<token>`


### User related

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* [Show Profile](docs/user/profile.md) : `GET /api/users/`
* [List / Delete / Add Skills](docs/user/skills.md) : `GET /api/user/` | `DELETE /api/user/` | `POST /api/user/`

### Job related

Each endpoint manages an aspect of the jobs for our application.

* [Apply to Job](docs/jobs/apply.md) : `POST /api/jobs/apply/`
* [Information on a Job](docs/jobs/info.md) : `GET /api/jobs/info/<int:id>`
* [List Jobs](docs/jobs/list.md) : `GET /api/jobs/list` | `GET /api/jobs/list/< filter>
* [Post Job](docs/jobs/post.md) : `POST /api/jobs/post/`