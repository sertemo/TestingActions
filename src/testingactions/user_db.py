import enum
from dataclasses import dataclass

COLLECTION = 'usuarios'


class PasswordTooShort(Exception):
    pass


class UserState(enum.Enum):
    active = enum.auto()
    inactive = enum.auto()
    blocked = enum.auto()


@dataclass
class User:
    username: str
    edad: int
    password: str
    state: UserState = UserState.inactive


class DataBase:
    def __init__(self, uri: str) -> None:
        self.URI = uri
        self.db: dict[str, list[User]] = {}

    def create_collection(self, collection: str) -> None:
        if collection not in self.db:
            self.db[collection] = []
        else:
            raise ValueError(f"La colección {collection} ya existe")

    def add(self, user: User, collection: str) -> None:
        if collection not in self.db:
            raise AttributeError(f"La colección {collection} no existe. \
            Debes crearla primero con create_collection()")
        self.db[collection].append(user)

    def get_users(self, collection: str) -> list[User]:
        if collection not in self.db:
            raise AttributeError(f"La colección {collection} no existe. \
            Debes crearla primero con create_collection()")
        return self.db[collection]

    def find_one(self, username: str, collection: str) -> User | None:
        if collection not in self.db:
            raise AttributeError(f"La colección {collection} no existe. \
            Debes crearla primero con create_collection()")
        for user in self.db[collection]:
            if user.username == username:
                return user
        return None


def inactivate_user(
        db_conn: DataBase,
        collection: str,
        username: str
        ) -> dict[str, str | int | UserState] | None:
    user = db_conn.find_one(username, collection)
    if user is not None:
        user.state = UserState.inactive
        return user.__dict__
    return None


def activate_user(
        db_conn: DataBase,
        collection: str,
        username: str
        ) -> dict[str, str | int | UserState] | None:
    user = db_conn.find_one(username, collection)
    if user is not None:
        user.state = UserState.active
        return user.__dict__
    return None


def block_user(
        db_conn: DataBase,
        collection: str,
        username: str
        ) -> dict[str, str | int | UserState] | None:
    user = db_conn.find_one(username.lower(), collection)
    if user is not None:
        user.state = UserState.blocked
        return user.__dict__
    return None


def create_user(
        username: str,
        edad: int,
        password: str,
        *,
        db_conn: DataBase,
        collection: str
        ) -> dict[str, str | int | UserState]:
    if user_already_exists(
                            username, db_conn, collection):
        raise ValueError(
                        f"El usuario {username} ya existe \
                        en la colección {collection}")
    if not is_valid_password(password):
        raise PasswordTooShort(
                        "El password no es válido. \
                        Debe tener al menos 4 dígitos.")
    if not username_is_not_one_word(username):
        raise ValueError("El username no puede contener espacios")
    user = User(username.lower(), edad, password)
    db_conn.add(user, collection)
    return user.__dict__


# Validaciones
def username_is_not_one_word(username: str) -> bool:
    return len(username.split()) == 1


def user_already_exists(
        username: str,
        db_conn: DataBase,
        collection: str) -> bool:
    if db_conn.find_one(username.lower(), collection):
        return True
    else:
        return False


def is_valid_password(password: str) -> bool:
    return len(password) >= 4


def main() -> None:
    # Instanciamos db
    db_conn = DataBase('mongodb://sertemo.db')
    # Creamos colección usuarios
    db_conn.create_collection(COLLECTION)

    # Creamos un usuario
    create_user('Sergio', 39, '1111', db_conn=db_conn, collection=COLLECTION)
    create_user('Leire', 36, '2345', db_conn=db_conn, collection=COLLECTION)
    create_user('inhar', 2, '3456', db_conn=db_conn, collection=COLLECTION)

    print(block_user(db_conn, COLLECTION, 'Sergio'))

    print(db_conn.get_users(COLLECTION))


if __name__ == '__main__':
    main()
