#read in excel file of data and format

import xlrd
import os

def getStudentValues():
	#access the housing data, which is just on the desktop
	book = xlrd.open_workbook("../../Desktop/Housing Data 2017.xls")

	#we only have 1 sheet, and only care about the first sheet
	housingData = book.sheet_by_index(0)

	#print "Cell D30 is", housingData.cell_value(rowx=29, colx=3)


	studentValues = []
	numStudent = 0
	#this gets us an array of arrays
	#each individual array stores the information provided for each student
	#the first entry is gender, followed by 8 numbers for the ranking questions
	for rowIndex in range(1, housingData.nrows):
		indivValues = []
		for colIndex in range(1, 10):
			#print (rowIndex, colIndex)
			cellVal = housingData.cell_value(rowx=rowIndex, colx=colIndex)
			indivValues.append(cellVal)
		studentValues.append(indivValues)
	   	numStudent += 1

	#print studentValues
	return studentValues