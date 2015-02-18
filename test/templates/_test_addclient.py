from test import TemplateTestCase


class TestAddClient(TemplateTestCase):
    def test_should_have_access_to_app_object(self):
        app = self.html_by_id('add-client.html', 'appScript')
        self.assertHasCorrectAttr(app, 'type', 'text/javascript')

    def test_should_have_appropriate_form_for_adding_a_client(self):
        form = self.html_by_id('add-client.html', 'addClientForm')
        self.assertFormContainsAllFields(form, ('name', 'text'))
