#
# Create photo info csv file by mergeing info of photo trap capture sheet
# extracted from diana_analysis.xlsx
#
#     This script requires three csv files. so prepare the csv files which 
#     extracted from diana_analysis_yyyymmddhhmm.xlsx in advance.
#
# USAGE:
#
#     $ python3.10 create-photoinfo.py filename filename filename
#
#     Order of 3 filenames:
#
#         1st: filename of photo sheet csv
#         2nd: filename of trap sheet csv
#         3rd: filename of capture sheet csv
#


import sys
import csv


# ah, you should check command line arguments :-P
photcsv = sys.argv[1]
trapcsv = sys.argv[2]
captcsv = sys.argv[3]

# a record of phot sheet csv
class photdatum:
    def __init__(self):
        self.filename = ""
        self.instid = ""
        self.cnfmid = ""
        self.captid = ""
        self.date = ""
        self.trap = trapdatum()
        self.capt = captdatum()

    def setcsv(self, row):
        field = 1

        for col in row:
            if field == 1:
                self.filename = col
            elif field == 2:
                self.instid = col
            elif field == 3:
                self.cnfmid = col
            elif field == 5:
                self.captid = col
            elif field == 7:
                self.date = col
                break

            field += 1

    def record(self):
        return f"{self.filename}, {self.instid}, "\
            f"{self.cnfmid}, {self.captid}, {self.date}"

    def print_record(self):
        print(self.record())


# a record of trap sheet csv
class trapdatum:
    def __init__(self):
        self.instid = ""
        self.cnfmid = ""
        self.username = ""
        self.date = ""
        self.trapnum = ""
        self.treated = ""

    def setcsv(self, row):
        field = 1

        for col in row:
            if field == 1:
                self.instid = col
            elif field == 2:
                self.cnfmid = col
            elif field == 4:
                self.username = col
            elif field == 6:
                self.date = col
            elif field == 18:
                self.trapnum = col
            elif field == 19:
                self.treated = col
                break

            field += 1

    def record(self):
        return f"{self.instid}, {self.cnfmid}," \
            f"{self.username}, {self.date}, {self.trapnum}, {self.treated}"

    def print_record(self):
        print(self.record)


# a record of capture sheet csv
class captdatum:
    def __init__(self):
        self.captid = ""
        self.cnfmid = ""
        self.username = ""
        self.date = ""
        self.city = ""
        self.how = ""
        self.tool = ""
        self.animal = ""
        self.sex = ""
        self.age = ""
        self.remarks = ""

    def setcsv(self, row):
        field = 1

        for col in row:
            if field == 1:
                self.captid = col
            elif field == 4:
                self.cnfmid = col
            elif field == 7:
                self.username = col
            elif field == 8:
                self.date = col
            elif field == 17:
                self.city = col
            elif field == 18:
                self.how = col
            elif field == 19:
                self.tool = col
            elif field == 21:
                self.animal = col
            elif field == 23:
                self.sex = col
            elif field == 24:
                self.age = col
            elif field == 37:
                self.remarks = col
                break

            field += 1

    def record(self):
        return f"{self.captid}, {self.cnfmid}, {self.username}, " \
            f"{self.date}, {self.city}, {self.how}, {self.tool}, " \
            f"{self.animal}, {self.sex}, {self.age}, {self.remarks}"

    def print_record(self):
        print(self.record)


#
# store phot sheet csv to list
#
photdata = []
with open(photcsv, "r") as pcsv:
    for row in csv.reader(pcsv, delimiter=','):
        datum = photdatum()
        datum.setcsv(row)
        photdata.append(datum)


#
# store trap sheet csv to list
#
trapdata = []
with open(trapcsv, "r") as tcsv:
    for row in csv.reader(tcsv, delimiter=','):
        datum = trapdatum()
        datum.setcsv(row)
        trapdata.append(datum)

#
# store capture sheet csv to list
#
captdata = []
with open(captcsv, "r") as ccsv:
    for row in csv.reader(ccsv, delimiter=','):
        datum = captdatum()
        datum.setcsv(row)
        captdata.append(datum)

#
# merge trapdata to photdata
#
for ph in photdata:
    if "" != ph.instid:
        for tr in trapdata:
            if ph.instid == tr.instid:
                ph.trap = tr
                break
    elif "" != ph.cnfmid:
        for tr in trapdata:
            if ph.cnfmid == tr.cnfmid:
                ph.trap = tr
                break

    if "" != ph.captid:
        for cp in captdata:
            if ph.captid == cp.captid:
                ph.capt = cp

                # no trapdatum yet ?
                if "" == ph.trap.username:
                    if "" != cp.cnfmid:
                        for tr in trapdata:
                            if cp.cnfmid == tr.cnfmid:
                                ph.trap = tr
                                break
                break

#
# show result
#
for datum in photdata:
    print(f"{datum.record()}, {datum.trap.record()}, {datum.capt.record()}")
