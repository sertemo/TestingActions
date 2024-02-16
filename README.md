# TestingActions

![Tests](https://github.com/sertemo/TestingActions/actions/workflows/tests.yml/badge.svg)

## Pequeño proyecto para probar las GitHub Actions
Automatización de testing con pytest, Flake8 y mypy y tox

Tutorial del canal **mCoding** de [James Murphy](https://www.youtube.com/watch?v=DhUpxWjOhME&ab_channel=mCoding)

[Repo del proyecto](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/blob/main/src/slapping/slap_that_like_button.py)

Configuración de [**pytest**](https://docs.pytest.org/en/stable/reference/customize.html) y [**mypy**](https://mypy.readthedocs.io/en/stable/config_file.html) en **pyproject.toml**

Configuración de [**Flake8**](https://www.flake8rules.com/rules/W292.html) en **setup.cfg**

Importante ejecutar para crear el paquete
```sh
poetry install
```

Comandos para pasar los tests
```sh
poetry run pytest
```

```sh
flake8 src
```

```sh
mypy src
```

## Cómo sabemos que los tests también pasarán en otros entornos virtuales ?
Usamos [**Tox**](https://tox.wiki/en/4.12.1/config.html)

Archivo de  configuración **tox.ini**

```sh
tox -v # Para verbose
```

## Configuramos GitHub Actions
Lanzamos **tox** cada vez que se ejecute un push en la rama main del repositorio.
Configuramos github actions con un fichero **.yml** dentro de **.github/workflows**

Tenemos que añadir a tox.ini sección [gh-actions]