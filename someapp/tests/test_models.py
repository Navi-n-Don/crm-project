import datetime
import tempfile
from django.test import TestCase

from interactions.models import Interaction, Keyword, Rating, Like
from main.constants import APPEALS
from someapp.models import Company, Phone, Email, Project
from users.models import Person


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(title='Test',
                               slug='test',
                               contact_person='Tester',
                               description='Test test TEST',
                               address='testing street, testhouse, 7/9')

    def test_title_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('title').max_length
        self.assertEquals(max_length, 250)

    def test_slug_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_contact_person_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('contact_person').verbose_name
        self.assertEquals(field_label, 'contact person')

    def test_contact_person_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('contact_person').max_length
        self.assertEquals(max_length, 250)

    def test_description_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_address_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_address_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('address').max_length
        self.assertEquals(max_length, 255)

    def test_company_title_is_title(self):
        company = Company.objects.get(id=1)
        expected_company = company.title
        self.assertEquals(expected_company, str(company))

    def test_save_object_slug(self):
        company = Company.objects.get(title='Test')
        company.save()
        self.assertEqual(company.slug, 'test')

    def test_get_absolute_url(self):
        company = Company.objects.get(id=1)
        self.assertEquals(company.get_absolute_url(), '/company-list/test/')


class PhoneModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(title='Test',
                                         slug='test',
                                         contact_person='Tester',
                                         description='Test test TEST',
                                         address='testing street, testhouse, 7/9')
        company.save()
        Phone.objects.create(phone_number='066-1234567', company=company)

    def test_phone_number_label(self):
        phone = Phone.objects.get(id=1)
        field_phone = phone._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_phone, 'phone number')

    def test_phone_number_max_length(self):
        phone = Phone.objects.get(id=1)
        max_length = phone._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 11)

    def test_company_is_company(self):
        phone = Phone.objects.get(id=1)
        field_company = phone.company
        self.assertTrue(type(field_company) is Company)

    def test_phone_is_phone_number(self):
        phone = Phone.objects.get(id=1)
        expected_phone = phone.phone_number
        self.assertEquals(expected_phone, str(phone))


class EmailModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(title='Test',
                                         slug='test',
                                         contact_person='Tester',
                                         description='Test test TEST',
                                         address='testing street, testhouse, 7/9')
        company.save()
        Email.objects.create(email_address='test@gmail.com', company=company)

    def test_email_address_label(self):
        email = Email.objects.get(id=1)
        field_phone = email._meta.get_field('email_address').verbose_name
        self.assertEquals(field_phone, 'email address')

    def test_email_address_max_length(self):
        email = Email.objects.get(id=1)
        max_length = email._meta.get_field('email_address').max_length
        self.assertEquals(max_length, 250)

    def test_company_is_company(self):
        email = Email.objects.get(id=1)
        field_company = email.company
        self.assertTrue(type(field_company) is Company)

    def test_email_is_email_address(self):
        email = Email.objects.get(id=1)
        expected_email = email.email_address
        self.assertEquals(expected_email, str(email))


