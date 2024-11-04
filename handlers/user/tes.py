import json


def transform_input(input_string):
    # Преобразуем строку в объект Python
    print(type(input_string))
    try:
        data = json.loads(input_string)

    except json.JSONDecodeError:
        raise ValueError("Некорректный формат JSON")

    # Проверяем, является ли data списком
    if isinstance(data, list):
        # Если список содержит более одного элемента
        if len(data) > 1:
            return data  # Возвращаем как есть
        else:
            return [data[0]]  # Возвращаем как список с одним элементом
    else:
        raise ValueError("Ожидался список объектов JSON")




result1 = transform_input(input_string1)

print(result1)
print(type(result1))
