def daytonumber(dayt):
    switcher = {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5
    }
    return switcher.get(dayt, "error")


def numbertoday(number):
    switcher = {
        1: "monday",
        2: "tuesday",
        3: "wednesday",
        4: "thursday",
        5: "friday"
    }
    return switcher.get(number, 0)


def readtimetable(filename):
    timetable = {}
    inputfile = open(filename, 'r')
    while True:
        line = inputfile.readline()
        if not line:
            break
        entry = [part.strip() for part in line.split(' ')]
        # day starthour endhour name
        day = daytonumber(entry[0])
        if day in timetable.keys():
            timetable[day].append((int(entry[1]), int(entry[2]), entry[3]))
        else:
            timetable[day] = [(int(entry[1]), int(entry[2]), entry[3])]

    inputfile.close()
    return timetable


def readoptionstable(filename):
    timetable = {}
    inputfile = open(filename, 'r')
    while True:
        line = inputfile.readline()
        if not line:
            break
        entry = [part.strip() for part in line.split(' ')]
        # day starthour endhour name
        day = daytonumber(entry[0])
        if entry[3] in timetable.keys():
            timetable[entry[3]].append((day, int(entry[1]), int(entry[2])))
        else:
            timetable[entry[3]] = [(day, int(entry[1]), int(entry[2]))]

    inputfile.close()
    return timetable


def updatetimetablefile(timetable):
    file = open("newtimetable.txt", "w")
    newtt = dict(sorted(timetable.items(), key=lambda item:item[1]))
    newtt2 = dict(sorted(newtt.items()))
    for key, value in newtt2.items():
        entries = sorted(value, key=lambda item:item[1])
        for rest in entries:
            string = numbertoday(key) + ' ' + str(rest[0]) + ' ' + str(rest[1]) + ' ' + str(rest[2]) + '\n'
            file.write(string)
    file.close()


def updateoptionsfile(options, newentry):
    file = open("newoptions.txt", "w")
    options[newentry[3]] = [(newentry[0], newentry[1], newentry[2])]
    for key, entries in options.items():
        for rest in entries:
            string = numbertoday(rest[0]) + ' ' + str(rest[1]) + ' ' + str(rest[2]) + ' ' + key + '\n'
            file.write(string)
    file.close()


def Reschedule(canbechanged, day, sh, name, timetable, options):
    if name is None:
        return True
    if canbechanged[day][sh]:
        try:
            reschedule = [(x, y, z) for x, y, z in timetable[day] if x == sh]
            otherentry = reschedule[0]
            timetable[day].remove(otherentry)
        except:
            otherentry = (None, None, None)
        if day in timetable:
            timetable[day].append((sh, sh + 2, name))
        else:
            timetable[day] = [(sh, sh + 2, name)]
        canbechanged[day][sh] = False
        if Reschedule(canbechanged, day, otherentry[0], otherentry[2], timetable, options):
            return True

        canbechanged[day][sh] = True
        #reset = [(x, y, z) for x, y, z in timetable[day] if x == sh]
        timetable[day].remove((sh, sh + 2, name))
        timetable[day].append(otherentry)

    for (xday, xsh, xeh) in options[name]:
        if canbechanged[xday][xsh]:
            try:
                reschedule = [(x, y, z) for x, y, z in timetable[xday] if x == xsh]
                otherentry2 = reschedule[0]
                timetable[xday].remove(otherentry2)
            except:
                otherentry2 = (None, None, None)

            if xday in timetable:
                timetable[xday].append((xsh, xsh + 2, name))
            else:
                timetable[xday] = [(xsh, xsh + 2, name)]
            canbechanged[xday][xsh] = False
            if Reschedule(canbechanged, xday, otherentry2[0], otherentry2[2], timetable, options):
                return True

            canbechanged[xday][xsh] = True
            #reset = [(x, y, z) for x, y, z in timetable[xday] if x == xsh]
            timetable[xday].remove((xsh, xsh + 2, name))
            timetable[xday].append(otherentry2)

    return False


if __name__ == '__main__':
    options = readoptionstable("options.txt")
    timetable = readtimetable("timetable.txt")
    entrylist = []
    day = 0
    eh = 0
    sh = 0
    name = ''
    while True:
        tofreeup = input(
            "Enter day(name in lowercase), start hour, end hour (8-20) and name for active you want to insert: ")
        entrylist = [part.strip() for part in tofreeup.split(' ')]
        # sh = start hour
        # eh = end hour
        day = daytonumber(entrylist[0])
        sh = int(entrylist[1])
        eh = int(entrylist[2])
        name = entrylist[3]
        # check day too
        if sh < eh and sh>=8 and sh<20 and eh>8 and eh<=20:
            break
        else:
            print("End hour must be greater than start hour, both must be in the 8-20 interval.")

    canbechanged = []
    for i in range(5):
        canbechanged.append({8: True, 10: True, 12: True, 14: True, 16: True, 18: True})
    if Reschedule(canbechanged, day, sh, name, timetable, options):
        print("Inserted successfully! Check newtimetable.txt for your rearranged timetable.")
        updatetimetablefile(timetable)
        updateoptionsfile(options, (day, sh, eh, name))
    else:
        print("Could not be inserted!")
