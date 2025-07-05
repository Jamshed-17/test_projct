import csv
import argparse
from tabulate import tabulate


def main():
    # Создаём список с аргументами скрипта
    options = [
        ["--file", "-f", "Добавьте путь к CSV файлу", True],
        ["--where", "-w", "Добавьте условие вывода (например, 'price>500')", False],
        ["--aggregate", "-a", "Добавьте условия для агрегации (например, 'avg=price')", False]
    ]

    # Создаём объект с аргументами
    parser = argparse.ArgumentParser(description='CSV file worker')
    # Добавляем аргументы по одному из списка
    for option in options:
        parser.add_argument(
            option[1], 
            option[0], 
            type=str, 
            help=option[2], 
            required=option[3])

    args = parser.parse_args()

    # Чтение CSV файла
    with open(args.file, encoding='utf-8') as r_file:
        reader = csv.DictReader(r_file)
        data = list(reader)

    # Обработка фильтрации
    if args.where:
        operators = ["=", ">", "<"]
        operand_point = -1
        used_operator = None
        
        # Находим оператор в условии
        for op in operators:
            pos = args.where.find(op)
            if pos > operand_point:
                operand_point = pos
                used_operator = op
        
        if operand_point == -1:
            print("Ошибка: Неверный оператор в условии. Используйте =, > или <")
            return

        column = args.where[:operand_point]
        value = args.where[operand_point+len(used_operator):]

        filtered_data = []
        for row in data:
            try:
                # Пробуем сравнить как числа
                row_val = float(row[column]) if '.' in row[column] else int(row[column])
                filter_val = float(value) if '.' in value else int(value)
            except ValueError:
                # Если не числа, сравниваем как строки
                row_val = row[column]
                filter_val = value

            if used_operator == "=" and row_val == filter_val:
                filtered_data.append(row)
            elif used_operator == ">" and row_val > filter_val:
                filtered_data.append(row)
            elif used_operator == "<" and row_val < filter_val:
                filtered_data.append(row)
        
        data = filtered_data

    # Обработка агрегации
    if args.aggregate:
        try:
            agg_type, column = args.aggregate.split("=")
            agg_type = agg_type.lower().strip()
            column = column.strip()

            # Получаем числовые значения для агрегации
            values = []
            for row in data:
                try:
                    val = float(row[column]) if '.' in row[column] else int(row[column])
                    values.append(val)
                except ValueError:
                    print(f"Ошибка: Невозможно агрегировать нечисловую колонку '{column}'")
                    return

            if not values:
                print("Нет данных для агрегации")
                return

            # Вычисляем агрегацию
            if agg_type == "avg":
                result = sum(values) / len(values)
            elif agg_type == "min":
                result = min(values)
            elif agg_type == "max":
                result = max(values)
            else:
                print(f"Ошибка: Неизвестный тип агрегации '{agg_type}'. Используйте avg, min или max")
                return

            # Выводим результат
            print(tabulate(
                [[agg_type, column, result]],
                headers=["Aggregation", "Column", "Value"],
                tablefmt="grid"
            ))
            return

        except ValueError:
            print("Ошибка: Неверный формат агрегации. Используйте 'тип=колонка', например 'avg=price'")
            return

    # Вывод данных (если не было агрегации)
    if data:
        print(tabulate(data, headers="keys", tablefmt="grid"))
    else:
        print("Нет данных, соответствующих условиям")


if __name__ == "__main__":
    main()