# Проект для летней практики-хакатона "Алгоритмы для логистики" в компании Garpix 
Алгоритм укладки коробок в контейнер по принципу конвейера

Исполняемым файлом является файл example.py
Для передачи информации используется первый аргумент при вызове скрипта ( python example.py src )
Путь необходимо указывать полностью, например: python3 example.py /var/tmp/hackathon/data1/113051_cl.json

В файле main.py хранятся классы и их методы, необходимые для работа алгоритма
В файле auxiliary_methods.py - вспомогительные методы для работы
В файле constants.py - константы


В плоскости XY предметы укладываются друг на друга, если они соответсвуют занимаемому пространству путем вращения предмета по любой из возможных осей. 
Коробка может быть поставлена ну другие ящики, если площадь поверхности соприкосновения коробки >=60% от площади ящиком под ней ( Для включения в файле main.py переменной area необходимо присвоить значение 0.6, в данный момент 0.1).

Алгоритм не кладет коробки в пустое пространство под другими коробками если слой уже заполнен
