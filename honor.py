"""
By Rose,
https://github.com/Rose-zk
Rose#6188 on Discord
"""

from webbrowser import open as wopen

class Honor:
    def __init__(self, honor_value, honor_type):
        self.honor_value = int(honor_value)
        self.honor_type = honor_type

    def get_honor(self):
        return self.honor_value


class HonorableKill(Honor):
    def __init__(self, level, rank, honor_value, confirmed):
        Honor.__init__(self, honor_value, "Honorable Kill")
        self.level = level
        self.rank = rank
        self.confirmed = int(confirmed)

    def output(self):
        if self.confirmed >= 2:
            return ("L" + str(self.level) + "R" + str(self.rank) + " <b>(HP:" + str(self.honor_value) + ")</b>")
        elif self.confirmed < 2:
            return (
            "L" + str(self.level) + "R" + str(self.rank) + " <b>(HP:" + str(self.honor_value) + ")</b> <i>(unsafe)</i>")


class MarkOfHonor(Honor):
    def __init__(self):
        Honor.__init__(self, 398, "3 Marks of Honor")



def match_honor(value, honorable_kills):
    for item in honorable_kills:
        if item.honor_value == value:
            return item


def file_reader():
    return_list = []
    with open("honor.csv") as file:
        file.readline()
        for line in file:
            hk = line.split(";")
            return_list.append(HonorableKill(hk[0], hk[1], hk[2], hk[3]))
        return return_list


def input_arguments():
    int_checker = True
    while int_checker:
        try:
            current_honor = int(input("What is your current honor?"))
            cap_goal = int(input("What is your goal?"))
            if current_honor < cap_goal:
                return current_honor, cap_goal
            else:
                raise ValueError
        except ValueError:
            print("Please use integers only.")


def subset_sum(honorable_kill_values, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(honorable_kill_values):
        remaining = honorable_kill_values[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)


def find_smaller_than_target(target, honorable_kills):
    viable_kills = []
    for item in honorable_kills:
        if target < item.honor_value and (target - item.honor_value) > 47:
            viable_kills.append(item)
        elif target == item.honor_value:
            viable_kills.append(item)
    return viable_kills, target


def honor_calculator(honor_difference):
    marks = MarkOfHonor()
    honorable_kills = file_reader()
    honorable_kill_values = []
    for item in honorable_kills:
        if item.get_honor() not in honorable_kill_values:
            honorable_kill_values.append(item.get_honor())
    paths = []
    if honor_difference % 398 == 0:
        number_of_marks = int(honor_difference / 398)
    elif honor_difference % 398 > 47:
        number_of_marks = int((honor_difference - (honor_difference % 398)) / 398)
    elif honor_difference % 398 < 47:
        number_of_marks = int((honor_difference - (honor_difference % 398)) / 398) + 1
    paths.append([number_of_marks, marks])
    remainder = honor_difference - (number_of_marks * 398)
    for i in subset_sum(honorable_kill_values, remainder):
        paths.append(i)

    return paths, honorable_kills


def main():
    current_honor, cap_goal = input_arguments()
    honor_difference = cap_goal - current_honor
    paths, honorable_kills = honor_calculator(honor_difference)
    with open("honor paths.htm", "w") as file:
        file.write(
            "<html><head><style>body{background-color:#e1e1e1;}p{color:#5f5f5f;font-family:'Sans-serif';font-size:'10px';border:1px;border-color:#f1f1f1;}</style></head><body>")
        file.write("<p>" + str(paths[0][0]) + " Battlemaster turn ins (<i>" + str(
            paths[0][0] * 3) + " marks)</i> </p><p><b>HK Paths: </b></p>")
        for item in paths[1:]:
            file.write("<p>")
            i = 1
            for items in item:
                it = match_honor(items, honorable_kills)
                file.write(it.output())
                if len(item) > 1:
                    if i < len(item):
                        i += 1
                        file.write(" -- ")
            file.write("</p>")
        file.write("</body></html>")
        wopen("honor paths.htm")


main()
