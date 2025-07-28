# публичный доступ к Jupyter серверу

Чтобы разрешить публичный доступ к Jupyter серверу, нужно изменить настройки его конфигурации. Вот пошаговая инструкция:

## 🔧 1. Создай конфиг Jupyter (если еще не создан)

```bash
jupyter notebook --generate-config
```

Это создаст файл конфигурации по пути (у каждого пользователя путь может отличаться):

```bash
~/.jupyter/jupyter_notebook_config.py
```

## 🛠️ 2. Открой конфигурационный файл

```bash
vim ~/.jupyter/jupyter_notebook_config.py
```

И установи:

```python
c.NotebookApp.ip = '0.0.0.0'              # слушать все интерфейсы
c.NotebookApp.port = 8888                 # порт (или другой, по желанию)
c.NotebookApp.open_browser = False        # не открывать браузер при старте
c.NotebookApp.allow_root = True           # если запускается от root
```

Если не нужен пароль/токен (не рекомендуется для открытых машин!):

```python
c.NotebookApp.token = ''                  # отключить токен
c.NotebookApp.password = ''               # отключить пароль
```

## 🔒 3. Открой порт в firewall (если используется)

Пример для ufw:

```bash
sudo ufw allow 8888/tcp
```

Или в iptables:

```bash
sudo iptables -A INPUT -p tcp --dport 8888 -j ACCEPT
```

## 🌐 4. Запусти сервер

```bash
jupyter notebook --config=~/.jupyter/jupyter_notebook_config.py
```

Или:

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser
```

⚠️ Важно:

- 🔐 Не запускай публично сервер без пароля или токена, если нет reverse proxy с аутентификацией или VPN.
- Лучше использовать Jupyter за прокси-сервером (например, nginx с basic auth или через SSH-tunnel).
