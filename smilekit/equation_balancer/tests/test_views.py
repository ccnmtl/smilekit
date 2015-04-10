from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile

from smilekit.family_info.tests.factories import UserFactory
from smilekit.equation_balancer.models import (
    Configuration, ModuleWeight, Weight
)
from smilekit.equation_balancer.views import (
    index, view_config, new_config, delete_config, export_config,
    import_config, save_config, load_questions, load_patient_data,
    recalculate,
)
from .factories import (
    ConfigurationFactory, ModuleFactory, QuestionFactory
)


class TestRecalculate(TestCase):
    def setUp(self):
        self.c = Client()

    def test_recalculate(self):
        r = self.c.post('/weights/recalculate/', dict())
        self.assertEqual(r.status_code, 302)


class TestIndex(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/")
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)

    def test_index(self):
        request = self.factory.get("/weights/")
        request.user = UserFactory()
        response = index(request)
        self.assertEqual(response.status_code, 200)


class TestViewConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/configuration/0/")
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)

    def test_view_config(self):
        c = ConfigurationFactory()
        request = self.factory.get("/weights/configuration/%d/" % c.pk)
        request.user = UserFactory()
        response = view_config(request, c.pk)
        self.assertEqual(response.status_code, 200)


class TestNewConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/create/")
        request.user = AnonymousUser()
        response = new_config(request)
        self.assertEqual(response.status_code, 302)

    def test_view_config(self):
        request = self.factory.post(
            "/weights/create/",
            dict(name='new config'))
        request.user = UserFactory()
        new_config(request)
        r = Configuration.objects.filter(name='new config', owner=request.user)
        self.assertEqual(r.count(), 1)


class TestDeleteConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/delete/0/")
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)

    def test_delete_config(self):
        c = ConfigurationFactory()
        request = self.factory.post("/weights/delete/%d/" % c.pk)
        request.user = UserFactory()
        response = delete_config(request, c.pk)
        self.assertEqual(response.status_code, 302)
        r = Configuration.objects.filter(pk=c.pk)
        self.assertFalse(r.exists())

    def test_nonexistent_config(self):
        request = self.factory.post("/weights/delete/0/")
        request.user = UserFactory()
        response = delete_config(request, 0)
        self.assertEqual(response.status_code, 302)


class TestExportConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/export/0/")
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)

    def test_export_config(self):
        c = ConfigurationFactory()
        request = self.factory.get("/weights/export/%d/" % c.pk)
        request.user = UserFactory()
        response = export_config(request, c.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/csv')


class TestImportConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/import/")
        request.user = AnonymousUser()
        response = import_config(request)
        self.assertEqual(response.status_code, 302)

    def test_import_config_get(self):
        request = self.factory.get("/weights/import/")
        request.user = UserFactory()
        response = import_config(request)
        self.assertEqual(response.status_code, 302)

    def test_import_config_nocsv(self):
        request = self.factory.post(
            "/weights/import/",
            dict())
        request.user = UserFactory()
        response = import_config(request)
        self.assertEqual(response.status_code, 302)

    def test_import_config_csv_nodata(self):
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content='id,row\n'
            ))
        request = self.factory.post(
            "/weights/import/",
            dict(csvfile=f))
        request.user = UserFactory()
        response = import_config(request)
        self.assertEqual(response.status_code, 302)
        r = Configuration.objects.filter(name='test')
        self.assertEqual(r.count(), 1)

    def test_import_config_csv_with_data(self):
        m = ModuleFactory()
        q = QuestionFactory()
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content='id,row\nModule %s,1\nQuestion %d,2' % (
                    m.name, q.number)
            ))
        request = self.factory.post(
            "/weights/import/",
            dict(csvfile=f))
        request.user = UserFactory()
        response = import_config(request)
        self.assertEqual(response.status_code, 302)
        r = Configuration.objects.filter(name='test')
        self.assertEqual(r.count(), 1)
        r = ModuleWeight.objects.filter(module=m, weight=1)
        self.assertEqual(r.count(), 1)
        r = Weight.objects.filter(question=q, weight=2)
        self.assertEqual(r.count(), 1)


