## Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр. Новые жанры может создавать только администратор. Пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Присутствует возможность комментирования отзывов.

Функционал API:
1) Просмотр произведений (кино, музыка, книги), которые подразделяются по жанрам и категориям..
2) Возможность оставлять отзывы на произведения и ставить им оценки, на основе которых построена система рейтингов.
3) Комментирование оставленных отзывов.

Проект разработан командой из трех человек с использованием Git в рамках учебного курса Яндекс.Практикум.

## Разработчики

1. Дамир Шамсутдинов ([ссылка на GitHub](https://github.com/DamirShamsutdinov)):
Разработка системы регистрации и аутентификации, прав доступа, работы с токеном, системы подтверждения через e-mail, скрипт по импорту CSV-файлов.

2. Михаил Глазов ([ссылка на GitHub](https://github.com/Anxeity)):
Разработка моделей "категории" (Categories), "жанры" (Genres) и "произведения" (Titles), а также разработка представлений и эндпойнтов для них.

3. Алексей Смирнов ([ссылка на GitHub](https://github.com/AxelVonReems)):
Разработка моделей "отзывы" (Review) и "комментарии" (Comments), а также разработка представлений и эндпойнтов для них. Настройка прав доступа для запросов. Реализация системы рейтингов.

## Стек технологий

![python version](https://img.shields.io/badge/Python-3.9-yellowgreen) 
![python version](https://img.shields.io/badge/Django-2.2.16-yellowgreen) 
![python version](https://img.shields.io/badge/djangorestframework-3.12.4-yellowgreen) 
![python version](https://img.shields.io/badge/djangorestframework--simplejwt-5.1-yellowgreen) 

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/alvaresShD/api_yamdb.git
cd api_yamdb
```

Перейти в папку с проектом

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
WIN: python -m venv venv
MAC: python3 -m venv venv
```

```
WIN: source venv/scripts/activate
MAC: source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
WIN: python -m pip install --upgrade pip
MAC: python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
WIN: python manage.py migrate
MAC: python3 manage.py migrate
```

Запустить проект:

```
WIN: python manage.py runserver
MAC: python3 manage.py runserver
```

[Примеры запросов и документация по ссылке](http://127.0.0.1:8000/redoc/)
