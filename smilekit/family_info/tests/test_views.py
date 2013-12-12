from django.test import TestCase
from django.test.client import Client
from smilekit.family_info.views import default_family_form_vars
from .factories import UserFactory, ConfigurationFactory


class DefaultFamilyFormVarsTest(TestCase):
    def test_basics(self):
        r = default_family_form_vars()
        self.assertEqual(r['equation_balancer_configs'].count(), 0)


class LoggedInViewsTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = UserFactory()
        self.u.set_password("test")
        self.u.save()
        self.c.login(username=self.u.username, password="test")

    def test_families(self):
        r = self.c.get("/family_info/families/")
        self.assertEqual(r.status_code, 200)

    def test_new_user_form(self):
        r = self.c.get("/family_info/new_user/")
        self.assertEqual(r.status_code, 200)

    def test_insert_user(self):
        r = self.c.post(
            "/family_info/insert_user/",
            dict(
                username="added",
                first_name="added",
                last_name="throughtheweb",
                password="password",
                password_2="password",
            )
        )
        self.assertEqual(r.status_code, 200)

    def test_edit_user_get(self):
        r = self.c.get("/family_info/edit_user/%d/" % self.u.id)
        self.assertEqual(r.status_code, 200)

    def test_new_family_form(self):
        r = self.c.get("/family_info/new_family/")
        self.assertEqual(r.status_code, 200)

    def test_insert_family(self):
        c = ConfigurationFactory(owner=self.u)
        r = self.c.post(
            "/family_info/insert_family/",
            dict(
                study_id_number="1",
                child_year_of_birth="2000",
                config_id=c.id,
                mother_born_in_us='True',
                food_stamps_in_last_year='True',
                race_ethnicity='martian',
                highest_level_of_parent_education='PhD',
            )
        )
        self.assertEqual(r.status_code, 200)

    def test_dashboard(self):
        r = self.c.get("/family_info/dashboard/")
        self.assertEqual(r.status_code, 200)

    def test_help_summary(self):
        r = self.c.get("/family_info/help_summary/")
        self.assertEqual(r.status_code, 200)

    def test_question_list(self):
        r = self.c.get("/family_info/question_list/")
        self.assertEqual(r.status_code, 200)

    def test_summary_table(self):
        r = self.c.get("/family_info/summary_table/")
        self.assertEqual(r.status_code, 200)

    def test_food_table(self):
        r = self.c.get("/family_info/food_table/")
        self.assertEqual(r.status_code, 200)

    def test_kill_localstorage(self):
        r = self.c.get("/family_info/kill/localstorage/")
        self.assertEqual(r.status_code, 200)

    def test_selenium(self):
        self.u.is_staff = True
        self.u.save()
        r = self.c.get("/family_info/selenium/setup/")
        self.assertEqual(r.status_code, 200)