class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(title='Test',
                                         slug='test',
                                         contact_person='Tester',
                                         description='Test test TEST',
                                         address='testing street, testhouse, 7/9')
        company.save()
        Project.objects.create(
            title='Project Test',
            slug='project-test',
            company=company,
            description='Test test TEST',
            begin='2022-01-01',
            end='2022-01-20',
            price='1500',
        )

    def test_title_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        self.assertEquals(max_length, 250)

    def test_slug_label(self):
        company = Project.objects.get(id=1)
        field_label = company._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_company_is_company(self):
        project = Project.objects.get(id=1)
        field_company = project.company
        self.assertTrue(type(field_company) is Company)

    def test_description_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_begin_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('begin').verbose_name
        self.assertEquals(field_label, 'begin')

    def test_end_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('end').verbose_name
        self.assertEquals(field_label, 'end')

    def test_price_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_price_max_length(self):
        project = Project.objects.get(id=1)
        max_digits = project._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)

    def test_project_title_is_title(self):
        project = Project.objects.get(id=1)
        expected_project = project.title
        self.assertEquals(expected_project, str(project))

    def test_save_object_slug(self):
        project = Project.objects.get(title='Project Test')
        project.save()
        self.assertEqual(project.slug, 'project-test')

    def test_get_absolute_url(self):
        project = Project.objects.get(id=1)
        self.assertEquals(project.get_absolute_url(), '/company-list/test/project-test/')

    def test_days_to_left_day(self):
        project = Project.objects.get(id=1)
        project.today_date = datetime.datetime(2022, 1, 4).date()
        project.begin = datetime.datetime(2022, 1, 5).date()
        project.end = datetime.datetime(2022, 2, 15).date()
        project.save()
        self.assertEqual(project.days_to, ['left 1 day', 'text-secondary'])

    def test_days_to_left_days(self):
        project = Project.objects.get(id=1)
        project.today_date = datetime.datetime(2022, 1, 4).date()
        project.begin = datetime.datetime(2022, 1, 14).date()
        project.end = datetime.datetime(2022, 2, 10).date()
        project.save()
        self.assertEqual(project.days_to, ['left 10 days', 'text-secondary'])

    def test_days_to_in_progress(self):
        project = Project.objects.get(id=1)
        project.today_date = datetime.datetime(2022, 1, 4).date()
        project.begin = datetime.datetime(2021, 12, 25).date()
        project.end = datetime.datetime(2022, 1, 10).date()
        project.save()
        self.assertEqual(project.days_to, ['In Progress', 'text-info'])

    def test_days_to_completed(self):
        project = Project.objects.get(id=1)
        project.today_date = datetime.datetime(2022, 1, 4).date()
        project.begin = datetime.datetime(2021, 11, 25).date()
        project.end = datetime.datetime(2021, 12, 15).date()
        project.save()
        self.assertEqual(project.days_to, ['Completed', 'text-success'])


class PersonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Person.objects.create(username='Tester',
                              image='test_image.png')

    def test_username_label(self):
        person = Person.objects.get(id=1)
        field_phone = person._meta.get_field('username').verbose_name
        self.assertEquals(field_phone, 'username')

    def test_username_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('username').max_length
        self.assertEquals(max_length, 150)

    def test_image_label(self):
        person = Person.objects.get(id=1)
        field_phone = person._meta.get_field('image').verbose_name
        self.assertEquals(field_phone, 'image')

    def test_person_username_is_username(self):
        person = Person.objects.get(id=1)
        expected_person = person.username
        self.assertEquals(expected_person, str(person))

    def test_add_photo_png(self):
        newPhoto = Person.objects.get(id=1)
        newPhoto.image = tempfile.NamedTemporaryFile(suffix=".png").name
        newPhoto.save()
        self.assertEqual(Person.objects.count(), 1)

    def test_add_photo_jpg(self):
        newPhoto = Person.objects.get(id=1)
        newPhoto.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        newPhoto.save()
        self.assertEqual(Person.objects.count(), 1)

    def test_add_photo_jpeg(self):
        newPhoto = Person.objects.get(id=1)
        newPhoto.image = tempfile.NamedTemporaryFile(suffix=".jpeg").name
        newPhoto.save()
        self.assertEqual(Person.objects.count(), 1)

    def test_add_photo_gif(self):
        newPhoto = Person.objects.get(id=1)
        newPhoto.image = tempfile.NamedTemporaryFile(suffix=".gif").name
        newPhoto.save()
        self.assertEqual(Person.objects.count(), 1)


class KeywordModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Keyword.objects.create(title='test_keyword')

    def test_title_label(self):
        keyword = Keyword.objects.get(id=1)
        field_keyword = keyword._meta.get_field('title').verbose_name
        self.assertEquals(field_keyword, 'title')

    def test_title_max_length(self):
        keyword = Keyword.objects.get(id=1)
        max_length = keyword._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_keyword_is_title(self):
        keyword = Keyword.objects.get(id=1)
        expected_keyword = keyword.title
        self.assertEquals(expected_keyword, str(keyword))


class RatingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Rating.objects.create(value=1)

    def test_value_label(self):
        rating = Rating.objects.get(id=1)
        field_rating = rating._meta.get_field('value').verbose_name
        self.assertEquals(field_rating, 'value')

    def test_rating_is_value(self):
        rating = Rating.objects.get(id=1)
        expected_rating = rating.value
        self.assertEquals(expected_rating, int(str(rating)))


class InteractionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(title='Test',
                                         slug='test',
                                         contact_person='Tester',
                                         description='Test test TEST',
                                         address='testing street, testhouse, 7/9')
        company.save()

        project = Project.objects.create(
            title='Project Test',
            slug='project-test',
            company=company,
            description='Test test TEST',
            begin='2022-01-01',
            end='2022-01-20',
            price='1500',
        )
        project.save()

        person = Person.objects.create(
            username='Manager',
            image='test_image.png',
        )
        person.save()

        keyword1 = Keyword.objects.create(title='keyword1')
        keyword2 = Keyword.objects.create(title='keyword2')
        keyword1.save()
        keyword2.save()

        action = Interaction.objects.create(
            project=project,
            appeals=APPEALS.choices,
            manager=person,
            description='Test test TEST',
        )
        action.keyword.set([keyword1.pk, keyword2.pk])

    def test_project_is_project(self):
        action = Interaction.objects.get(id=1)
        field_project = action.project
        self.assertTrue(type(field_project) is Project)

    def test_appeals_label(self):
        action = Interaction.objects.get(id=1)
        field_label = action._meta.get_field('appeals').verbose_name
        self.assertEquals(field_label, 'appeals')

    def test_manager_label(self):
        action = Interaction.objects.get(id=1)
        field_manager = action.manager
        self.assertTrue(type(field_manager) is Person)

    def test_description_label(self):
        action = Interaction.objects.get(id=1)
        field_label = action._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_keyword_is_keyword(self):
        action = Interaction.objects.get(id=1)
        for keyword in action.keyword.all():
            self.assertTrue(type(keyword) is Keyword)

    def test_get_appeals_string(self):
        action = Interaction.objects.get(id=1)
        action.appeals = APPEALS.REQUEST
        action.save()
        self.assertEqual(action.get_appeals(), 'Request')


class LikeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(title='Test',
                                         slug='test',
                                         contact_person='Tester',
                                         description='Test test TEST',
                                         address='testing street, testhouse, 7/9')
        company.save()

        project = Project.objects.create(
            title='Project Test',
            slug='project-test',
            company=company,
            description='Test test TEST',
            begin='2022-01-01',
            end='2022-01-20',
            price='1500',
        )
        project.save()

        person = Person.objects.create(
            username='Manager',
            image='test_image.png',
        )
        person.save()

        action = Interaction.objects.create(
            project=project,
            appeals=APPEALS.choices,
            manager=person,
            description='Test test TEST',
        )

        rating = Rating.objects.create(value=1)
        rating.save()

        Like.objects.create(
            who=person,
            action=action,
            like=rating,
        )

    def test_who_label(self):
        like = Like.objects.get(id=1)
        field_who = like.who
        self.assertTrue(type(field_who) is Person)

    def test_action_is_action(self):
        like = Like.objects.get(id=1)
        field_action = like.action
        self.assertTrue(type(field_action) is Interaction)

    def test_like_is_like(self):
        like = Like.objects.get(id=1)
        field_like = like.like
        self.assertTrue(type(field_like) is Rating)

    def test_like_is_action_who(self):
        like = Like.objects.get(id=1)
        action = like.action
        action.appeals = APPEALS.REQUEST
        action.save()
        expected_action_who = f'{action.get_appeals()} - {like.who}'
        self.assertEquals(expected_action_who, str(like))
