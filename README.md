# Photo assistant

## Описание

Photo assistant - это удобный web сервис для быстрого редактирования
изображений. На данный момент сервис предлагает вам добавить разнообразные
эффекты на изображение, а также с лёгкостью поможет удалить фон с картинки.
Все отредактированные изображения хранятся в галереи пользователя.

## Установка

Чтобы запустить приложение безупречно, удовлетворяйте требованиям
``
$ pip install -r requirements.txt
``

## Запустить сервер

```bash
$ python3 main.py
```

На UNIX/Linux/MacOS:

```bash
$ ./main.py
```

## Возможности

|                  |                 |
|------------------|-----------------|
| black_find_edges | quantization    |
| black_white      | red+            |
| blue+            | sharpness       |
| blur             | smooth          |
| green+           | violet+         |
| delete fon       | create a sketch |

**примеры изображений можно посмотреть в static/image**

## Структура базы данных

![Структура](/data/db/database_structure.png)

## API

| URL    | Описание             |
|--------|----------------------|
| /users | Список пользователей |
| /works | Список работ         |

***users***
 ```bash
{
  "users": [
    {
      "created_date": "2024-04-23 20:00:54",
      "email": "example@gmail.com",
      "id": 1,
      "is_premium": null,
      "login": "marsin"
    }
  ]
}
```
***works***
```bash
{
  "works": [
    {
      "id": 1,
      "name_file": "static/image/effect_im/examp.png",
      "type_works": "effect-black_white",
      "user_id": null
    }
  ]
}
```