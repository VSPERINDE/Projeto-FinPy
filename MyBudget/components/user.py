from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = user_data[
            "_id"
        ]  # Supondo que "_id" seja o identificador exclusivo do usuário no MongoDB
        self.email = user_data["email"]
        self.password = user_data["password"]
