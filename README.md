Инструкция по установке и запуску.
=====

Установка:

```
git pull https://github.com/voron3x/trial.git
cd trial
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requires.txt
python manage.py syncdb
```

Запуск веб сервера:

```
source virtualenv/bin/activate
python ./manage.py runserver
```

Запуск тестов:

```
source virtualenv/bin/activate
python ./manage.py test
