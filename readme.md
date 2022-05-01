Судоку - невероятно популярная во всем мире головоломка.
Самые преданные фанаты покупают специальные сборники с головоломками различной сложности.
Несложные судоку регулярно публикуются во многих газетах и журналах.

Данный проект является программой для генерации и решения головоломок Судоку.
Для пользователя генерируется уникальная головоломка, которая имеет единственное решение.
Пользователь может выбрать один из 10 уровней сложности.
Чем выше уровень сложности, тем больше пустых клеток на "старте".
Уровни 9 и 10 способны "взорвать мозг" даже профессионалу. 
Данная программа умеет "решать" судоку с помощью рекурсивного перебора.
Однако данная возможность недоступна пользователям, т.к. она разработана только для генерации корректных судоку.

При генерации судоку сначала генерируется квадрат 9 на 9, удовлетворяющий требованиям судоку. 
Таким образом, генерируется решение головоломки.
Далее поочередно "удаляются" случайные цифры. Чем выше уровень, тем больше цифр будет удалено.
После каждого удаления происходит проверка, имеет ли текущая головоломка только одно решение.

Реализованы возможности сохранения игры в файл и загрузки игры из файла.
Таким образом, пользователь может в любой момент сделать паузу и вернуться к головоломке спустя некоторое время.
В файле хранится стартовая головоломка и все заполненные пользователем цифры.
Возможность жульничества (внесения некорректных правок в файлы) исключена.
При загрузке из файла программа проверяет, что "стартовое" поле имеет единственное решение.

Все файлы данного проекта должны находиться в одной папке.
Для успешного запуска проекта необходимо установить лишь "PyQt5".
Рекомендуется работать с проектом в PyCharm, т.к. именно в этой IDE он разрабатывался.
Необходимо создать новый проект и поместить все файлы, находящиеся в этом архиве, в папку проекта.
Файлы "game01.txt" ... "game07.txt" в архиве для примера для тестирования загрузки игры из файла.
Само собой, можно выбрать опцию "Новая игра", заполнить несколько ячеек и сохранить игру в другой файл.

Для запуска проекта необходимо запустить файл "MainWindow.py".

Общий объем программного кода составляет 479 строк.
Код разбит на два файла по следующему принципу:

1. "Field.py" - 220 строк кода
Файл содержит два класса - Field и FieldsGenerator.
Реализовано хранение текущего состояния поля, генерация головоломок различных уровней сложности.
Реализована проверка, имеет ли головоломка единственное решение или же решений два и больше.
Реализовано сохранение прогресса пользователя в текстовый файл и загрузка игры из текстового файла.
При загрузке из файла производится проверка, корректная ли игра сохранена в этом файле.   

2. "MainWindow.py" - 259 строк кода
Графическое оформление для удобства пользователя.
Все кнопки реагируют на движение мыши изменением своего цвета. 
Недоступные для изменения цифры выделены отдельным цветом и не являются кликабельными.
Реализовано всплывающее окно для выбора цифры или очистки ячейки.
Также реализованы всплывающие окна с информационными сообщениями:
Успешное решение судоку, успешная загрузка из файла, успешное сохранение, ошибка загрузки, ошибка сохранения.