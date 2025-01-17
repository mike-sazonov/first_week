# Напишите метакласс, который автоматически добавляет атрибут created_at с текущей датой и временем к любому классу,
# который его использует.

from datetime import datetime

class MetaCreatedAt(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, attrs)
