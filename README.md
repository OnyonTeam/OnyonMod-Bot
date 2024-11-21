**Единая Система Банов (ЕСБ): автоматизация блокировок**

ЕСБ — это бот для блокировки пользователей на нескольких серверах одновременно. Система создана, чтобы облегчить жизнь модераторов, помогая бороться с неадекватами, спамерами и пиарщиками.

**Как это работает?**

При использовании команды /oban запрос на блокировку отправляется всем серверам, подключённым к ЕСБ. Это позволяет мгновенно блокировать нарушителя на нескольких платформах.

**Команды бота:**

``/oban user:(имя пользователя) reason:(причина) image:(скриншот, если есть)`` - отправить запрос на бан (и забанить у себя на сервере)
``/autoban`` - автосоглашаться на запрос с другого сервера
``/obanlist`` - список забаненых в системе
 команды **доступные только администрации бота** нужны в основном для разработки, но если надо:
``/reload`` - перезагрузить 
``/addserver`` - добавить сервер в учет
``/removeserver`` - убрать сервре из учета
``/setstatus`` - установить статус

**Почему это важно?**

Система банов уже активно используется на западных технических серверах (точнее, в редстоун сообществе), где спам стал проблемой. ЕСБ — это улучшенная версия таких решений для русских дискорд серверов, особенно для хостингов.
