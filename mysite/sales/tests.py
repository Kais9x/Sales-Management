from django.test import TestCase
import datetime
from django.utils import timezone
from .models import User
from django.urls import reverse


# Create your tests here.

def create_user(name, address, birthday, status, type_user, phone):
    """
    Create an User.
    """
    return User.object.create(name=name, address=address, birthday=birthday, status=status, type_user=type_user,
                              phone=phone)

class UserIndexViewTests(TestCase):
    def test_past_User(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        datetime_str = '09/19/22 13:55:26'

        datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        user = create_user(name='phong pham', address='t3k5', birthday=datetime_object, status=0, type_user='re',
                              phone='0985166472')
        response = self.client.get(reverse("sales"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [user],
        )
