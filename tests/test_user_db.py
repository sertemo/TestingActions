from testingactions.user_db import (create_user, 
                                    PasswordTooShortError,
                                    InvalidUsernameError,
                                    block_user,
                                    UserState,
                                    activate_user,
                                    inactivate_user)
import pytest



def test_create_user_invalid_password_too_short(db_conn):
    with pytest.raises(PasswordTooShortError):
        create_user('Pedro', 51, '234', db_conn=db_conn, collection='usuarios')


def test_create_user_two_words_username(db_conn):
    with pytest.raises(InvalidUsernameError):
        create_user('Juan Rodriguez', 43, '1223', db_conn=db_conn, collection='usuarios')


def test_create_user_already_exist(db_conn):
    with pytest.raises(InvalidUsernameError):
        create_user('pedro', 51, '23480322', db_conn=db_conn, collection='usuarios')
        create_user('Pedro', 44, '2345', db_conn=db_conn, collection='usuarios')


def test_block_user_correct(db_conn):
    create_user('sertemo', 51, '23480322', db_conn=db_conn, collection='usuarios')
    assert block_user(db_conn, 'usuarios', 'sertemo') == {'username': 'sertemo',
                                                            'edad': 51,
                                                            'password': '23480322',
                                                            'state': UserState.blocked}

def test_block_user_incorrect(db_conn):
    create_user('carmksd', 33, '23480322', db_conn=db_conn, collection='usuarios')
    assert block_user(db_conn, 'usuarios', 'rodri98') is None


def test_activate_user_correct(db_conn):
    create_user('regekod', 24, '234e20322', db_conn=db_conn, collection='usuarios')
    assert activate_user(db_conn, 'usuarios', 'regekod') == {'username': 'regekod',
                                                            'edad': 24,
                                                            'password': '234e20322',
                                                            'state': UserState.active}    


def test_inactivate_user_correct(db_conn):
    create_user('pp', 24, '234e20322', db_conn=db_conn, collection='usuarios')
    assert inactivate_user(db_conn, 'usuarios', 'pp') == {'username': 'pp',
                                                            'edad': 24,
                                                            'password': '234e20322',
                                                            'state': UserState.inactive}  
    

def test_check_default_state_on_creation(db_conn):
    create_user('lapikot2', 67, '234e20322', db_conn=db_conn, collection='usuarios')
    user = db_conn.find_one('lapikot2', 'usuarios')
    assert user.state == UserState.inactive


def test_no_collection(db_conn):
    with pytest.raises(AttributeError):
        create_user('lapikot2', 67, '234e20322', db_conn=db_conn, collection='animales')


def test_no_user(db_conn):
    assert db_conn.find_one('perro', 'usuarios') is None


def test_inactivate_user_incorrect(db_conn):
    create_user('ppop', 24, '24e20322', db_conn=db_conn, collection='usuarios')
    assert inactivate_user(db_conn, 'usuarios', 'usuario_que_no_existe') is None
    

@pytest.mark.xfail # Marcamos que sabemos que va a fallar
def test_divide_by_zero():
    assert 1 / 0 == 1