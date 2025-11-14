import copy

# Заданные значения и закрепленные ячейки
values = {
    'E': 7, 'H': 6, 'I': 9, 'Q': 3, 'R': 4, 'S': 2, 'U': 8, 'V': 1, 'X': 5
}
fixed_cells = ['E', 'H', 'I', 'Q', 'R', 'S', 'U', 'V', 'X']

# Макет 2D
layout = [
    [None, None, None, 'A', 'B', 'C', None, None, None],
    [None, None, None, 'D', 'F', 'G', None, None, None],
    [None, None, None, 'E', 'H', 'I', None, None, None],
    ['A', 'D', 'E', 'E', 'H', 'I', 'I', 'G', 'C'],
    ['L', 'W', 'U', 'U', 'X', 'V', 'V', 'Y', 'M'],
    ['K', 'P', 'Q', 'Q', 'R', 'S', 'S', 'T', 'N'],
    [None, None, None, 'Q', 'R', 'S', None, None, None],
    [None, None, None, 'P', 'Z', 'T', None, None, None],
    [None, None, None, 'K', 'O', 'N', None, None, None],
    [None, None, None, 'K', 'O', 'N', None, None, None],
    [None, None, None, 'L', 'J', 'M', None, None, None],
    [None, None, None, 'A', 'B', 'C', None, None, None],
]

# Срезы
slices = {
    'slice1': ['D', 'F', 'G', 'W', '!', 'Y', 'P', 'Z', 'T'],
    'slice2': ['U', 'X', 'V', 'W', '!', 'Y', 'L', 'J', 'M'],
    'slice3': ['H', 'X', 'R', 'F', '!', 'Z', 'B', 'J', 'O'],
}

# Структура 3D куба
cube3D_structure = {
    'front': [['E', 'H', 'I'], ['U', 'X', 'V'], ['Q', 'R', 'S']],
    'right': [['I', 'G', 'C'], ['V', 'Y', 'M'], ['S', 'T', 'N']],
    'back': [['C', 'B', 'A'], ['M', 'J', 'L'], ['N', 'O', 'K']],
    'left': [['A', 'D', 'E'], ['L', 'W', 'U'], ['K', 'P', 'Q']],
    'top': [['A', 'B', 'C'], ['D', 'F', 'G'], ['E', 'H', 'I']],
    'bottom': [['Q', 'R', 'S'], ['P', 'Z', 'T'], ['K', 'O', 'N']]
}

# Определяем блоки 2D
blocks_2d = [
    {'id': 'top', 'coords': {'rows': [1, 2, 3], 'cols': [4, 5, 6]}},
    {'id': 'left', 'coords': {'rows': [4, 5, 6], 'cols': [1, 2, 3]}},
    {'id': 'front', 'coords': {'rows': [4, 5, 6], 'cols': [4, 5, 6]}},
    {'id': 'right', 'coords': {'rows': [4, 5, 6], 'cols': [7, 8, 9]}},
    {'id': 'bottom', 'coords': {'rows': [7, 8, 9], 'cols': [4, 5, 6]}},
    {'id': 'back', 'coords': {'rows': [10, 11, 12], 'cols': [4, 5, 6]}},
    {'id': 'slice1', 'coords': {'slice': 'slice1'}},
    {'id': 'slice2', 'coords': {'slice': 'slice2'}},
    {'id': 'slice3', 'coords': {'slice': 'slice3'}}
]

# Создаем словарь для хранения значений ячеек
cell_data = {}
for y, row in enumerate(layout):
    for x, letter in enumerate(row):
        if letter and letter not in cell_data:
            cell_data[letter] = {'value': values.get(letter, 0), 'is_fixed': letter in fixed_cells}

for slice_name, cells in slices.items():
    for letter in cells:
        if letter and letter not in cell_data:
            cell_data[letter] = {'value': values.get(letter, 0), 'is_fixed': letter in fixed_cells}

for face, rows in cube3D_structure.items():
    for row in rows:
        for letter in row:
            if letter and letter not in cell_data:
                cell_data[letter] = {'value': values.get(letter, 0), 'is_fixed': letter in fixed_cells}

