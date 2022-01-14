# XML TO EXCEL FILE
import xml.etree.ElementTree as ET
from openpyxl import Workbook
import os


def readFile(filename):
    '''
        Checks if file exists, parses the file and extracts the needed data
        returns a 2 dimensional list without "header"
    '''
    if not os.path.exists(filename): return
    tree = ET.parse(filename)
    root = tree.getroot()
    # you may need to adjust the keys based on your file structure
    dict_keys = ["INDIVIDUAL", "DATAID", "FIRST_NAME", "SECOND_NAME", "THIRD_NAME", "UN_LIST_TYPE", "REFERENCE_NUMBER",
                 "LISTED_ON", "GENDER", "COMMENTS1", "DESIGNATION", "NATIONALITY", "LIST_TYPE", "LAST_DAY_UPDATED",
                 "INDIVIDUAL_ALIAS", "INDIVIDUAL_ADDRESS", "INDIVIDUAL_DATE_OF_BIRTH", "INDIVIDUAL_PLACE_OF_BIRTH",
                 "INDIVIDUAL_DOCUMENT", "NOTE"]  # all keys to be extracted from xml
    mdlist = []
    count = 0
    for child in root:
        for children in child:
            temp = []
            for key in dict_keys:
                try:
                    ind_keys = []
                    if key == "DESIGNATION" or key == "NATIONALITY" or key == "LIST_TYPE" or key == "LAST_DAY_UPDATED":
                        temp.append(children.find(key).find("VALUE").text)
                    elif key == "INDIVIDUAL_ALIAS":
                        ind_keys = ["QUALITY", "ALIAS_NAME"]
                        for each_key in ind_keys:
                            try:
                                temp.append(children.find(key).find(each_key).text)
                            except:
                                temp.append("")
                    elif key == "INDIVIDUAL_ADDRESS":
                        ind_keys = ["STREET", "CITY","STATE_PROVINCE","COUNTRY"]
                        for each_key in ind_keys:
                            try:
                                temp.append(children.find(key).find(each_key).text)
                            except:
                                temp.append("")
                        # temp.append(children.find(key).find("STREET").text)
                        # temp.append(children.find(key).find("CITY").text)
                        # temp.append(children.find(key).find("STATE_PROVINCE").text)
                        # temp.append(children.find(key).find("COUNTRY").text)
                    elif key == "INDIVIDUAL_PLACE_OF_BIRTH":
                        ind_keys = ["CITY", "STATE_PROVINCE", "COUNTRY"]
                        for each_key in ind_keys:
                            try:
                                temp.append(children.find(key).find(each_key).text)
                            except:
                                temp.append("")
                        # temp.append(children.find(key).find("CITY").text)
                        # temp.append(children.find(key).find("STATE_PROVINCE").text)
                        # temp.append(children.find(key).find("COUNTRY").text)
                    elif key == "INDIVIDUAL_DATE_OF_BIRTH":
                        ind_keys = ["TYPE_OF_DATE", "YEAR", "DATE"]
                        for each_key in ind_keys:
                            try:
                                temp.append(children.find(key).find(each_key).text)
                            except:
                                temp.append("")
                        # temp.append(children.find(key).find("TYPE_OF_DATE").text)
                        # temp.append(children.find(key).find("YEAR").text)
                        # temp.append(children.find(key).find("DATE").text)
                    elif key == "INDIVIDUAL_DOCUMENT":
                        ind_keys = ["TYPE_OF_DOCUMENT", "TYPE_OF_DOCUMENT2", "NUMBER"]
                        for each_key in ind_keys:
                            try:
                                temp.append(children.find(key).find(each_key).text)
                            except:
                                temp.append("")
                        # temp.append(children.find(key).find("TYPE_OF_DOCUMENT").text)
                        # temp.append(children.find(key).find("TYPE_OF_DOCUMENT2").text)
                        # temp.append(children.find(key).find("NUMBER").text)
                    else:
                        temp.append(children.find(key).text)
                except:
                    temp.append("")
            if temp[6].startswith("TAi"):
                count += 1
                mdlist.append(temp)
    print(count)
    return mdlist


def to_Excel(mdlist):
    '''
        Generates excel file with given data
        mdlist: 2 Dimenusional list containing data
    '''
    wb = Workbook()
    ws = wb.active
    for i, row in enumerate(mdlist):
        for j, value in enumerate(row):
            ws.cell(row=i + 1, column=j + 1).value = value
    newfilename = os.path.abspath("xml_to_excel.xlsx")
    wb.save(newfilename)
    print("complete")
    return


result = readFile("consolidated.xml")
if result:
    to_Excel(result)
