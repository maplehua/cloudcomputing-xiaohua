from flask.ext.wtf import Form, TextField, HiddenField
from flask.ext.wtf import validators

class SearchForm(Form):
    keyword = TextField(validators = [validators.Length(max=40)])
    offset = HiddenField(default = 0, validators = [validators.Required()])
    theme = HiddenField(default = 'none', validators = [validators.Required()])
