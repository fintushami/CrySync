# CrySync
CrySync - приложение для облачной сихронизации и использованием оконечного шифрования.
[![N|Solid](https://www.python.org/static/community_logos/python-powered-w-140x56.png)](https://www.python.org/)
# Характеристики
  - Сквозное шифрование для пользовательских данных. Никто, кроме обладателя секрета не имеет представления о структуре данных.
  - Шифрование с применением GOST R 34.12-2015 128-bit (Kuznechik) ([RFC 7801](https://tools.ietf.org/html/rfc7801))
  - Использование транспорта [ZMQ](http://zeromq.org/)
  - Возможность работы, как в режиме клиент-сервер, так и в режиме одноранговой сети (в разработке)
  - ...

# Установка

```sh
$ pip install crysync
```
Для запуска сервера используйте:
```sh
$ crysync serve
```
Для запуска клиента:
```sh
$ crysync use
```
**README UNDER MAITENANCE**
