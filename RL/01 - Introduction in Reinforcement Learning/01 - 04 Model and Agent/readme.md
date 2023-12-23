# Инструкция

Уважаемые студенты!

Для запуска настроенных сред Gymnasium нужен Docker.

Как узнать установлен ли Docker ?

| Команда            |Если установлен|Если не установлен| Как устновить                                     |
|--------------------|---|---|---------------------------------------------------|
| ```docker -v``` |Docker version хх.хх.хх, build ххххх|bash: docker: command not found| [ссылка](https://docs.docker.com/engine/install/) |
|```docker compose version```|Docker Compose version vx.xx.x|bash: docker: command not found|[ссылка](https://docs.docker.com/compose/install/)|

После установки Docker-a нужно из текущей директории запустить контейнер командой

```shell
docker compose up --build
```

После запуска контейнера можно перейти на основную страницу [веб-сервера](http://0.0.0.0:80)
