# flaskWebRTC

## Простой пример реализации RTSP-WebRTC, с помощью Flask, на базе [Kurento](https://www.kurento.org), Kurento-Media-Server

### Установка

1. Установка системных зависимостей

  ```
  sudo apt-get install python3 python3-pip python3-dev python3-venv python3-setuptools python3-wheel build-essential libssl-dev libffi-dev
  ```

  ```
  curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
  sudo apt-get install -y nodejs
  sudo npm install -g bower
  ```

2. Установка Kurento

 - Установка GnuPG:
```
sudo apt-get update \
  && sudo apt-get install --no-install-recommends --yes \
     gnupg
```
 - Выбор версии Kurento (только одно на выбор):
```
  DISTRO="xenial"  # KMS for Ubuntu 16.04 (Xenial)
  DISTRO="bionic"  # KMS for Ubuntu 18.04 (Bionic)
```
- Добавление репозитория Kurento в систему:
```
 sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5AFA7A83
```
```
 sudo tee "/etc/apt/sources.list.d/kurento.list" >/dev/null <<EOF
# Kurento Media Server - Release packages
deb [arch=amd64] http://ubuntu.openvidu.io/6.10.0 $DISTRO kms6
EOF
```

- Установка Kurento:
```
sudo apt-get update \
  && sudo apt-get install --yes kurento-media-server
```

 - Остановка и запуска Kurento
```
 sudo service kurento-media-server stop
 sudo service kurento-media-server start
```

3. Разворачивание проекта flaskWebRTC

- Скачать проект:
 ```
 wget https://github.com/4rtcrt/flaskWebRTC/archive/master.zip
 unzip flaskWebRTC-master.zip
 rm flaskWebRTC-master.zip
 mv flaskWebRTC-master flaskwebrtc
 cd flaskwebrtc
 ```

- Python зависимости
 ```
 python3 -m venv pyenv
 source pyenv/bin/activate
 export PRODUCTION=True
 python3 -m pip install -r requirements.txt
 deactivate
 ```

- Kurento зависимости
 ```
 bower install
 ```
 или
  ```
 bower install --allow-root
 ```

4. Фикс ошибки

 ```
  rm app/static/bower_components/kurento-utils/js/kurento-utils.js
  cp fix/kurento-utils.js app/static/bower_components/kurento-utils/js/
 ```

5. Nginx
 - Сконфигурировать (то есть пересобрать nginx или поставить из исходников) nginx по конфигу лежащему в файле ```nginxhttp```
 - При этом в строчке ``` -fdebug-prefix-map=/build/nginx-0TiIP5/nginx-1.14.0= ``` заменить версию nginx на используемую вами
 - В процессе конфигурации могут быть ошибки в зависимости от того, какие системные библиотеки отсутствуют у вас для ngixn - поставить эти библиотеки и снова запускать конфигурацию nginx
 - Отредактировать файл flaskwebrtc.conf в соотвествие с вашем ip/доменом, и путями к данному проекту
 - Скопировать или линкануть этот файл в вашу дирректорию ```nginx/sites-enabled`` (или подключить любым другим удобным способом)
 - Дописать в файле ```nginx/nginx.conf``` в разделе ```http```  (или в любом другом месте где вы это делаете) следующее:
 
 ```
        keepalive_timeout ваше_значение;
        proxy_connect_timeout ваше_значение;
        proxy_send_timeout ваше_значение;
        proxy_read_timeout ваше_значение;

        map $http_upgrade $connection_upgrade {
            default upgrade;
            ''      close;
         }

        upstream 127.0.0.1:8888 {
        server ws:8888;
      }
 ```
 - Проверить правильность конфигов nginx:
  ``` nginx -t ```
  - Перезапустить nginx

6. Проверка перед запуском

 - Проверка работоспособности Kurento-Media-Server
 ```
 sudo service kurento-media-server status
 ```
 
 - Если по каким то причинам не активна:
 ```
 sudo service kurento-media-server stop
 sudo service kurento-media-server start
```

- Дополнительная проверка:
 ```
 curl -i -N \
    -H "Connection: Upgrade" \
    -H "Upgrade: websocket" \
    -H "Host: 127.0.0.1:8888" \
    -H "Origin: 127.0.0.1" \
    http://127.0.0.1:8888/kurento
 ```
 - Ответ должен быть примерно следующим:
 ```
  HTTP/1.1 500 Internal Server Error
  Server: WebSocket++/0.7.0
 ```
 
7. Запуск проекта
 - Запуск из точки входа:
```
source pyenv/bin/activate
cd app
gunicorn app:app
```
 - Запуск из systemcl
```
Пока что не написан но возможен
```

