# Создайте декоратор access_control, который ограничивает доступ к функции на основе переданных ролей пользователя.
# Декоратор должен принимать аргументы, определяющие допустимые роли (например, @access_control(roles=['admin', 'moderator'])).

# Требования:
#
# - Если текущий пользователь имеет одну из допустимых ролей, функция выполняется.
# - Если нет, выбрасывается исключение PermissionError с соответствующим сообщением.
# - Реализуйте механизм определения текущей роли пользователя. Для целей задания можно использовать
#   глобальную переменную или контекстный менеджер.


user_role=None


class RoleContextManager:
    def __init__(self, role):
        global user_role
        user_role = role

    def __enter__(self):
        print("Вход в контекстный менеджер, назначение роли")

    def __exit__(self, exc_type, exc_val, exc_tb):
        global user_role
        user_role= None
        print("Выход из контекстного менеджера")



def access_control(roles=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if user_role in roles:
                return func(*args, **kwargs)
            raise PermissionError(f"У роли {user_role} нет доступа")
        return wrapper
    return decorator



@access_control(roles=["admin", "director"])
def print_hello():
    print("hello")


with RoleContextManager("admin") as manager:
    print_hello()


print(user_role)