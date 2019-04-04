import datetime
from pynamodb import models, attributes


class User(models.Model):
    """ this is the model for our users table """

    username = attributes.UnicodeAttribute(hash_key=True)
    password = attributes.UnicodeAttribute()
    github = attributes.UnicodeAttribute()
    groups = attributes.UnicodeSetAttribute()
    created = attributes.UTCDateTimeAttribute(default=datetime.datetime.now())
    last_login = attributes.UTCDateTimeAttribute(default=datetime.datetime.now())

    class Meta:
        table_name = 'Pdpd_Users'
        region = 'ap-southeast-2'

    @classmethod
    def authenticate(cls, username: str, password: str):
        """ authenticate the user or fail. """
        try:
            user = cls.get(username)
            if user.password != password:
                raise ValueError("Password mismatch.")
            user.update({
                "last_login": {
                    "action": "put",
                    "value": datetime.datetime.now()
                }
            })
            return user
        except cls.DoesNotExist:
            raise ValueError("User does not exist.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_login = self.last_login

    @property
    def token_payload(self) -> dict:
        """ return the user object details for jwt """
        return {
            'sub': self.username,  # JWT standard uses sub as the subscriber id
            'github': self.github,
            'groups': self.groups,
            'last_login': self.previous_login,
            'this_login': self.last_login
        }


# create the table if it doesn't exist
# also add a test user
if not User.exists():
    User.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    bendog = User(username='bendog', password='pdpd', github='bendog', groups=['pdpd', 'ausvet', 'djangogirls', 'melbdjango', 'sailors'])
    bendog.save()
