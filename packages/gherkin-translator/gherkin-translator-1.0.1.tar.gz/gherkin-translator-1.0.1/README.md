# Gherkin translator

Транслятор ключевых слов пользовательского сценария, написанного на [gherkin](https://wellbehaved.readthedocs.io/Gherkin.html), из русского языка в английский

Скрипт переводит ключевые слова gherkin с русского на английский для удобства переноса тест-кейсов в TMS Zephyr.

До:

```gherkin
@positive
Структура сценария: Успешная авторизация по логину и паролю
  Дано есть логин и пароль пользователя, который предварительно зарегистрирован в ЕЛК
    | name     | value      |
    | email    | <email>    |
    | phone    | <phone>    |
    | password | <password> |
  Когда вызываем метод авторизации по логину и паролю
  Тогда получаем ответ с кодом статуса "200"
  И получаем тело ответа в формате json
  И в теле ответа есть токен авторизации

  Примеры:
    | email             | phone        | password   |
    | odeto@rover.info  | null         | Test123456 |
    | null              | +79999999123 | Test123456 |
    | ukkosu@rover.info | +79999999567 | Test123456 |
```

После:

```gherkin
@positive
Scenario: Успешная авторизация по логину и паролю
Given есть логин и пароль пользователя, который предварительно зарегистрирован в ЕЛК
  | name     | value      |
  | email    | <email>    |
  | phone    | <phone>    |
  | password | <password> |
When вызываем метод авторизации по логину и паролю
Then получаем ответ с кодом статуса "200"
And получаем тело ответа в формате json
And в теле ответа есть токен авторизации

Examples:
  | email             | phone        | password   |
  | odeto@rover.info  | null         | Test123456 |
  | null              | +79999999123 | Test123456 |
  | ukkosu@rover.info | +79999999567 | Test123456 |
```


## Зависимости

Для реализации CLI интерфейса используется [typer](https://typer.tiangolo.com/)


## Установка модуля

```shell
pip install gherkin-translator
```

## Использование

```shell
python -m gherkin_translator path/to/test.feature
```

Можно также указывать путь до директории. В таком случае скрипт будет искать все файлы фич, заканчивающиеся на `.feature` и будет пытаться перевести их.
