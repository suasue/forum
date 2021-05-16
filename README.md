# forum_api
### Insatllation from the git repo
```
$ git clone https://github.com/suasue/forum.git
$ cd forum
$ docker-compose up
```

### How to use
- **Install httpie for integration test**
```
$ pip install httpie
```

- **URL List:**
```
/question
/question/:id
/question/:id/comment
/question/:id/like
/question/:id/best
/user/signup
/user/signin
```
- **User Example:**
```
email : user1@example.com
password : 12341234
access_token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY
```
<br>

## APIs

### Show questions and search by keyword
- **URL:**

    /question

- **Method:**

    `GET`

- **Query Params:**

    **Optional:**

    `keyword=[string]`

- **Sample Call:**

    ```bash
    $ http GET localhost:8000/question
    ```
    ```bash
    $ http GET localhost:8000/question keyword=="01"
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{
    "questions": [
        {
            "author": "user1",
            "content": "what is migrate and makemigrations in django?",
            "created_at": "2021-05-16 06:23:41",
            "id": 1,
            "title": "django migrate"
        },
        {
            "author": "user1",
            "content": "What is JWT? How to use it in my project?",
            "created_at": "2021-05-16 06:25:57",
            "id": 2,
            "title": "what is JWT?"
        },
        {
            "author": "user2",
            "content": "What's better to use Django ORM or to use raw SQL?",
            "created_at": "2021-05-16 06:27:49",
            "id": 3,
            "title": "Django ORM vs SQL"
        }
    ]
}
`

<br>

### Create a question

- **URL:**

    /question

- **Method:**

    `POST`

- **Body:**

    **Required:**

    `title`, `content`

- **Request Header:**
    Authorization: {access token]

- **Sample Call:**

    ```bash
    $ http POST localhost:8000/question "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY title="test_title04" content="test_content04"
    ```

- **Success Response:**
    - **Code:** 201 Created
    - **Content:** `{'message': 'SUCCESS'}`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`

<br>

### Update a question

- **URL:**

    /question/:id

- **Method:**

    `PUT`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Body:**

    **Required:**

    `title`, `content`

- **Request Header:**
    Authorization: {access token]

- **Sample Call:**

    ```bash
    $ http PUT localhost:8000/question/1 "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY title="modified_title" content="modified_content"
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{'message': 'SUCCESS'}`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`
    - **Code:** 401 Unauthorized
    - **Content:** `{'message': 'INVALID_USER'}`
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`

<br>

### Delete a question

- **URL:**

    /question/:id

- **Method:**

    `DELETE`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Request Header:**
    Authorization: {access token]

- **Sample Call:**

    ```bash
    $ http DELETE localhost:8000/question/1 "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{'message': 'SUCCESS'}`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`
    - **Code:** 401 Unauthorized
    - **Content:** `{'message': 'INVALID_USER'}`
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`

<br>

### Show a question

- **URL:**

    /question/:id

- **Method:**

    `GET`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Sample Call:**

    ```bash
    $ http GET localhost:8000/question/1
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{
    "questions": {
            "author": "sua01",
            "content": "test_content01",
            "created_at": "2021-05-15 19:22:23",
            "id": 1,
            "title": "test_title01"
        } }`

- **Error Response:**
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`


<br>

### Create a comment

- **URL:**

    /question/:id/comment

- **Method:**

    `POST`

- **URL params:**

    **Required:**

    `id=[integer]`
    
- **Body:**

    **Required:**

    `content`

- **Request Header:**
    Authorization: {access token]

- **Sample Call:**

    ```bash
    $ http POST localhost:8000/question/1/comment "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY content="test_comment"
    ```

- **Success Response:**
    - **Code:** 201 Created
    - **Content:** `{'message': 'SUCCESS'}`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`
 
<br>

### Show all comments to the question

- **URL:**

    /question/:id/comment

- **Method:**

    `GET`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Sample Call:**

    ```bash
    $ http GET localhost:8000/question/1/comment
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{
    "comments": [
        {
            "author": "user2",
            "content": "As Django's documentation says Migrations are Django’s way of propagating changes you make to your models into your database schema.",
            "created_at": "2021-05-16 06:31:41",
            "id": 1
        },
        {
            "author": "user1",
            "content": "Thank you for your answer",
            "created_at": "2021-05-16 06:33:17",
            "id": 2
        }
    ]
}
`
- **Error Response:**
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`

<br>

### Create or delete a like

- **URL:**

    /question/:id/like

- **Method:**

    `POST`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Request Header:**
    Authorization: {access token]

- **Sample Call:**

    ```bash
    $ http POST localhost:8000/question/1/like "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY
    ```

- **Success Response:**
    - **Code:** 201 Created
    - **Content:**`{
    "like_count": 1,
    "message": "SUCCESS"
}
`
    - **Code:** 200 OK
    - **Content:** `{
    "like_count": 0,
    "message": "SUCCESS"
}
`
- **Error Response:**
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`

<br>

### Show most liked question of the month that the question created in

- **URL:**

    /question/:id/best

- **Method:**

    `GET`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Sample Call:**

    ```bash
    $ http GET localhost:8000/question/1/best
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `
{
    "best_question": {
        "author": "user2",
        "content": "What's better to use Django ORM or to use raw SQL?",
        "created_at": "2021-05-16 06:27:49",
        "id": 3,
        "like_count": 3,
        "title": "Django ORM vs SQL"
    }
}
`
- **Error Response:**
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'QUESTION_DOES_NOT_EXIST'}`

<br>

### Signup

- **URL:**

    /user/signup

- **Method:**

    `POST`

- **Body:**

    **Required:**

    `email`, `name`, `password`


- **Sample Call:**

    ```bash
    $ http POST localhost:8000/user/signup email="user1@example.com" name="user1" password="12341234"
    ```

- **Success Response:**
    - **Code:** 201 Created
    - **Content:**`{
    "message": "SUCCESS"
}
`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`
    - **Code:** 409 Conflict
    - **Content:** `{'message': 'USER_ALREADY_EXISTS'}`


### Signin

- **URL:**

    /user/signin

- **Method:**

    `POST`

- **Body:**

    **Required:**

    `email`, `password`


- **Sample Call:**

    ```bash
    $ http POST localhost:8000/user/signin email="user1@example.com" password="12341234"
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:**`{
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY",
    "message": "SUCCESS"
}
`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`
    - **Code:** 401 Unauthorized
    - **Content:** `{'message': 'INVALID_PASSWORD'}`
    - **Code:** 404 Not Found
    - **Content:** `{'message': 'USER_DOES_NOT_EXIST'}`

