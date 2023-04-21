from models.init_bd import s
from models.users_model import UserModel


def check_user(id_user_telegram):
    id_user = s.query(UserModel.id_user).filter(UserModel.id_telegram == str(id_user_telegram)).first()
    if id_user:
        s.close()
        return id_user[0]
    s.close()
    return False