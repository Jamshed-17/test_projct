## Для установки

1. ```git clone https://github.com/Jamshed-17/test_projct.git```
2. Поставить виртуальное окружение
3. ```pip install -r requirements.txt```

## Для запуска
1. ```python3 main.py -f <файл.csv> [--where <условие>] [--aggregate <агрегация>]```

### Параметры:

| Флаг | Полная версия | Описание                         |
| ---- | ------------- | -------------------------------- |
| -f   | --file        | Путь к CSV файлу (обязательный)  |
| -w   | --where       | Условие фильтрации (опционально) |
| -a   | --aggregate   | Агрегация данных (опционально)   |


### Примеры команд:
Фильтрация по цене (>500):
```python3 main.py -f data.csv -w "price>500"```
![1](https://iimg.su/i/vprSj1)

Средний рейтинг:
```python3 main.py -f data.csv -a "avg=rating"```
![2](https://iimg.su/i/nOlINq)

Максимальная цена у Xiaomi:
```python3 main.py -f data.csv -w "brand=xiaomi" -a "max=price"```
![3](https://iimg.su/i/E4rXvQ)

## Тестирование
Запуск тестов:
```pytest tests/```

Проверка покрытия:
```pytest --cov=. tests/```