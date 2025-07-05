import pytest
import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main
from io import StringIO


# Фикстура для тестовых данных
@pytest.fixture
def sample_csv(tmp_path):
    data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""
    file_path = tmp_path / "sample.csv"
    file_path.write_text(data)
    return str(file_path)

# Фикстура для пустого файла
@pytest.fixture
def empty_csv(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("name,brand\n")
    return str(file_path)

# Тест чтения CSV
def test_read_csv(sample_csv):
    with open(sample_csv, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        assert len(data) == 4
        assert data[0]['name'] == 'iphone 15 pro'

# Тест фильтрации (числовые значения)
def test_filter_numeric(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-w', 'price>500']
    main()
    captured = capsys.readouterr()
    assert 'iphone 15 pro' in captured.out
    assert 'galaxy s23 ultra' in captured.out
    assert 'redmi note 12' not in captured.out

# Тест фильтрации (строковые значения)
def test_filter_string(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-w', 'brand=xiaomi']
    main()
    captured = capsys.readouterr()
    assert 'xiaomi' in captured.out
    assert 'apple' not in captured.out

# Тест агрегации avg
def test_aggregate_avg(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-a', 'avg=price']
    main()
    captured = capsys.readouterr()
    assert '674' in captured.out  # Изменили на проверку целого числа

# Тест агрегации min
def test_aggregate_min(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-a', 'min=price']
    main()
    captured = capsys.readouterr()
    assert '199' in captured.out

# Тест агрегации max
def test_aggregate_max(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-a', 'max=price']
    main()
    captured = capsys.readouterr()
    assert '1199' in captured.out

# Тест пустого файла
def test_empty_file(empty_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', empty_csv]
    main()
    captured = capsys.readouterr()
    assert 'Нет данных' in captured.out

# Тест ошибки при агрегации нечисловой колонки
def test_aggregate_non_numeric(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-a', 'avg=name']
    main()
    captured = capsys.readouterr()
    assert 'Невозможно агрегировать' in captured.out

# Тест ошибки при неверном операторе
def test_invalid_operator(sample_csv, capsys):
    sys.argv = ['csv_processor.py', '-f', sample_csv, '-w', 'price?100']
    main()
    captured = capsys.readouterr()
    assert 'Неверный оператор' in captured.out