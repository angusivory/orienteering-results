import requests
import datetime
now = datetime.datetime.now()

print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)

print("last used at {}:{}:{} on {}/{}/{}".format(now.hour, now.minute, now.second, now.day, now.month, now.year))


class TheUsual():
    def __init__(self):

        self.normalmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.leapyearmonths = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.monthrewind = False

        if now.day < 8:
            self.monthrewind = True
            if now.year % 4 != 0:
                self.dayFrom = (now.day - 7)%self.normalmonths[now.month - 2]
                if self.dayFrom == 0:
                    self.dayFrom = self.normalmonths[now.month - 2]
            else:
                self.dayFrom = (now.day - 7)%self.leapyearmonths[now.month - 2]
                if self.dayFrom == 0:
                    self.dayFrom = self.leapyearmonths[now.month - 2]
        else:
            self.dayFrom = now.day - 7
        if len(str(self.dayFrom)) == 1:
            self.dayFrom = "0{}".format(self.dayFrom)

        if self.monthrewind == True:
            self.monthFrom = now.month - 1
        else:
            self.monthFrom = now.month
        if len(str(self.monthFrom)) == 1:
            self.monthFrom = "0{}".format(self.monthFrom)

        self.yearFrom = now.year

        self.dateFrom = [str(self.dayFrom), str(self.monthFrom), str(self.yearFrom)]
        self.dateTo = "now"
        self.level = "all"
        self.assoc_num = "all"
        self.host_club_num = "any"
        self.searchType = "club"
        self.searchQuery = "INT"

class setup():
    def __init__(self, params):
        self.params = params

Vars = setup("")

Vars.params = TheUsual()
website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level={}&evt_type=0&event_club={}&evt_start_d={}&evt_start_m={}&evt_start_y={}&evt_end_d={}&evt_end_m={}&evt_end_y={}&evt_assoc={}&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format(Vars.params.level, Vars.params.host_club_num, Vars.params.dateFrom[0], Vars.params.dateFrom[1], Vars.params.dateFrom[2], Vars.params.dateTo[0], Vars.params.dateTo[1], Vars.params.dateTo[2], Vars.params.assoc_num))


print(jeff.dateFrom)


import external_funcs

searchYOBs = []
listofclubs = {"AIRE": 23, "AROS": 147, "AUOC": 158, "AYROC": 58, "BADO": 89, "BAOC": 117, 
                "BASOC": 62, "BKO": 91, "BL": 60, "BOF": 152, "BOK": 44, "CHIG": 92, 
                "CLARO": 24, "CLOK": 41, "CLYDE": 63, "COBOC": 38, "CUOC": 112, "DEE": 61, 
                "DEVON": 45, "DFOK": 94, "DRONGO": 139, "DUOC": 134, "DVO": 21, "EBOR": 25, 
                "ECKO": 65, "ELO": 67, "EPOC": 26, "ERYRI": 53, "ESOC": 68, "EUOC": 111, 
                "FERMO": 87, "FVO": 69, "GMOA": 120, "GO": 95, "GRAMP": 71, "GUOC": 153, 
                "HALO": 27, "HAVOC": 32, "HH": 96, "HOC": 39, "INT": 72, "INVOC": 73, 
                "IOM OK": 166, "JOK": 121, "KERNO": 46, "KFO": 74, "LEI": 29, "LOC": 64, 
                "LOG": 30, "LOK": 97, "LUOC": 157, "LUUOC": 151, "LVO": 88, "MA": 161, 
                "MAROC": 75, "MDOC": 66, "MOR": 76, "MV": 99, "MWOC": 54, "NATO": 50, 
                "NGOC": 15, "NN": 55, "NOC": 31, "NOR": 33, "NWO": 47, "NWOC": 90, 
                "OD": 19, "OROX": 163, "OUOC": 114, "PARCOR": 165, "PFO": 78, 
                "POTOC": 40, "QO": 48, "RAFO": 115, "RNRMOC": 128, "RR": 77, 
                "RSOC": 159, "SARUM": 49, "SAX": 148, "SBOC": 56, "SELOC": 79, "SHUOC": 129, 
                "SLOW": 100, "SMOC": 34, "SN": 101, "SO": 105, "SOC": 102, "SOFA": 103, 
                "SOLWAY": 80, "SOS": 35, "SPOOK": 137, "SROC": 81, "STAG": 82, "SUFFOC": 36, 
                "SWOC": 57, "SYO": 28, "TAY": 84, "TINTO": 86, "TVOC": 104, "UBOC": 132, 
                "WAOC": 37, "WAROC": 83, "WCH": 42, "WCOC": 85, "WIGHTO": 106, "WIM": 51, 
                "WRE": 43, "WSX": 52, "XPLORER": 160}

class Params():
    def __init__(self):
        self.associations = {"BOF": 14, "BSOA": 13, "EAOA": 1, "EMOA": 2, "NEOA": 3, "NIOA": 4, "NWOA": 5, "SCOA": 6, "SEOA": 7, "SOA": 8, "SWOA": 9, "WMOA": 10, "WOA": 11, "YHOA": 12}
        self.dateFrom = str(input("Set date from which to get results (dd/mm/yyyy)\n"))
        self.dateFrom = self.dateFrom.split("/")
        if not len(self.dateFrom) == 3:
            self.dateFrom = ["0", "0", "0"]

        self.dateTo = str(input("Set end date to get results until (dd/mm/yyyy)\nIf you don't want a specific end date, type 'now'\n"))
        self.dateTo = self.dateTo.split("/")
        if not len(self.dateTo) == 3:
            self.dateTo = ["0", "0", "0"]

        self.level = input("What level events? Type '0' for all, '1' for Major, '2' for National, '3' for Regional or '-4' for all except local.\n")
        
        self.assoc = input("[opt] Specify region: BOF, BSOA, EAOA, EMOA, NEOA, NIOA, NWOA, SCOA, SEOA, SOA, SWOA, WMOA, WOA, YHOA, all.\n").upper()
        if self.assoc in self.associations:
            self.assoc_num = self.associations[self.assoc]
        else:
            self.assoc_num = 0

        self.host_club = input("[opt] Specify host club abbr. or 'any'\n").upper()
        if self.host_club in listofclubs:
            self.host_club_num = listofclubs[self.host_club]
        else:
            self.host_club_num = 0

        if str(input("Search by 'age' or 'club'?\n")) == "age":
            self.searchQuery = external_funcs.agetoyears()
            self.searchType = "age"
        else:
            self.searchQuery = str(input("Which club do you want to search for? (use abbr.)\n")).upper()
            self.searchType = "club"


#GET SEARCH INFO
SearchInfo = Params()
website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level={}&evt_type=0&event_club={}&evt_start_d={}&evt_start_m={}&evt_start_y={}&evt_end_d={}&evt_end_m={}&evt_end_y={}&evt_assoc={}&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format(SearchInfo.level, SearchInfo.host_club_num, SearchInfo.dateFrom[0], SearchInfo.dateFrom[1], SearchInfo.dateFrom[2], SearchInfo.dateTo[0], SearchInfo.dateTo[1], SearchInfo.dateTo[2], SearchInfo.assoc_num))
print("Searching all current {} level {} results hosted by {} from {}/{}/{} to {}/{}/{} in the {} region.".format(SearchInfo.searchQuery, SearchInfo.level, SearchInfo.host_club, SearchInfo.dateFrom[0], SearchInfo.dateFrom[1], SearchInfo.dateFrom[2], SearchInfo.dateTo[0], SearchInfo.dateTo[1], SearchInfo.dateTo[2], SearchInfo.assoc))
