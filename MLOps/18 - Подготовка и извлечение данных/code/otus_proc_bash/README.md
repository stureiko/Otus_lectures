# Материалы к занятию «Подготовка и обогащение данных»

## Пререквизиты

### Утилита YC

[Конфигурация](https://yandex.cloud/ru/docs/cli/operations/profile/profile-create) утилиты `yc`;

> Note: Идентификатор каталога можно найти в графическом интерфейсе YC.

### Ключевая пара для ssh

Выполните интерактивную команду:

```bash
ssh-keygen -t ed25519
```

> Note: Назовите ключ `yc`. В противном случае измените переменную `SSH_PUBLIC_KEY_PATH` в файле `env.sh` и используйте свой путь к ключу в соответствующих командах.

### Имя пользователя

Установите переменную `YC_USER` в файле `env.sh` в имя вашего пользователя.

### Данные для занятия

Данные [скачиваем тут](https://www.kaggle.com/competitions/riiid-test-answer-prediction/data) – чтобы скачать, нужно присоединиться к соревнованию, нажать `Late Submission`. Файлы `train.csv`, `lectures.csv` и `question.csv` положите в папку `data`.

### Имя пользователя

Установите в переменную

## Что делаем на занятии

### Создаем бакет в Object Storage

```bash
bash create_bucket.sh
```

### Создаем сервисный аккаунт

```bash
bash create_service_account.sh
```

Идентфиикатор секретного ключа и сам секретный ключ осядут в файле `sa-key.json`. __Никому их не показывайте!__

### Конфигурируем s3cmd

[Установите](https://github.com/s3tools/s3cmd/blob/master/INSTALL.md) утилиту.

Далее просто запустите:

```bash
bash setup_s3cmd.sh
```

Команда создат файл конфигурации `~/.s3cmd`, куда запишет все необходимые параметры, важнейшими среди которых являются ваши идентификатор секретного ключа и сам секретный ключ, которые команда возьмет из файла `sa-key.json`. Чтобы проверить, что все работает выполните:

```bash
s3cmd ls s3://otus-dataproc-b42
```

> Note: Если нтересны другие способы настройки, читайте [тут](https://yandex.cloud/ru/docs/storage/tools/s3cmd).

### Скопируйте данные в облачный бакет

```bash
# Выполнится быстро
bash upload_data_to_bucket.sh data/lectures.csv

# Выполнится быстро
bash upload_data_to_bucket.sh data/questions.csv 

# Займет продолжительное время
bash upload_data_to_bucket.sh data/train.csv
```

### Создаем сеть, подсеть, шлюз, таблицу маршрутизации и группу безопасности

```bash
bash create_vpc.sh
```

### Создаем spark-кластер (DataProc)

```bash
bash create_dataproc_cluster.sh
```

### Создаем [Jump Server](https://en.wikipedia.org/wiki/Jump_server), чтобы попадать в кластер из вне

Выполните:

```bash
cp metadata.yaml.example metadata.yaml
```

Откройте файл `metadata.yaml` и в ппараметр `ssh-authorized-keys` запишите строку с вашим публичным ключом.

> Note: указывайте не путь, а именно сам ключ (то, что выводит команда `cat ~/.ssh/yc.pub`).

Выполните:

```bash
bash create_virtual_machine.sh jumpserver
```

В числе прочего команда напечатает публичный IP свежей VM. Затем выполните:

```bash
scp -i $HOME/.ssh/yc $HOME/.ssh/yc {публичный-IP-вашей-ВМ}:.ssh/yc
```

Эта команда скопирует ваш приватный ключ на виртуальную машину, и вы сможете попадать с нее на мастер-ноду spark-кластера.

### Попадаем на мастер ноду кластера

Попадаем на Jump Server:

Выполните

```bash
bash get_masternode_fqdn.sh
```

Команда выведет [Полное доменное имя (fqdn)](https://yandex.cloud/ru/docs/glossary/fqdn) мастер-ноды вашего кластера.

Выполните:

```bash
ssh -i ~/.ssh/yc {публичный-IP-вашей-ВМ}
```

Изнутри виртуальной машины выполните:

```bash
ssh -i ~/.ssh/yc ubuntu@{fqdn-мастер-ноды}
```

На мастер ноде выполните:

```bash
# Создаем папку на HDFS
hdfs dfs -mkdir -p /user/ubuntu/data

# Копируем наши данные из бакета в эту HDFS-папку
hadoop distcp s3a://otus-dataproc-b42/ /user/ubuntu/data

# Смотрим, какие файлы появились
hdfs dfs -ls /user/ubuntu/data
```

### Копируем ноутбуки на мастер-ноду

```bash
# Сперва на jump-сервер
scp -i ~/.ssh/yc notebooks/*.ipynb {публичный-IP-вашей-ВМ}:

# Потом идем на jump-сервер
ssh -i ~/.ssh/yc {публичный-IP-вашей-ВМ}

# И копируем файлы на мастер-ноду
scp -i ~/.ssh/yc *.ipynb ubuntu@{fqdn-мастер-ноды}:
```

### Попадаем через Jupyter

```bash
# Проброс порта с вашей машины на Jump Server
ssh -i ~/.ssh/yc -L 8888:localhost:8888 {публичный-IP-вашей-ВМ}

# Проброс порта с Jump Server на мастер-ноду
ssh -i .ssh/yc -L 8888:localhost:8888 ubuntu@{fqdn-мастер-ноды}

# Запуск Jupyter
jupyter notebook
```
