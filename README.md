# Todo Challenge for Invera

![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


#### Introduction
This API works as a task app, where you can create, delete, edit, and complete tasks. 
For using this app an account is needed, the tasks of each user are saved in a database and can be retrieved only by its creator.

#### How to launch the API in local
The API is configured with Docker for an easy setup in any machine.
Just clone the repository and run ```docker-compose up --build```
The docker configuration consists of 1 service/image called API but it could be configurated easily with 2 services, for backend and frontend.

#### Authentication
The API uses the [DRF TokenAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication "Django TokenAuthentication") system.

#### Status Codes

| Status Code | Description |
| ------------ | ------------ |
| 200 | `OK` |
| 201 | `CREATED` |
| 204 | `NO CONTENT` |
| 400 | `BAD REQUEST` |
| 403 | `FORBIDDEN` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |


#### Response behaviour
The response can contain data as a value (text or list) of the `'detail'` key.

When creating or updating a user or task (`201 CREATED`/`200 OK`), it will always return the created/updated object. 

When deleting, the response will only be a `204 NO CONTENT` and no data will be returned.


## Users

#### Create users
```http
POST /users/signup/
```
The needed values for creating user accounts are the ones from the user, the profile information its not required when creating a user.

| Form Keys |
| ------------ |
| username |
| password |
| password_confirmation |

#### Login user
```http
POST /users/login/
```
The response will contain the username and the token for authentication, as following:

```
{
"username":  "nicolas",
"access_token":  "dc47c4a70e930a6b890fc80fba701a581ee6b846"
}
```

| Form Keys |
| ------------ |
| username |
| password |


#### Get current user
```http
GET /users/current/
```
This will retrieve the username of the current user, as following:

```
{
"username":  "nicolas"
}
```


| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |


#### Update users
```http
PUT /users/`username`/
```

The update of the user applies only to the username.

| Form Keys |
| ------------ |
| username |

#### Change password
```http
PUT /users/change_password/
```

Change the user password.

| Form Keys |
| ------------ |
| password |
| new_password |

#### Delete user
```http
DELETE /users/'username'/
```

This will delete the user from the database.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

## Tasks
#### Create task
```http
POST /tasks/
```
This request will create a task, and return it.
Anyone who is logged in can create a task.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

The only required field is the title.

| Form Keys |
| ------------ |
| title |
| limit_date (Optional) |

#### List tasks
```http
GET /tasks/'filters'
```
This will retrieve a list of tasks created by the user (15 at a time, if the user has more than 15 tasks, pagination will be applied), as following:
```
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": 1,
            "user": "nicolas",
            "title": "Task number 1",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": null
        },
        {
            "pk": 5,
            "user": "nicolas",
            "title": "Task number 2",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": null
        },
        {
            "pk": 6,
            "user": "nicolas",
            "title": "Task number 5",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": null
        },
        {
            "pk": 2,
            "user": "nicolas",
            "title": "Task number 3",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": "2021-10-14"
        },
        {
            "pk": 3,
            "user": "nicolas",
            "title": "Task number 4",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": "2022-02-03"
        },
        {
            "pk": 4,
            "user": "nicolas",
            "title": "Task number 6",
            "is_completed": false,
            "date": "2021-10-14",
            "limit_date": "2025-12-02"
        }
    ]
}
```

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |


For filtering the following parameters can be aplied in the url:

| Filter by | Value |
| ------------ | ------------ |
| Search | `title` |
| Ordering | `is_completed, date, limit_date` |
| is_completed | `True/1 or False/0` |
| date | `date` |
| limit_date | `date` |

By default the not completed tasks will appear first.

#### Update task
```http
PATCH /tasks/'id'/
```
Only the title of a task can be changed.

Only the user who created the task can update it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |

| Form Keys |
| ------------ |
| title |

#### Delete task
```http
DELETE /tasks/'id'/
```

Only the user who created the task can delete it.

| Headers | Value |
| ------------ | ------------ |
| authorization | token `user token` |
