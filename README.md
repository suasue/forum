# forum_api

### GET /question : Show question list and search by keyword
- **URL:**

    /question

- **Method:**

    `GET`

- **Query Params:**

    **Optional:**

    `keyword=[string]`

- **Sample Call:**

    ```bash
    http GET localhost:8000/question
    ```
    ```bash
    http GET localhost:8000/question keyword=="01"
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{
    "questions": [
        {
            "author": "sua01",
            "content": "test_content01",
            "created_at": "2021-05-15 19:22:23",
            "id": 1,
            "title": "test_title01"
        }, {...}
    ]
}`

<br>

### POST /question : Create a question

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
    http POST localhost:8000/question "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY title="test_title04" content="test_content04"
    ```

- **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{'message': 'SUCCESS'}`
- **Error Response:**
    - **Code:** 400 Bad Request
    - **Content:** `{'message': 'KEY_ERROR'}`

<br>

### Put /question/:id : Update a question

- **URL:**

    /question/:id

- **Method:**

    `POST`

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
    http PUT localhost:8000/question/1 "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY title="modified_title" content="modified_content"
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

### Delete /question/:id : Delete a question

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
    http DELETE localhost:8000/question/1 "Authorization":eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.IBOJR9PIpMToOWcFjK7XK5zEGrgCMQYG-D8Kcwa9VKY
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

### Get /question/:id : Show a question

- **URL:**

    /question/:id

- **Method:**

    `GET`

- **URL params:**

    **Required:**

    `id=[integer]`

- **Sample Call:**

    ```bash
    http GET localhost:8000/question/1
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
