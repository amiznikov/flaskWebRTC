# flaskWebRTC

## Простой пример реализации RTSP-WebRTC, с помощью Flask, на базе [Kurento](https://www.kurento.org), Kurento-Media-Server

### Установка

1. Установка системных зависимостей
  - Для dev
  ```
  sudo apt-get install python3 python3-pip python3-dev python3-venv python3-setuptools build-essential libssl-dev libffi-dev
  ```
  - Для production
  ```
  sudo apt-get install python3 python3-pip python3-dev python3-venv python3-setuptools build-essential libssl-dev libffi-dev uwsgi uwsgi-plugin-python3 nginx
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

3. Разворачивание проекта flaskWebRTC

 - Для dev

```
 git clone git@github.com:4rtcrt/flaskWebRTC.git
 cd flaskWebRTC
 python3 -m venv pyenv
 source pyenv/bin/activate
 python3 -m pip install -r requirements.txt
 python3 app/app.py
 ```
- Для production

```
 git clone git@github.com:4rtcrt/flaskWebRTC.git
 cd flaskWebRTC
 python3 -m venv pyenv
 source pyenv/bin/activate
 export PRODUCTION=True
 python3 -m pip install -r requirements.txt
 python3 app/app.py
 ```

4. Различные команды
 - Остановка и запуска Kurento
```
 sudo service kurento-media-server stop
 sudo service kurento-media-server start
```
