from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, URL

class TodoForm(FlaskForm):
    username = StringField('Cafe Username', validators=[DataRequired()])
    name = StringField("Cafe Name", validators=[DataRequired(), URL()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    todo = TextAreaField("Todo", validators=[DataRequired()])
    added_date = DateTimeField("Todo Added Date", validators=[DataRequired()])
    due_date = DateTimeField("Todo Due Date", validators=[DataRequired()])
    status = SelectField("Power Socket Availability", choices=["Archived", "Completed", "Has due date"], validators=[DataRequired()])
    submit = SubmitField('Submit')
