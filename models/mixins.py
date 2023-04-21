from sqlalchemy.exc import IntegrityError

from models.init_bd import s


class ModelDbExt:
    def save(self):
        try:
            s.add(self)
            s.commit()
            return True
        except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
            s.rollback()
            return False
        except Exception as ex:
            s.rollback()
            return False

    def delete(self):
        try:
            s.delete(self)
            s.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def to_archive(self):
        self.is_archive = True
