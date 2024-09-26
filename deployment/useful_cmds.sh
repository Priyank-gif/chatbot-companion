#!/bin/bash

# view the scripts of the instance initiation (performed via user data)
tail -111f /var/log/cloud-init-output.log

tail -111f /var/log/nginx/access.log

cat /etc/nginx/sites-available/chatbot-companion

sudo nginx -s reload

ss -tuln | grep :8000

ps aux | grep python

sudo kill -9 port
