# Setting up Translations

After setting up the models and views to support translations, you'll need to create translation files.

## Directory Structure

Ensure your project has this structure for translations:

```
project_root/
  ├── locale/
  │   ├── en/
  │   │   └── LC_MESSAGES/
  │   │       └── django.po
  │   ├── uz/
  │   │   └── LC_MESSAGES/
  │   │       └── django.po
  │   └── ru/
  │       └── LC_MESSAGES/
  │           └── django.po
```

## Creating Translation Files

1. First, make sure you've marked all strings for translation in your code using `_()` or `gettext_lazy()`:

   ```python
   from django.utils.translation import gettext_lazy as _
   
   error_message = _("This field is required.")
   ```

2. Create message files:

   ```bash
   python manage.py makemessages -l en
   python manage.py makemessages -l uz
   python manage.py makemessages -l ru
   ```

3. Edit the `.po` files in the `locale` directory to add translations.

4. Compile the messages:

   ```bash
   python manage.py compilemessages
   ```

## Example Translation for fields in `uz` (Uzbek)

```
#: users/models.py:80
msgid "Full Name"
msgstr "To'liq ism"

#: users/models.py:81
msgid "Age"
msgstr "Yosh"

#: users/models.py:83
msgid "Discovery Source"
msgstr "Kashfiyot manbasi"

#: users/models.py:84
msgid "STEM Level"
msgstr "STEM darajasi"

#: users/models.py:85
msgid "Motivation"
msgstr "Motivatsiya"

#: users/models.py:86
msgid "Daily Goal"
msgstr "Kunlik maqsad"

#: users/models.py:55
msgid "Google"
msgstr "Google"

#: users/models.py:56
msgid "Facebook"
msgstr "Facebook"

#: users/models.py:57
msgid "TikTok"
msgstr "TikTok"

#: users/models.py:58
msgid "Play Store"
msgstr "Play Store"

#: users/models.py:59
msgid "TV"
msgstr "Televideniye"

#: users/models.py:63
msgid "Beginner"
msgstr "Boshlang'ich"

#: users/models.py:64
msgid "Intermediate"
msgstr "O'rta"

#: users/models.py:65
msgid "Advanced"
msgstr "Yuqori"

#: users/models.py:69
msgid "Fun"
msgstr "Ko'ngil ochar"

#: users/models.py:70
msgid "Career"
msgstr "Karyera"

#: users/models.py:71
msgid "Education"
msgstr "Ta'lim"

#: users/models.py:72
msgid "Growth"
msgstr "Rivojlanish"

#: users/models.py:73
msgid "Society"
msgstr "Jamiyat"

#: users/models.py:77
msgid "5 minutes"
msgstr "5 daqiqa"

#: users/models.py:78
msgid "10 minutes"
msgstr "10 daqiqa"

#: users/models.py:79
msgid "15 minutes"
msgstr "15 daqiqa"

#: users/models.py:80
msgid "30 minutes"
msgstr "30 daqiqa"

#: users/models.py:81
msgid "60 minutes"
msgstr "60 daqiqa"
```

## Example Translation for fields in `ru` (Russian)

```
#: users/models.py:80
msgid "Full Name"
msgstr "Полное имя"

#: users/models.py:81
msgid "Age"
msgstr "Возраст"

#: users/models.py:83
msgid "Discovery Source"
msgstr "Источник открытия"

#: users/models.py:84
msgid "STEM Level"
msgstr "Уровень STEM"

#: users/models.py:85
msgid "Motivation"
msgstr "Мотивация"

#: users/models.py:86
msgid "Daily Goal"
msgstr "Дневная цель"

#: users/models.py:55
msgid "Google"
msgstr "Google"

#: users/models.py:56
msgid "Facebook"
msgstr "Facebook"

#: users/models.py:57
msgid "TikTok"
msgstr "TikTok"

#: users/models.py:58
msgid "Play Store"
msgstr "Play Store"

#: users/models.py:59
msgid "TV"
msgstr "ТВ"

#: users/models.py:63
msgid "Beginner"
msgstr "Начинающий"

#: users/models.py:64
msgid "Intermediate"
msgstr "Средний"

#: users/models.py:65
msgid "Advanced"
msgstr "Продвинутый"

#: users/models.py:69
msgid "Fun"
msgstr "Развлечение"

#: users/models.py:70
msgid "Career"
msgstr "Карьера"

#: users/models.py:71
msgid "Education"
msgstr "Образование"

#: users/models.py:72
msgid "Growth"
msgstr "Развитие"

#: users/models.py:73
msgid "Society"
msgstr "Общество"

#: users/models.py:77
msgid "5 minutes"
msgstr "5 минут"

#: users/models.py:78
msgid "10 minutes"
msgstr "10 минут"

#: users/models.py:79
msgid "15 minutes"
msgstr "15 минут"

#: users/models.py:80
msgid "30 minutes"
msgstr "30 минут"

#: users/models.py:81
msgid "60 minutes"
msgstr "60 минут"
```