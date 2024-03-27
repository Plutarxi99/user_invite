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
* Подключена докуменация и swagger для работы через браузер.  <pre><code>http://127.0.0.1:8000/docs#/</code></pre>
* Пользователь может получить действующий или создать новый реферальный код. Удалить его. Получить своих рефераллов или по id или email получить рефералов подписанных на указанных.
* Изменить о себе информацию
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
|     **MAIL_USERNAME**| fastapi_referal       |     названия твоего почтового сервиса|
|     **MAIL_PASSWORD**| qweq223e123edqwr       |     пароль полученный в настройках приложения для почтового сервиса P.S. Далее идет инструкция в картинках|
|     **MAIL_PORT**| 465       |     почтовый порт|
|     **MAIL_FROM**| <Твой почтовый адрес>       |     от кого придет почта|
|     **MAIL_SERVER**| <pre><code>smtp.yandex.ru</code></pre>      |      почтовый сервер, в моем случае это яндекс|
|     **EMAIL_TEST_USER**| test@test.ru       |     установить email для тестового пользоватлея|
|     **PASSWORD_TEST_USER**| test       |     установить пароль для тестового пользователя|
|     **CLEARBIT_API_SECRET**| sk_8caa...83d58c       |     ключи API сервиса clearbit https://dashboard.clearbit.com/api|
|     **CLEARBIT_API_PUBLIC**| pk_8caa...83d58c        |     ключи API сервиса clearbit https://dashboard.clearbit.com/api|
|     **REDIS_SERVER**| redis://localhost       |     подключение к бд редис, если это в докере, то он строится иначе и уже прописан|

</details>

<details>

<summary>Как использовать?</summary>

* Переходим в папку где будет лежать код

* Копируем код с git:
  <pre><code>git clone git@github.com:Plutarxi99/user_invite.git</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* После установки нужных настроeк в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Создать секретный ключ:
  <pre><code>openssl rand -hex 32</code></pre>

* Вставить его в .env

* Удалить все миграции  user_invite/backend/migrations/versions;

* Создать свою первую миграцию:
    <pre><code>alembic revision --autogenerate -m "name_migration"</code></pre>

* Создать базу данных:
  <pre><code>psql -U postgres</code></pre>
  <pre><code>create database user_invite;</code></pre>

* Заполнить файл .env и приложение готово к запуску;

* Для запуска в PyCharme использовал такие настройки запуска:
![Screenshot from 2024-03-25 15-13-13](https://github.com/Plutarxi99/user_invite/assets/132927381/c3894bbb-38e6-4c2f-93ca-995e59c8c8ed)

* Вам надо зарегистроваться и авторизоваться по эндпоинту:
![Screenshot from 2024-03-27 13-25-10](https://github.com/Plutarxi99/user_invite/assets/132927381/5dec5988-517f-4161-bdf2-39969ec8d486)

* После регистрации по эндпоинта вам на почту придет письмо с таким содержанием:
![Screenshot from 2024-03-27 13-22-51](https://github.com/Plutarxi99/user_invite/assets/132927381/12193474-9255-4743-a670-a06a3d8279c8)

* Содержимое надо скопировать и вставить в эндпоинт:
![Screenshot from 2024-03-27 13-25-56](https://github.com/Plutarxi99/user_invite/assets/132927381/b14dcfec-46c3-4b40-a347-67c36ef10213)

* Протустировать достаточно использовать команду:
  <pre><code>pytest</code></pre>

</details>

<details>

<summary>Как получить пароль почтового сервиса?</summary>
Функционал:

* Создать приложение по ссылке и создать приложение <<Почта>> и получить пароль:
  https://id.yandex.ru/security/app-passwords
![Screenshot from 2024-03-25 15-08-40](https://github.com/Plutarxi99/user_invite/assets/132927381/330bf584-9920-40a5-8324-5429f2d8ddc4)

* Скопировать пароль в .env файл оставльные настройка уже готовы.

</details>

<details>

<summary>Что использовалось в приложение?</summary>
Функционал:

* Подключено jwt для авторизации пользователя Bearer token
* Подключено PostgreSQL
* Добавил миграции с помощью alembic
* Добавил redis для кэширования реферального кода
* API интеграция https://app.clearbit.com для поулчения компании почтового адреса
* Добавил инструкции для создания docker-compose
* Добавил модуль тестрования основных эндпоинтов с созданием временной и тестовой базы данных на основе Pytest
</details>

<details>

<summary>Как запустить приложение в docker?</summary>
Функционал:

* Выполняем код:
  <pre><code>docker-compose build</code></pre>
  <pre><code>docker-compose up</code></pre>

* Подключаемся к контейнеру:
  <pre><code>http://127.0.0.1:8008/docs#/</code></pre>
</details>