# Проверка начальных конфликтов
def check_initial_conflicts():
    conflicts = []
    for letter in fixed_cells:
        value = values[letter]
        blocks = get_blocks_for_letter(letter)
        for block in blocks:
            if block in ['top', 'left', 'front', 'right', 'bottom', 'back']:
                for row in blocks_2d[[b['id'] for b in blocks_2d].index(block)]['coords']['rows']:
                    for col in blocks_2d[[b['id'] for b in blocks_2d].index(block)]['coords']['cols']:
                        other_letter = layout[row-1][col-1]
                        if other_letter and other_letter != letter and other_letter in fixed_cells and values.get(other_letter) == value:
                            conflicts.append(f"Конфликт в блоке {block}: буквы {letter} и {other_letter} имеют значение {value}")
            elif block in ['slice1', 'slice2', 'slice3']:
                for other_letter in slices[block]:
                    if other_letter != letter and other_letter in fixed_cells and values.get(other_letter) == value:
                        conflicts.append(f"Конфликт в срезе {block}: буквы {letter} и {other_letter} имеют значение {value}")
            elif block in cube3D_structure:
                for row in cube3D_structure[block]:
                    for other_letter in row:
                        if other_letter != letter and other_letter in fixed_cells and values.get(other_letter) == value:
                            conflicts.append(f"Конфликт на грани {block}: буквы {letter} и {other_letter} имеют значение {value}")
    return conflicts

# Определяем блоки для проверки ограничений
def get_blocks_for_letter(letter):
    blocks = []
    for block in blocks_2d:
        if 'slice' in block['coords']:
            if letter in slices[block['coords']['slice']]:
                blocks.append(block['id'])
        else:
            for row in block['coords']['rows']:
                for col in block['coords']['cols']:
                    if layout[row-1][col-1] == letter:
                        blocks.append(block['id'])
                        break
    for face, rows in cube3D_structure.items():
        for row in rows:
            if letter in row:
                blocks.append(face)
                break
    return blocks

# Проверка, можно ли поставить число в ячейку
def can_place(letter, value, current_values):
    if current_values[letter]['is_fixed']:
        return current_values[letter]['value'] == value
    blocks = get_blocks_for_letter(letter)
    for block in blocks:
        if block in ['top', 'left', 'front', 'right', 'bottom', 'back']:
            for row in blocks_2d[[b['id'] for b in blocks_2d].index(block)]['coords']['rows']:
                for col in blocks_2d[[b['id'] for b in blocks_2d].index(block)]['coords']['cols']:
                    other_letter = layout[row-1][col-1]
                    if other_letter and other_letter != letter and current_values.get(other_letter, {}).get('value') == value:
                        return False
        elif block in ['slice1', 'slice2', 'slice3']:
            for other_letter in slices[block]:
                if other_letter != letter and current_values.get(other_letter, {}).get('value') == value:
                    return False
        elif block in cube3D_structure:
            for row in cube3D_structure[block]:
                for other_letter in row:
                    if other_letter != letter and current_values.get(other_letter, {}).get('value') == value:
                        return False
    return True

# Рекурсивная функция для подсчета и сохранения решений
def count_solutions(current_values, letters, index, solution_count, solutions, variant_count):
    if index >= len(letters):
        solution_count[0] += 1
        # Сохраняем текущее решение
        solution = {letter: current_values[letter]['value'] for letter in letters}
        solutions.append(solution)
        print(f"Найдено решений: {solution_count[0]}")
        return

    letter = letters[index]
    if current_values[letter]['is_fixed']:
        count_solutions(current_values, letters, index + 1, solution_count, solutions, variant_count)
        return

    for value in range(1, 10):
        variant_count[0] += 1  # Увеличиваем счетчик вариантов
        if can_place(letter, value, current_values):
            current_values[letter]['value'] = value
            count_solutions(current_values, letters, index + 1, solution_count, solutions, variant_count)
            current_values[letter]['value'] = 0

# Основная функция
def solve_sudoku():
    # Проверка начальных конфликтов
    conflicts = check_initial_conflicts()
    if conflicts:
        print("Найдены конфликты в начальных данных:")
        for conflict in conflicts:
            print(conflict)
        print("Решений не существует из-за конфликтов.")
        return 0

    # Список всех букв
    letters = sorted(list(set([letter for row in layout for letter in row if letter] +
                             [letter for slice in slices.values() for letter in slice] +
                             [letter for face in cube3D_structure.values() for row in face for letter in row])))
    
    # Подсчет решений
    solution_count = [0]
    variant_count = [0]  # Счетчик проверенных вариантов
    solutions = []
    print("Поиск решений начат...")
    count_solutions(copy.deepcopy(cell_data), letters, 0, solution_count, solutions, variant_count)
    print(f"Поиск завершен. Всего найдено решений: {solution_count[0]}")
    print(f"Всего проверено вариантов: {variant_count[0]}")
    
    # Вывод всех решений
    if solutions:
        print("\nНайденные решения:")
        for i, solution in enumerate(solutions, 1):
            print(f"Решение {i}:")
            solution_str = ", ".join(f"{letter}: {value}" for letter, value in sorted(solution.items()))
            print(solution_str)
    
    return solution_count[0]

# Запуск
if __name__ == "__main__":
    solve_sudoku()