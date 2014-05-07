#classGetdata.py

import xlrd
import os

def getStudentValues():
	#access the housing data, which is just on the desktop
	book = xlrd.open_workbook("../../Desktop/classData.xls")

	#we only have 1 sheet, and only care about the first sheet
	housingData = book.sheet_by_index(0)

	#print "Cell D30 is", housingData.cell_value(rowx=29, colx=3)

	studentNames = {}
	studentValues = {}
	numStudent = 0
	#this gets us a dictionary of student id to arrays
	#each individual key-value (id to array) stores the information provided for each student
	#the first entry is gender, followed by 8 numbers for the ROOMMATE ranking questions, then 2 numbers for GROUP rankings
	for rowIndex in range(1, housingData.nrows):
		indivValues = []
		for colIndex in range(0, 12):
			cellVal = housingData.cell_value(rowx=rowIndex, colx=colIndex)
			if colIndex == 0 :
				studentNames[numStudent] = cellVal
			else : 
				if colIndex > 1 :
					cellVal = float(cellVal)
				indivValues.append(cellVal)
		studentValues[numStudent] = indivValues
		
	   	numStudent += 1

	return (studentNames, studentValues)