import unittest
import flask_testing
from app import create_app
from app.forms import SearchForm, color_list, orientation_list


class TestSearchForm(flask_testing.TestCase):
    def create_app(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["DEBUG"] = True
        self.app.secret_key = "pass"
        return self.app

    def test_color_validation(self):
        with self.app.app_context():
            f = SearchForm()
            f.select.data = "Color"
            f.search.data = "pink"
            f.validate()
            err_msg = [f"Please use one of {color_list} for your color selection"]
            self.assertEqual(f.errors["select"], err_msg)

    def test_orientation_validation(self):
        with self.app.app_context():
            f = SearchForm()
            f.select.data = "Orientation"
            f.search.data = "rounded"
            f.validate()
            err_msg = [
                f"Please use one of {orientation_list} for your orientation selection"
            ]
            self.assertEqual(f.errors["select"], err_msg)


if __name__ == "__main__":
    unittest.main()
