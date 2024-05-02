import os
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
import psycopg2
from flask import Flask, request, jsonify
from todoform import TodoForm
from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import  load_dotenv
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


load_dotenv()
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///posts.db')
#app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = 'QQWqWERRRWtYbggdd#$%dt'
connection = psycopg2.connect(url)

CREATE_TODOS_TABLE = ("CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, username TEXT, name TEXT, "
                      "email TEXT, password TEXT, todo TEXT, date_added TEXT, due_date TEXT,status TEXT);")

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_TODOS_TABLE)

INSERT_TODOS_RETURN_ID = ("INSERT INTO todos (username, name, email, password, todo, date_added, due_date, status, ) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;")
SELECT_ALL_TODOS = "SELECT * FROM todos;"
SELECT_TODOS_BY_ID = "SELECT id, username, name, email, password, todo, filter, sort FROM todos WHERE id = %s;"
TODOS_STATUS_BY_COMPLETED = ("SELECT id, username, name, email, password, todo, added_date, due_date, status "
                             "FROM todos WHERE filter = %s;")
TODOS_STATUS_BY_HAS_DUE_DATE = ("SELECT id, username, name, email, password, todo, added_date, due_date, status "
                                "FROM todos WHERE filter = %s;")
TODOS_STATUS_BY_ARCHIVED = ("SELECT id, username, name, email, password, todo, added_date, due_date, status "
                            "FROM todos WHERE filter = %s;")
SORT_TODOS_BY_DUE_DATE = ("SELECT id, username, name, email, password, todo, added_date, due_date, status "
                          "FROM todos WHERE filter = %s;")
SORT_TODOS_BY_ADDED_DATE = ("SELECT id, username, name, email, password, todo, added_date, due_date, status "
                            "FROM todos WHERE filter = %s;")
UPDATE_USERNAME_BY_ID = "UPDATE todos SET username = %s WHERE id = %s;"
UPDATE_NAME_BY_ID = "UPDATE todos SET name = %s WHERE id = %s;"
UPDATE_EMAIL_BY_ID = "UPDATE todos SET email = %s WHERE id = %s;"
UPDATE_ADDED_DATE_BY_ID = "UPDATE todos SET added_date = %s WHERE id = %s;"
UPDATE_DUE_DATE_BY_ID = "UPDATE todos SET due_date = %s WHERE id = %s;"
UPDATE_STATUS_BY_ID = "UPDATE todos SET status = %s WHERE id = %s;"
UPDATE_TODO_BY_ID = "UPDATE todos SET todo = %s WHERE id = %s;"
DELETE_TODO_BY_ID = "DELETE FROM todos WHERE id = %s;"

Bootstrap5(app)

# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)



# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


# @app.route('/')
# def home():
#     return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=request.form.get('name'),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/", methods=['POST'])
def home():
    return render_template("index.html")

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create_todo():
    form = TodoForm()
    data = request.get_json()
    form.username = data["username"]
    form.name = data["name"]
    form.email = data["email"]
    form.password = data["password"]
    form.todo = data["todo"]
    form.added_date = data["added_date"]
    form.due_date = data["added_date"]
    form.status = data["status"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TODOS_RETURN_ID, (form.username, form.name, form.email, form.password, form.todo, form.added_date, form.due_date, form.status))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "username": data['username'], "name": data['name'],
            "message": f"Username:  {data['username']} created successfully."}, 201

@app.route("/search/todos/all", methods=['GET', 'POST'])
def get_all_todos():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_TODOS)
            todos = cursor.fetchall()
            if todos:
                result = []
                for todo in todos:
                    result.append({"id": todo[0], "username": todo[1], "name": todo[2], "email": todo[3],
                                   "todo": todo[5], "added_date": todo[6], "due_date": todo[7], "status": todo[8]})
                return jsonify(result)
            else:
                return jsonify({"error": f" Todo not found."}), 404
    render_template("display_todos.html", todos=todos, name=current_user, logged_in=True)

@app.route("/search/todo/<int:todo_id>", endpoint='get_todo', methods=["GET"])
def get_todo(todo_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
            todo = cursor.fetchone()
            if todo:
                return jsonify({"id": todo[0], "username": todo[1], "name": todo[2], "email": todo[3],
                                   "todo": todo[5], "added_date": todo[6], "due_date": todo[7], "status": todo[8]})
            else:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    render_template("display_todos.html", todos=todo, name=current_user.name, logged_in=True)

@app.route("/update/todo/<int:todo_id>", endpoint='update_todo_entries', methods=["PUT"])
@login_required
def update_todo_entries(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.username = data["username"]
    form.name = data["name"]
    form.email = data["email"]
    form.password = data["password"]
    form.todo = data["todo"]
    form.added_date = data["added_date"]
    form.due_date = data["added_date"]
    form.status = data["status"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USERNAME_BY_ID, (form.username, form.name, form.email, form.password, form.todo,
                                                   form.added_date, form.due_date, form.status))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "username": form.username, "name": form.name, "email": form.email,
                    "message": f"Todo with username {data['username']} entries updated successfully."})
@app.route("/update/todo/<int:todo_id>", endpoint='update_email_entry', methods=["PATCH"])
@login_required
def update_email_entry(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.email = data["email"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_EMAIL_BY_ID, (form.email, todo_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "email": data['email'], "message":
        f"The email of Todo with ID {todo_id} updated successfully."})

@app.route("/update/todo/<int:todo_id>", endpoint='update_todo_entry', methods=["PATCH"])
@login_required
def update_todo_entry(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.todo = data["todo"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TODO_BY_ID, (form.todo, todo_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "todo": data['todo'], "message":
        f"The Todo entry with ID {todo_id} updated successfully."})

@app.route("/update/todo/<int:todo_id>", endpoint='update_added_date_entry', methods=["PATCH"])
@login_required
def update_added_date_entry(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.added_date = data["added_date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_ADDED_DATE_BY_ID, (form.added_date, todo_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "added_date": data['added_date'], "message":
        f"The Added date of Todo with ID {todo_id} updated successfully."})

@app.route("/update/todo/<int:todo_id>", endpoint='update_due_date_entry', methods=["PATCH"])
@login_required
def update_due_date_entry(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.due_date = data["due_date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_DUE_DATE_BY_ID, (form.due_date, todo_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "due_date": data['due_date'], "message":
        f"The due date of Todo with ID {todo_id} updated successfully."})

@app.route("/update/todo/<int:todo_id>", endpoint='update_status_entry', methods=["PATCH"])
@login_required
def update_status_entry(todo_id):
    data = request.get_json()
    form = TodoForm()
    form.status = data["status"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_STATUS_BY_ID, (form.status, todo_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Todo with ID {todo_id} not found."}), 404
    return jsonify({"id": todo_id, "status": data['status'], "message":
        f"The status of Todo with ID {todo_id} updated successfully."})
@app.route("/delete/user/<int:todo_id>", methods=["DELETE"])
@login_required
def delete_todo(todo_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_TODO_BY_ID, (todo_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {todo_id} not found."}), 404
    return jsonify({"message": f"Todo with ID {todo_id} deleted."})

@app.route('/secrets', methods=['POST'])
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
