from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextField

colors = ["", "red", "blue", "black_and_white"]


class SearchForm(FlaskForm):
    choices = [("Color", 'Color'),
               ("Orientation", 'Orientation')]
    select = SelectField('Search photos by:', choices=choices)
    search = StringField('')

    def validate_select(self, select):
        print("In error")
        if select.data == "Color" and self.search.data not in colors:
            self.select.errors.append(f"Please use one of {'[red, blue, white] for your color selection'}")
