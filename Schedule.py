class Schedule:
    def __init__(self, xml_list):
        self.groups = list()
        self.str_groups = list()
        for i in range(0, len(xml_list) - 4, 4):
            self.str_groups.append(xml_list[i][0])
            self.groups.append(GroupSchedule(xml_list[i:i + 4]))


class GroupSchedule:
    def __init__(self, xml_list):
        self.group = xml_list[0][0]
        self.week = list()
        for i in range(2, len(xml_list[0]), 14):
            self.week.append(DaySchedule(
                xml_list[0][i:i+14],
                xml_list[1][i:i+14],
                xml_list[2][i:i+14],
                xml_list[3][i:i+14]))

    def str(self, week_1: bool):
        temp = ''
        sp = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу']
        for i in range(6):
            if week_1:
                temp += 'Раписание на ' + sp[i] + ':\n' + self.week[i].str(week_1) + '\n'
            else:
                temp += 'Раписание на ' + sp[i] + ':\n' + self.week[i].str(week_1) + '\n'
        return temp


class DaySchedule:
    def __init__(self, discipline_names, discipline_types, discipline_teachers, discipline_cabs):
        self.lessons_1 = list()
        self.lessons_2 = list()

        for i in range(0, 13, 2):
            j = i + 1
            self.lessons_1.append(
                Lesson(
                    discipline_names[i],
                    discipline_types[i],
                    discipline_teachers[i],
                    discipline_cabs[i]))
            self.lessons_2.append(
                Lesson(
                    discipline_names[j],
                    discipline_types[j],
                    discipline_teachers[j],
                    discipline_cabs[j]))

    def str(self, week_1: bool):
        if week_1:
            temp = ''
            for i in range(6):
                if self.lessons_1[i].__str__() == '':
                    temp += str(i + 1) + ') ' + '-\n'
                else:
                    temp += str(i + 1) + ') ' + self.lessons_1[i].__str__() + '\n'
            return temp
        else:
            temp = ''
            for i in range(6):
                if self.lessons_2[i].__str__() == '':
                    temp += str(i + 1) + ') ' + '-\n'
                else:
                    temp += str(i + 1) + ') ' + self.lessons_2[i].__str__() + '\n'
            return temp


class Lesson:
    def __init__(self, name, lesson_type, teacher, cabinet):
        self.name = name
        self.lesson_type = lesson_type
        self.teacher = teacher
        self.cabinet = cabinet

    def __str__(self):
        if self.name == '':
            return ''
        return fr'{self.name}, {self.lesson_type}, {self.teacher}, {self.cabinet}'
