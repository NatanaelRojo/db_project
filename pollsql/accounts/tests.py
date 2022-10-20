from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import CustomUser, identification_validator, phone_number_validator

# Create your tests here.

def create_user() -> CustomUser:
    user = CustomUser(
            username='test',
            password='testpassword',
            email='test@example.com'
    )
    return user

class CustomUserModelTests(TestCase):
    def test_allowed_characteres_to_identification(self):
        '''
            This function returns true for allowed characters to user identification
        '''
        user = create_user()
        user.identification = 'V26488388'
        self.assertIs(identification_validator(user.identification), None)
        user.identification = 'V9002765'
        self.assertIs(identification_validator(user.identification), None)
        user.identification = 'E14460252'
        self.assertIs(identification_validator(user.identification), None)
    
    def test_not_allowed_characters_to_identification(self):
        '''
            This function returns true for not allowed characters to identification
        '''
        user = create_user()
        try:
            user.identification = 'V26488a88'
            self.assertIs(identification_validator(user.identification), ValidationError('This identification is not valid'))
        except ValidationError:
            pass
        try:
            user.identification = 'Nv6488388'
            self.assertIs(identification_validator(user.identification), ValidationError('This identification is not valid'))
        except ValidationError:
            pass
        try:
            user.identification = 'E9)4?123'
            self.assertIs(identification_validator(user.identification), ValidationError('This identification is not valid'))
        except ValidationError:
            pass

    def test_allowed_characteres_to_phone_number(self):
        '''
            This function returns true for allowed characters to user phone number
        '''
        user = create_user()
        user.phone_number = '04126643200'
        self.assertIs(phone_number_validator(user.phone_number), None)
        user.phone_number = '04147453112'
        self.assertIs(phone_number_validator(user.phone_number), None)
        user.phone_number = '02712216694'
        self.assertIs(phone_number_validator(user.phone_number), None)
    
    def test_not_allowed_characters_to_phone_number(self):
        '''
            This function returns true for not allowed characters to phone number
        '''
        user = create_user()
        try:
            user.phone_number = '0412664a200'
            self.assertIs(phone_number_validator(user.phone_number), ValidationError('This phone number is not valid'))
        except ValidationError:
            pass
        try:
            user.phone_number = '0_4147_?31|d'
            self.assertIs(phone_number_validator(user.phone_number), ValidationError('This identification is not valid'))
        except ValidationError:
            pass
        try:
            user.phone_number = '0412664311'
            self.assertIs(phone_number_validator(user.phone_number), ValidationError('This identification is not valid'))
        except ValidationError:
            pass