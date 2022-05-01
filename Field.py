from random import shuffle

numbers_in_cells = {1: 70, 2: 65, 3: 60, 4: 55, 5: 50, 6: 45, 7: 40, 8: 35, 9: 30, 10: 25}


class Field:
    def __init__(self):
        self.start_field = []
        self.field = []
        self.answer = []
        self.hard_level = None
        for i in range(9):
            self.start_field.append([None] * 9)
            self.field.append([None] * 9)
            self.answer.append([None] * 9)

    @staticmethod
    def field_to_str(field):
        result = []
        for i in range(9):
            block = list()
            block.append(' '.join([str(x) for x in field[i][:3]]))
            block.append(' '.join([str(x) for x in field[i][3:6]]))
            block.append(' '.join([str(x) for x in field[i][6:]]))
            line = ' | '.join(block)
            line = line.replace('None', ' ')
            result.append(line)
            if i == 2 or i == 5:
                result.append("-" * 21)
        return '\n'.join(result)

    def __str__(self, start=False, answer=False):
        result = "Field:\n" + self.field_to_str(self.field)
        if start:
            result += "\n\nStart field:\n" + self.field_to_str(self.start_field)
        if answer:
            result += "\n\nAnswer:\n" + self.field_to_str(self.answer)
        return result

    @staticmethod
    def get_boarders(x):
        if x <= 2:
            return [0, 1, 2]
        elif x <= 5:
            return [3, 4, 5]
        else:
            return [6, 7, 8]

    def get_bad_numbers(self, x, y):
        bad_numbers = set()
        for i in range(9):
            if self.field[x][i] is not None:
                bad_numbers.add(self.field[x][i])
            if self.field[i][y] is not None:
                bad_numbers.add(self.field[i][y])
        row = self.get_boarders(x)
        col = self.get_boarders(y)
        for r in row:
            for c in col:
                if self.field[r][c] is not None:
                    bad_numbers.add(self.field[r][c])
        bad_numbers = list(bad_numbers)
        bad_numbers.sort()
        return bad_numbers

    def get_good_numbers(self, x, y):
        bad_numbers = self.get_bad_numbers(x, y)
        good_numbers = []
        for i in range(1, 10):
            if i not in bad_numbers:
                good_numbers.append(i)
        return good_numbers

    @staticmethod
    def copy(field):
        field_copy = []
        for i in range(len(field)):
            field_copy.append(field[i].copy())
        return field_copy

    def find_answers(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j] is None:
                    number_of_answers = 0
                    good_numbers = self.get_good_numbers(i, j)
                    shuffle(good_numbers)
                    for gn in good_numbers:
                        self.field[i][j] = gn
                        answers = self.find_answers()
                        self.field[i][j] = None
                        if answers == 2:
                            return 2
                        if answers == 1:
                            if number_of_answers == 1:
                                return 2
                            number_of_answers = 1
                    return number_of_answers
        self.answer = self.copy(self.field)
        return 1

    def save_game(self, file_name):
        string_start_field = ""
        string_field = ""
        for i in range(9):
            for j in range(9):
                if self.start_field[i][j] is None:
                    string_start_field += "0"
                else:
                    string_start_field += str(self.start_field[i][j])
                if self.field[i][j] is None:
                    string_field += "0"
                else:
                    string_field += str(self.field[i][j])
            string_start_field += "\n"
            string_field += "\n"
        file = open(file_name, mode="w")
        sep = "=" * 9
        file.write(string_start_field + sep + "\n" + string_field)
        file.close()

    def check_game(self):
        for i in range(9):
            for j in range(9):
                if self.start_field[i][j] is not None:
                    if self.field[i][j] != self.start_field[i][j]:
                        return False
        field_copy = self.copy(self.field)
        self.field = self.copy(self.start_field)
        correct_game = True
        for i in range(9):
            for j in range(9):
                if self.field[i][j] is not None:
                    number = self.field[i][j]
                    self.field[i][j] = None
                    if number not in self.get_good_numbers(i, j):
                        correct_game = False
                    self.field[i][j] = number
        if correct_game:
            if self.find_answers() != 1:
                correct_game = False
        self.field = self.copy(field_copy)
        return correct_game

    def open_game(self, file_name):
        file = open(file_name, mode="r")
        s = file.readlines()
        file.close()
        try:
            strings_start_field = s[:9]
            strings_field = s[10:]
            cells_with_number = 0
            for i in range(9):
                for j in range(9):
                    if strings_start_field[i][j] == "0":
                        self.start_field[i][j] = None
                    else:
                        self.start_field[i][j] = int(strings_start_field[i][j])
                        cells_with_number += 1
                    if strings_field[i][j] == "0":
                        self.field[i][j] = None
                    else:
                        self.field[i][j] = int(strings_field[i][j])
            for i in range(10, 0, -1):
                if cells_with_number <= numbers_in_cells[i]:
                    self.hard_level = i
                    break
            if self.hard_level is None:
                return False
            return self.check_game()
        except Exception:
            return False

    def is_game_over(self):
        result = True
        for i in range(9):
            for j in range(9):
                if self.field[i][j] != self.answer[i][j]:
                    result = False
        return result


class FieldsGenerator(Field):
    def __init__(self, hard_level):
        super().__init__()
        self.generate()
        self.hard_level = hard_level
        for i in range(9):
            for j in range(9):
                self.answer[i][j] = self.field[i][j]
        self.erase_numbers(81 - numbers_in_cells[hard_level])
        for i in range(9):
            for j in range(9):
                self.start_field[i][j] = self.field[i][j]

    def generate(self):
        line0 = list(range(1, 10))
        shuffle(line0)
        self.field[0] = line0
        self.find_answers()
        self.field = self.copy(self.answer)

    def erase_numbers(self, count):
        positions = list(range(81))
        shuffle(positions)
        can_erase_number = True
        number_of_erases = 0
        while can_erase_number and number_of_erases < count:
            can_erase_number = False
            for i in range(len(positions)):
                p = positions[i]
                current_number = self.field[p // 9][p % 9]
                self.field[p // 9][p % 9] = None
                if self.find_answers() == 1:
                    can_erase_number = True
                    number_of_erases += 1
                    positions = positions[i + 1:]
                    break
                self.field[p // 9][p % 9] = current_number
