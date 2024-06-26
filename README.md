
# MyTodoSite

FlaskPostgresAPI is a simple RESTful API site built using Flask and PostgreSQL. It allows you to perform CRUD (Create, Read, Update, Delete) operations on a database through HTTP requests.

![img.png](img.png)

![img_1.png](img_1.png)

![img_2.png](img_2.png)
## Installation

1. Clone this repository:
    ```
    git clone https://github.com/olusesa/mytodosite.git
    ```

2. Navigate into the project directory:
    ```
    cd FlaskPostgresAPI
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database and configure the connection details as environment variable.

5. Run the application:
    ```
    python main.py
    ```

By default, the application will run on `http://localhost:5000`.

## Endpoints

- **GET /**: Retrieve all users.
- **GET /search/todo/<id>**: Retrieve a specific user by ID.
- **POST /add/todo/<username>**: Create a new user.
- **PUT /update/todo/<id>**: Update a user by ID.
- **PATCH /update/todo/<id>**: Update a user entry by ID.
- **DELETE /delete/todo/<id>**: Delete a user by ID.

## Request & Response Examples

### GET all ("/")

Request:
```
curl http://localhost:5000/
```

Response:
```
[
    {
        "id": #,
        "username": "<username>
        "name": "<name>",
        "email": "<email>",
        "phone": "<phone>"
    },
    {
        "id": 3,
        "username": "<username>
        "name": "<name>",
        "email": "<email>",
        "added_date": "<added_date>"
        "due_date": "<due_date>"
        "status": "<status>"
    }
]
```

### GET /search/todo/1

Request:
```
curl http://localhost:5000/1
```

Response:
```
{
       "id": 3,
        "username": "<username>
        "name": "<name>",
        "email": "<email>",
        "added_date": "<added_date>"
        "due_date": "<due_date>"
        "status": "<status>"
}
```

### POST /add/todo/<username>

Request:
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"<username>, "name": "New user name", "email": "New user email", "phone": "New user phone number"}' http://localhost:5000/add/todo/<username>
```

Response:
```
{
        "id": 3,
        "username": "<username>
        "name": "<name>",
        "email": "<email>",
        "added_date": "<added_date>"
        "due_date": "<due_date>"
        "status": "<status>"
}
```

### PATCH /update/todo/3

Request:
```
curl -X PATCH -H "Content-Type: application/json" -d '{"name": "New Name", "Message": "name entry updated successfully"}' http://localhost:5000/update/todo/3
```

Response:
```
{
        "id": 3,
        "username": "<username>
        "name": "<name>",
        "email": "<email>",
        "added_date": "<added_date>"
        "due_date": "<due_date>"
        "status": "<status>"
}
```

### DELETE /delete/todo/3

Request:
```
curl -X DELETE http://localhost:5000/delete/todo/3
```

Response:
```
{
    "message": "User with ID 3 has been deleted successfully"
}
```

## License

This project is licensed under the MIT License