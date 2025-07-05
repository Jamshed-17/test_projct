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
![[Pasted image 20250705182714.png]]


Средний рейтинг:
```python3 main.py -f data.csv -a "avg=rating"```
![[Pasted image 20250705182730.png]]


Максимальная цена у Xiaomi:
```python3 main.py -f data.csv -w "brand=xiaomi" -a "max=price"```
![[Pasted image 20250705182740.png]]

## Тестирование
Запуск тестов:
```pytest tests/```

Проверка покрытия:
```pytest --cov=. tests/```