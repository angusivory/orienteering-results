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

clubList = []
for key in listofclubs:
    clubList.append(key)
print(clubList)

for key in listofclubs:
    print("<option value='{}'>{}</option>".format(listofclubs[key], key))

