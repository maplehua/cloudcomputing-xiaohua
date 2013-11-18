from flask.ext.wtf import Form
from wtforms import TextField, HiddenField, PasswordField, SubmitField
from wtforms import validators
from app.models.User import User

class SearchForm(Form):
    keyword = TextField(validators = [validators.Required(), validators.Length(max = 127)])
    offset = HiddenField(default = 0, validators = [validators.Required()])
    theme = HiddenField(default = 'none', validators = [validators.Required()])
    page = HiddenField(default = 1)

class LoginForm(Form):
    username = TextField(validators = [validators.Required(), validators.Length(max = 20)])
    password = PasswordField(validators = [validators.Required(), validators.Length(max = 20)])
    submit = SubmitField('Login')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = self.get_user()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        if user.password != self.password.data:
            self.password.errors.append('Invalid password')
            return False

        return True

    def get_user(self):
        return User.objects(username = self.username.data).first()

class RegistrationForm(Form):
    username = TextField(validators = [validators.Required()])
    password = PasswordField(validators = [validators.Required()])

    def validate_login(self, field):
        if User.objects(username = self.username.data):
            raise validators.ValidationError('Duplicate username')
