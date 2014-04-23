#read in excel file of data and format

import xlrd
import os


#access the housing data, which is just on the desktop
book = xlrd.open_workbook("../../Desktop/Housing Data 2017.xls")

#we only have 1 sheet, and only care about the first sheet
housingData = book.sheet_by_index(0)

print "Cell D30 is", housingData.cell_value(rowx=29, colx=3)
numStudent = 0

#this for loop gets us ordered pairs of every student and their entries in the columns
#skips the first line because this just labels columns
for rx in range(1, housingData.nrows):
    print (numStudent, housingData.row(rx))
    numStudent += 1
