# Боты для vk и telegram с распознаванием речи на основе Google DialogFlow
Боты предназначены для онлайн-издательства "Игра глаголов" для разгрузки
работников технической поддержки сервиса.

Основная цель - автоматизировать ответы на типичные вопросы пользователей
в Telegram и vk.com, такие как:
1. Приветствия пользователей;
2. Вопросы о забытом пароле, банах, удалении аккаунтов;
3. Вопросы от действующих партнеров;
4. Вопросы о устройстве на работу.

Для работы используется [Google DialogFlow](), что позволяет отвечать на вопросы,
заданные в произвольной форме. 
Если же бот не знает ответа, то отправляется сообщение модератору в 
Telegram с указанием социальной сети и id пользователя, который ожидает ответа.

Так же реализована возможность дообучать DialogFlow своими собственными вариантами вопросов и ответов.

## Как попробовать работу ботов
Есть два способа попробовать работу ботов - в vk.com и в telegram. Просто напиши им "Привет!".
1. Написать в сообщения группы [TestDialogFlow](https://vk.com/club207153259) в vk.com;
2. Написать боту в Telegram @DialogFlow_Chat3Bot

Пример работы Telegram бота:

![tg_bot_gif](https://user-images.githubusercontent.com/36712818/133781420-99a76676-ab11-422f-9ba1-0eacd5d580ca.gif)


## Используемые технологии
1. `python`
2. `python-telegram-bot`
3. `vk-api`
4. `DialogFlow`

## Установка и использование
Код состоит из 2-х ботов, хендлера Telegram для работы с логами и модуля для работы с api DialogFlow.

### Подготовка к работе бота vk_bot
1. Создать группу (если не создана), в настройках в разделе "Сообщения" включить возможность
отправлять сообщения группе;
2. В настройках группы в разделе "Работа с API" создать новый ключ с правами доступа "управление
сообществом" и "сообщения сообщества".
   
### Подготовка к работе бота tg_bot
1. Создать бота (написать боту @BotFather);
2. Получить токен созданного бота.

### Регистрация и получение json-ключа в Dialogflow
1. Создать проект в DialogFlow ([документация](https://cloud.google.com/dialogflow/es/docs/quick/setup))
2. Создать агента в DialogFlow ([документация](https://cloud.google.com/dialogflow/es/docs/quick/build-agent))
3. Получить json-ключ в настройках проекта ([документация](https://cloud.google.com/docs/authentication/getting-started))
4. Создать новый интент в агенте, наполнить его примерами вопросов и какие ответы должны быть на них.

### Переменные окружения
Для работы приложения необходимо внести чувствительные данные (пароли, токены) в переменные окружения:
1. `TG_BOT_TOKEN` - токен телеграм-бота
2. `DIALOGFLOW_PROJECT_ID` - id проекта в DiaflogFlow
3. `GOOGLE_APPLICATION_CREDENTIALS` - путь к json-файлу
4. `VK_BOT_TOKEN` - токен vk.vom 
5. `LOG_CHAT_ID` - id чата с юзером, которому будут отправлять от имени телеграм-бота сообщения 
об ошибках, уведомления и тд
   
### Установка зависимостей и запуск ботов на локальном компьютере
1. Для работы ботов на локальном компьютере необходимо создать файл `.env` с переменными окружения
и положить этот файл в корень проекта, рядом с файлами кода
2. Создать новое виртуальное окружение для python и активировать его
3. Установить все зависимости `pip install -r requirements.txt`
4. Выполнить команду в терминале `python vk_bot.py` или `python tg_bot.py` для запуска ботов.
Чтобы боты работали одновременно, то просто запусти второго бота в другом окне терминала
   
### Деплой ботов на heroku
1. Сделать форк данного репозитория на github
2. Создать новый проект на heroku
3. На вкладке "Deploy" привязать репозиторий к проекту
4. На вкладке "Settings" в разделе "Buildpacks" добавить новый билдпак: 
[https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack](https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack)
5. На той же вкладке в разделе Config Vars прописать все переменные окружения, описанные выше.

**Важный момент**:
В переменные окружения добавляем еще одну переменную `GOOGLE_CREDENTIALS` и туда помещаем данные из
нашего json-файла.

После этого проверяем наличие файла `Procfile` в репозитории. Он должен содержать две строки:
```
vk-bot: python3 vk_bot.py
tg-bot: python3 tg_bot.py
```

После этого выполняем деплой проекта из github, на вкладке `Resources` включаем `Dynos` и всё.

Если все настроено правильно, то в чат с модератором (который указывали в переменной `LOG_CHAT_ID`)
придут 2 уведомления, что боты запущены.

## Обучение DialogFlow новым вопросам и ответам
Для обучения новым вопросам создан скрипт `intents_loader.py`.
Данный скрипт взаимодействует с API DialogFlow и на вход принимает
название файла с данными для обучения.

К примеру :
```commandline
python intents_loader.py questions.json
```

Важно, чтобы данные для обучения были в формате json.
Пример того, как должен выглядеть json:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Как работать у вас?",
      "Хочу работать у вас",
      "Возможно-ли устроиться к вам?",
      "Можно-ли мне поработать у вас?",
      "Хочу работать редактором у вас"
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
  }
}
```

Давайте разберем что к чему:
1. `Устройство на работу` - название топика\интента, который будет создан;
2. `questions` - массив вопросов, на которых будет происходить обучение;
3. `answer` - ответ, который должен давать DialogFlow.

## Цель проекта
Код написан в учебных целях в рамках модуля Чат-боты проекта [Devman](https://dvmn.org/).


