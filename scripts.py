from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random
from datacenter.models import Schoolkid, Teacher, Subject, Lesson, Mark, Chastisement, Commendation


PRAISES = [
    "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!",
    "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!",
    "Очень хороший ответ!", "Талантливо!", "Ты сегодня прыгнул выше головы!",
    "Я поражен!", "Уже существенно лучше!", "Потрясающе!", "Замечательно!",
    "Прекрасное начало!", "Так держать!", "Ты на верном пути!",
    "Здорово!", "Это как раз то, что нужно!", "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!", "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!", "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!", "Теперь у тебя точно все получится!"
]


def get_schoolkid_by_name(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=full_name)
        return schoolkid
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f'Ученик с именем "{full_name}" не найден.')
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned(f'Найдено несколько учеников с именем "{full_name}".')


def fix_marks(schoolkids):
    for schoolkid in schoolkids:
        low_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])

        if low_marks.exists():
            updated_count = low_marks.update(points=5)
            print(f'Исправлено оценок 2 и 3 на 5 для ученика {schoolkid.full_name}: {updated_count} оценок изменено.')
        else:
            print(f'У ученика {schoolkid.full_name} нет плохих оценок для исправления.')


def remove_chastisements(schoolkids):
    for schoolkid in schoolkids:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)

        if chastisements.exists():
            chastisements.delete()
            print(f'Все замечания для ученика {schoolkid.full_name} были удалены.')
        else:
            print(f'У ученика {schoolkid.full_name} нет замечаний.')


try:
    schoolkid = get_schoolkid_by_name('Фролов Иван')
    fix_marks([schoolkid])

    schoolkid_for_chastisements = get_schoolkid_by_name('Голубев Феофан')
    remove_chastisements([schoolkid_for_chastisements])

except ObjectDoesNotExist as e:
    print(e)
except MultipleObjectsReturned as e:
    print(e)


def create_commendation(student_full_name, subject_title):
    students_praises = Schoolkid.objects.filter(full_name__icontains=student_full_name).order_by('full_name')

    if not students_praises.exists():
        print(f"Ученик с именем '{student_full_name}' не найден.")
        return None
    elif students_praises.count() > 1:
        print(f"Найдено несколько учеников с именем '{student_full_name}'. Пожалуйста, уточните запрос.")
        return None

    student_praise = students_praises.first()

    try:
        subject_praise = Subject.objects.get(title=subject_title, year_of_study=student_praise.year_of_study)
    except ObjectDoesNotExist:
        print(f"Предмет '{subject_title}' для года обучения {student_praise.year_of_study} не найден.")
        return None

    lessons_praise = Lesson.objects.filter(
        year_of_study=student_praise.year_of_study,
        group_letter=student_praise.group_letter,
        subject=subject_praise,
    )

    if not lessons_praise.exists():
        print(f"Не найдено уроков по предмету '{subject_title}' для ученика {student_praise.full_name}.")
        return None

    random_lesson_praise = random.choice(lessons_praise)
    praise_text = random.choice(PRAISES)
    praise = Commendation.objects.create(
        text=praise_text,
        created=random_lesson_praise.date,
        schoolkid=student_praise,
        subject=subject_praise,
        teacher=random_lesson_praise.teacher
    )

    return praise


praise = create_commendation("Фролов Иван", "Музыка")
if praise:
    print(praise)
