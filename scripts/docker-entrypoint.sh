#!/bin/bash

# Устанавливаем переменные окружения для cron
printenv | grep -v "no_proxy" >> /etc/environment

# Запускаем cron в фоновом режиме
cron

# Запускаем бота в основном режиме
echo "Starting bot..."
exec python -m app.bot
