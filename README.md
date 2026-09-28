# Internet Speed Test

## Сборка

```bash
docker build -t speedtest .
```

## Запуск

```bash
# По умолчанию: 100MB.bin от Hetzner, 10 запросов
docker run --rm speedtest

# Свой URL
docker run --rm speedtest https://images.pexels.com/photos/6224289/pexels-photo-6224289.jpeg?_gl=1*73zwni*_ga*MjEwNDMwOTkxMC4xNzkwNTk1Mjgy*_ga_8JE65Q40S6*czE3OTA1OTUyODIkbzEkZzEkdDE3OTA1OTUyODkkajUzJGwwJGgw

# Своё количество запросов
docker run --rm speedtest https://images.pexels.com/photos/6224289/pexels-photo-6224289.jpeg?_gl=1*73zwni*_ga*MjEwNDMwOTkxMC4xNzkwNTk1Mjgy*_ga_8JE65Q40S6*czE3OTA1OTUyODIkbzEkZzEkdDE3OTA1OTUyODkkajUzJGwwJGgw -n 5
```

## Без Docker

```bash
pyenv install 3.12.0 
pyenv virtualenv 3.12 speed-request
pyenv local speed-request
pip install -r requirements.txt
python speedtest.py https://images.pexels.com/photos/6224289/pexels-photo-6224289.jpeg?_gl=1*73zwni*_ga*MjEwNDMwOTkxMC4xNzkwNTk1Mjgy*_ga_8JE65Q40S6*czE3OTA1OTUyODIkbzEkZzEkdDE3OTA1OTUyODkkajUzJGwwJGgw -n 5
```