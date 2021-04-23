FROM python:3.7.2-alpine3.8
# Устанавливаем зависимости
ENV database = "database/db.db"/
client_id = "9ff8f300ec3d64d48796"/
client_secret = "9e023423bc80ab40892da67823c24463487e7293"/
secret_key = "QWRWLIWDTDBDEFJACZEBYQEBQPUPZVVHUNSN"
RUN pip RUN requirements.txt
# Задаём текущую рабочую директорию
WORKDIR /usr/src/gitwithme
# Копируем код из локального контекста в рабочую директорию образа
COPY . ./
# Настраиваем команду, которая должна быть запущена в контейнере во время его выполнения
ENTRYPOINT ["python", "run.py"]
# Открываем порты
EXPOSE 8000
# Создаём том для хранения данных
VOLUME /my_volume
