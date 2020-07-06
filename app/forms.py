from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from app.utils import color_list, orientation_list


class SearchForm(FlaskForm):
    choices = [("Color", "Color"), ("Orientation", "Orientation")]
    select = SelectField("Search photos by:", choices=choices)
    search = StringField("")

    def validate_select(self, select):
        if select.data == "Color" and (
            self.search.data not in color_list and not self.search.data == ""
        ):
            self.select.errors.append(
                f"Please use one of {color_list} for your color selection"
            )
        elif select.data == "Orientation" and (
            self.search.data not in orientation_list and not self.search.data == ""
        ):
            self.select.errors.append(
                f"Please use one of {orientation_list} for your orientation selection"
            )
