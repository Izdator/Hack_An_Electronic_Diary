# Электронный дневник школы

Этот сайт - интерфейс для учеников школы. Здесь можно посмотреть оценки, расписание и прочую открытую информацию. Учителя заполняют базу данных через другой сайт. Ставят там оценки и т.д.

## Описание моделей

На сайте есть ученики: `Schoolkid`. Класс ученика определяется через комбинацию его полей `year_of_study` — год обучения и `group_letter` — литера класса. Вместе получается, например, 10А. Ученик связан со следующими моделями:

- `Mark` — оценка на уроке, от 2 до 5.
- `Commendation` — похвала от учителя, за особые достижения.
- `Chastisement` — замечание от учителя, за особые проступки.

Все 3 объекта связаны не только с учителем, который их создал, но и с учебным предметом (`Subject`). Примеры `Subject`:

- Математика 8 класса
- Геометрия 11 класса
- Русский язык 1 класса
- Русский язык 4 класса

`Subject` определяется не только названием, но и годом обучения, для которого учебный предмет проходит.

За расписание уроков отвечает модель `Lesson`. Каждый объект `Lesson` — урок в расписании. У урока есть комбинация `year_of_study` и `group_letter`, благодаря ей можно узнать для какого класса проходит этот урок. У урока есть `subject` и `teacher`, которые отвечают на вопросы "что за урок" и "кто ведёт". У урока есть `room` — номер кабинета, где он проходит. Урок проходит в дату `date`.

Расписание в школе строится по слотам:

- 8:00-8:40 — 1 урок
- 8:50-9:30 — 2 урок
- ...

У каждого `Lesson` есть поле `timeslot`, которое объясняет, какой номер у этого урока в расписании.

## Запуск

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте БД командой `python3 manage.py migrate`
- Запустите сервер командой `python3 manage.py runserver`

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:
- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `DATABASE_NAME` — путь до базы данных, например: `schoolbase.sqlite3`

# Скрипт управления школьной системой

Этот скрипт позволяет исправлять оценки, удалять замечания и писать похвалы в учебной системе.

## Описание

Скрипт выполняет следующие функции:

1. **Исправление оценок** - изменяет оценки 2 и 3 на 5 для выбранного ученика.
2. **Удаление замечаний** - удаляет все замечания у выбранного ученика.
3. **Создание похвалы** - создает похвалу с использованием случайных положительных фраз для случайно выбранного урока по указанному предмету для указанного ученика.

## Установка

1. Убедитесь, что у вас установлен Python и Django.
2. Склонируйте репозиторий или скачайте файл со скриптом в папку.
3. Чтобы запустить скрипт, можно его целиком копипастнуть в shell, а можно положить файл с кодом рядом с `manage.py` и подключить через import. 

## Запуск shell
```
python manage.py shell
```
## Импортируйте необходимые модели и выполните функции:
```
python
import random
from datacenter.models import Schoolkid, Teacher, Subject, Lesson, Mark, Chastisement, Commendation
```
### Примеры использования

- **Исправление оценок:**
```
python
schoolkid = get_schoolkid_by_name('Фролов Иван')
fix_marks([schoolkid])
```
Скопируйте код в shell и замените 'Фролов Иван' на нужного ученика. Следите за правильностью написания имени и фамилии во избежание ошибок.

- **Удаление замечаний:**
```
python
schoolkid_for_chastisements = get_schoolkid_by_name('Голубев Феофан')
remove_chastisements([schoolkid_for_chastishments])
```
Скопируйте код в shell и замените 'Голубев Феофан' на нужного ученика. Следите за правильностью написания имени и фамилии во избежание ошибок.

- **Создание похвалы:**
```
python
praise = create_commendation("Фролов Иван", "Музыка")
if praise:
    print(praise)
```
Скопируйте код в shell и замените 'Фролов Иван' на нужного ученика, а "Музыка" на нужный предмет. Следите за правильностью написания имени и фамилии, а также предмета во избежание ошибок.

## Тестирование

### 1. Исправить оценки
- Убедитесь, что у вас есть доступ к сайту электронного дневника.
- Запустите скрипт, следуя инструкциям в README.
- Проверьте, исправлены ли оценки, исчезли ли замечания и появилась ли похвала от учителя.

### 2. Помогите друзьям
- Запустите скрипт для друга, следуя тем же инструкциям.
- Проверьте, исправлены ли его оценки и исчезли ли замечания.

### 3. Многократное использование
- Запускайте скрипт в течение учебного года, чтобы исправлять оценки, удалять жалобы и добавлять похвалу.
- Убедитесь, что текст похвалы меняется при каждом запуске.

### 4. Ошибки ввода
- Проверьте, как скрипт обрабатывает ошибки ввода, например, если имя ученика указано неверно или оставлено пустым.
- Убедитесь, что скрипт сообщает о проблемах и предлагает исправления.

### 5. Что за проект?
- Если вы случайно наткнулись на этот репозиторий, вы можете узнать, как этот код связан с электронным дневником и что он делает.

### 6. Хочу такой же
- Если вы хотите развернуть код у себя, следуйте инструкциям в README и настройте базу данных и сайт.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

