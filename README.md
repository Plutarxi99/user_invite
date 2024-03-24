# user_invite
Сервис для реферальной системы

<details>
<summary>Что делает приложение?</summary>
Функционал:
* Пользователь регистрируется и создаёт свой аккаунт. Изначально он не активен
* Пользователь может зарегестрироваться как реферал имея реферальный код
* Пользователь логиниться на сервисе и ему высылается на почту bearer token
* Через эндпоинт он устанавливает к себе в cookie браузера bearer token
* Работа с бд PostgreSQL
* Создавать пользователя может только админ
* К сервису к кадому эндпоинту написаны тесты
* Подключена докуменация и swagger для работы через браузер.
* Пользователь может получиться информация о себе, может ее изменять информация о себе и выводить список пользователей
* Админ может создавать, изменять, удалять и получаться постраничный список пользователей
</details>

> [!IMPORTANT]
> Добавлен файл .env-sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **SECRET_KEY**| ahrfgyu34hfy3qh4fy4hufy3qfyb3k4f       |     код генерируется командой, которая указана ниже|
|     **POSTGRES_DB**| NAME_BD   |     название базы данных |
|     **POSTGRES_USER**| USER_BD   |     название пользователя базы данных |
|     **POSTGRES_PASSWORD**| PASSWORD_BD   |     пароль базы данных |
|     **POSTGRES_SERVER**| HOST_BD   |     подключение к базе данных |
|     **POSTGRES_DRIVER**| postgresql   |     типы подключение к базе данных PostgreSQL |
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
|     **COOKIE_NAME**| bearer       |     название ключа cookie, который присвается пользователю при вхождение на сервис|
|     **EMAIL_TEST_USER**| test@test.ru       |     установить email для тестового пользоватлея|
|     **PASSWORD_TEST_USER**| test       |     установить пароль для тестового пользователя|

</details>

<details>

<summary>Как использовать?</summary>

* Переходим в папку где будет лежать код

* Копируем код с git:
  <pre><code>git clone git@github.com:Plutarxi99/storage_user.git</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* После установки нужных настроeк в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Создать секретный ключ:
  <pre><code>openssl rand -hex 32</code></pre>

* Удалить все миграции  storage_user/backend/migrations/versions;

* Создать базу данных:
  <pre><code>psql -U postgres</code></pre>
  <pre><code>create database storage_user;</code></pre>

* Заполнить файл .env и приложение готово к запуску;

* Создать первого пользователя в сервеси. Перейти в файл и исполнить его
  <pre><code>python3 backend/src/backend_pre_start.py </code></pre>


</details>

<details>

<summary>Что использовалось в приложение?</summary>
Функционал:

* Подключено fastapi_filter для пагинации
* Подключено jwt для авторизации пользователя Bearer token
* Подключено PostgreSQL
* Обложил тестами все эндпоинты сервиса
* Добавил миграции с помощью alembic
* Добавил инструкции для создания docker-compose
</details>

<details>

<summary>Как запустить приложение в docker?</summary>
Функционал:

* Выполняем код:
  <pre><code>docker-compose build</code></pre>
  <pre><code>docker-compose up</code></pre>
  
* Для создания первого пользователя и начать пользоваться сервисом:
  <pre><code>docker exec app python3 backend/src/backend_pre_start.py</code></pre>
</details>


