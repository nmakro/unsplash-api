import unittest
import flask_testing
from unittest.mock import patch, Mock
from app import create_app


class TestRoutes(flask_testing.TestCase):
    render_templates = False

    def create_app(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["DEBUG"] = True
        self.app.secret_key = "pass"
        return self.app

    def setUp(self):
        self.patcher1 = patch("app.routes.SearchForm", autospec=True)
        self.patcher2 = patch("app.routes.requests", autospec=True)
        self.patcher3 = patch("app.utils.Image")

        self.mock_Form = self.patcher1.start()
        self.mock_Request = self.patcher2.start()
        self.mock_Image = self.patcher3.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def testAppCreated(self):
        self.assertTrue(self.app is not None)

    def testGetHomeRoute(self):
        with self.app.test_client() as c:
            self.mock_Form().validate_on_submit.return_value = False
            r = c.get("/")
            self.assertEqual(r.status_code, 200)
            self.assert_template_used("base.html")

    def testSearchPhoto(self):
        with self.app.test_client() as c:
            self.mock_Form().validate_on_submit.return_value = True
            r = c.post("/")
            self.assertRedirects(r, "/photo")

        with self.app.test_client() as c:
            self.mock_Form().validate_on_submit.return_value = False
            c.post("/")
            self.assert_template_used("base.html")

    def testPhotoRoute(self):
        with self.app.test_client() as c:
            attrs = {
                "json.return_value": {
                    "urls": {"small": "https://images.unsplash.com/photo-123"},
                    "id": "photo-123",
                }
            }
            self.mock_Request.get.side_effect = [
                Mock(status_code=200, **attrs),
                Mock(status_code=200, content=b"0x410x420x43"),
            ]
            self.mock_Request.head.return_value.headers.get.return_value = "image/jpeg"
            m = unittest.mock.mock_open()
            with unittest.mock.patch("app.utils.open", m):
                c.get("/photo")
                m.return_value.write.assert_called_with(b"0x410x420x43")
            self.assert_template_used("photo.html")

        self.mock_Request.get.reset_mock(side_effect=True, return_value=True)

        with self.app.test_client() as c:
            attrs = {
                "json.return_value": {
                    "urls": {"small": "https://images.unsplash.com/photo-123"},
                    "id": "photo-123",
                }
            }
            self.mock_Request.get.side_effect = [Mock(status_code=200, **attrs)]
            self.mock_Request.head.return_value.headers.get.return_value = (
                "video/x-msvideo"
            )
            res = c.get("/photo")
            self.assert_template_used("415.html")
            res.status_code = 415

    def testPhotoRouteError(self):
        with self.app.test_client() as c:
            self.mock_Request.get.return_value = Mock(status_code=404)
            c.get("/photo")
            self.assert_template_used("external_error.html")

        self.mock_Request.get.reset_mock(side_effect=True, return_value=True)

        with self.app.test_client() as c:
            attrs = {
                "json.return_value": {
                    "urls": {"small": "https://images.unsplash.com/photo-123"},
                    "id": "photo-123",
                }
            }
            self.mock_Request.get.side_effect = [
                Mock(status_code=200, **attrs),
                Mock(status_code=200, content=b"0x410x420x43"),
            ]
            self.mock_Request.head.return_value.headers.get.return_value = "image/jpeg"
            self.mock_Image.open.return_value.save.side_effect = Exception
            m = unittest.mock.mock_open()
            with unittest.mock.patch("app.utils.open", m):
                c.get("/photo")
            self.assert_template_used("500.html")


if __name__ == "__main__":
    unittest.main()
