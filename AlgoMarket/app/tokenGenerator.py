from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return sum([ord(let) for let in user.username]) + timestamp
        
token_generator = EmailTokenGenerator()