class TestSaveConfig(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/save/")
        request.user = AnonymousUser()
        response = save_config(request)
        self.assertEqual(response.status_code, 302)

    def test_save_config_no_data(self):
        c = ConfigurationFactory()
        request = self.factory.post(
            "/weights/save/",
            dict(config=c.pk, ajax='true')
        )
        request.user = UserFactory()
        response = save_config(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "")

    def test_save_config_clear_values(self):
        m = ModuleFactory()
        q = QuestionFactory(module=m)
        c = ConfigurationFactory()
        request = self.factory.post(
            "/weights/save/",
            {
                'config': c.pk,
                'ajax': 'true',
                'moduleweight-%d' % m.pk: "",
                'weight-%d' % q.number: "",
            }
        )
        request.user = UserFactory()
        response = save_config(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "")

        r = ModuleWeight.objects.filter(module=m, weight=0)
        self.assertEqual(r.count(), 1)
        r = Weight.objects.filter(question=q, weight=0)
        self.assertEqual(r.count(), 1)

    def test_save_config_set_values(self):
        m = ModuleFactory()
        q = QuestionFactory(module=m)
        c = ConfigurationFactory()
        request = self.factory.post(
            "/weights/save/",
            {
                'config': c.pk,
                'ajax': 'true',
                'moduleweight-%d' % m.pk: 5,
                'weight-%d' % q.number: 5,
            }
        )
        request.user = UserFactory()
        response = save_config(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "")

        r = ModuleWeight.objects.filter(module=m, weight=5)
        self.assertEqual(r.count(), 1)
        r = Weight.objects.filter(question=q, weight=5)
        self.assertEqual(r.count(), 1)


class TestLoadQuestions(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logged_out(self):
        request = self.factory.get("/weights/loadquestions/")
        request.user = AnonymousUser()
        response = load_questions(request)
        self.assertEqual(response.status_code, 302)

    def test_load_questions_nocsv(self):
        request = self.factory.post(
            "/weights/loadquestions/",
            dict())
        request.user = UserFactory()
        response = load_questions(request)
        # this is actually a bug in the code. It should be
        # returning an HttpResponse, not an empty dict
        # but for now...
        self.assertEqual(response, {})

    def test_load_questions_csv_nodata(self):
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content=(
                    '"question text,question number,answers,'
                    'numerical equivalent,module"\n')
            ))
        request = self.factory.post(
            "/weights/loadquestions/",
            dict(csvfile=f))
        request.user = UserFactory()
        response = load_questions(request)
        self.assertEqual(response.status_code, 302)

    def test_load_questions_csv_with_data(self):
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content=(
                    '"question text,question number,answers,'
                    'numerical equivalent,module"\n'
                    'qt,1,"foo,bar","1,2",foo')
            ))
        request = self.factory.post(
            "/weights/loadquestions/",
            dict(csvfile=f))
        request.user = UserFactory()
        response = load_questions(request)
        self.assertEqual(response.status_code, 302)


class TestLoadPatientData(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_load_patient_data_nocsv(self):
        request = self.factory.post(
            "/weights/loadquestions/",
            dict())
        response = load_patient_data(request)
        # this is actually a bug in the code. It should be
        # returning an HttpResponse, not an empty dict
        # but for now...
        self.assertEqual(response, {})

    def test_load_patient_data_csv_nodata(self):
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content=(
                    '1,2')
            ))
        request = self.factory.post(
            "/weights/loadquestions/",
            dict(csvfile=f))
        response = load_patient_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/javascript')

    def test_load_patient_data_csv_with_data(self):
        f = SimpleUploadedFile.from_dict(
            dict(
                filename='test.csv', content_type='text/csv',
                content=(
                    '1,2,3\n\n\n\n1,2,3\n2,2,3')
            ))
        request = self.factory.post(
            "/weights/loadquestions/",
            dict(csvfile=f))
        response = load_patient_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/javascript')


class TestRecalculateData(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_recalculate_empty(self):
        request = self.factory.post(
            "/weights/recalculate/",
            dict())
        response = recalculate(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/javascript')

    def test_recalculate_bs_params(self):
        request = self.factory.post(
            "/weights/recalculate/",
            dict(foo='foo', bar='bar'))
        response = recalculate(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/javascript')

    def test_recalculate(self):
        request = self.factory.post(
            "/weights/recalculate/",
            {
                'patient-1-1': "1",
                "weight-1": "1",
                "moduleweight-1": "1",
            }
        )
        response = recalculate(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/javascript')
