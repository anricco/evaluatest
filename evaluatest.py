#!/usr/bin/python

#------------------------------------------------------------------------------#
#                                                                              #
#                                                                              #
#                                EVALUATEST                                    #
#                            (Mac OS X version)                                #
#                               Antonio Ricco                                  #
#                                                                              #
#------------------------------------------------------------------------------#

import os
import sys
import fileinput

import numpy
#import math

# to add command line options
import argparse

#import random
#import itertools

#from pdfrw import PdfReader, PdfWriter


# - FROM MAKETEST2
def removeExtension(fileName):
    base=os.path.basename(fileName) # only filename without path
    removedExtensionFile = os.path.splitext(base)[0] # extension =  os.path.splitext(base)[1]
    return removedExtensionFile



# it opens a .csv file with tab as separator and converts it in a matrix list - FROM MAKETEST2
def csvFileToMatrix(csvFileName, csvFilePath):
    outputMatrix = []

    for line in fileinput.input( csvFilePath + "/" + csvFileName ):
        outputMatrixLine = []
        for k in range(0,line.count("\t")+1):
            outputMatrixLine.append(line.split("\t")[k].rstrip())  # rstrip() removes \n, \r, etc.
        outputMatrix.append(outputMatrixLine)

    return outputMatrix



# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \t
# and rows separated by \n
def matrixToCsvFile(inputMatrix, csvFileName, csvFilePath):
    outputCsvFile = open( csvFilePath + "/" + csvFileName, 'w' )

    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            outputCsvFile.write ( str(inputMatrix[j][k]) + "\t" )
        outputCsvFile.write ( str(inputMatrix[j][len(inputMatrix[j])-1]) + "\n" )

    outputCsvFile.close()


# trasposition of matrices  - FROM MAKETEST2
# https://stackoverflow.com/questions/4937491/matrix-transpose-in-python#9622534
def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)


# removes the first two rows and the firs column of a matrix
def stripMatrix(matrix):
    del matrix[0]
    del matrix[0]
    newMatrix = transposed(matrix)
    #print newMatrix[0]
    del newMatrix[0]
    #print newMatrix

    matrix = transposed(newMatrix)
    return matrix


# It creates the matrix containing the answers to the questions
# with the questions in the original order (answersoutMatrix[30][39]) (same order for all versions)
# *before* rearranging also the answer order
# Matrix = [[0 for x in range(w)] for y in range(h)]
def rearrangeOrderMatrix(verNumber, qNumber, inMatrix, orderinMatrix):

    # print inMatrix
    # print orderinMatrix
    outMatrix = []
    for j in range(0,verNumber+1):
        outLine = ["-" for x in range(0,qNumber)]
        for k in range(0,qNumber):
            outLine[int(orderinMatrix[j][k])-1:int(orderinMatrix[j][k])] = [inMatrix[j][k]]
        outMatrix.append(outLine)

    # print outMatrix
    return outMatrix





# takes the answer given by the students to a specific question and returns the answer in the original order
# i.e. if it is the correct one it returns 'A'
def rearrangeAnswer(givenAnswer, qType, answersOrderString):
    answersOrderList = list(answersOrderString)
    # print answersOrderList
    givenAnswer = givenAnswer.upper()
    # print givenAnswer
    answersDict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
    inverseAnswersDict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}


    # print givenAnswerNumber

    answer = ""
    if not givenAnswer:
        answer = '-'
    elif (givenAnswer == 'A' or givenAnswer == 'B' or givenAnswer == 'C' or givenAnswer == 'D' or givenAnswer == 'E'):
        givenAnswerNumber = answersDict[givenAnswer]
        answer = inverseAnswersDict[int(answersOrderList[givenAnswerNumber-1])]
    else:
        answer = givenAnswer
    # print answer

    return answer



def rearrangeQAMatrix(verNumber, qNumber, givenAnswersMatrix, qAnswerOrderMatrix, qNumberMatrix):

    rearrangedGivenAnswersMatrix = rearrangeOrderMatrix(verNumber, qNumber, givenAnswersMatrix, qNumberMatrix)
    # print rearrangedGivenAnswersMatrix

    rearrangedQAnswerOrderMatrix = rearrangeOrderMatrix(verNumber, qNumber, qAnswerOrderMatrix, qNumberMatrix)
    # print rearrangedQAnswerOrderMatrix

    outMatrix = []
    for j in range(0,verNumber+1):
        outLine = ["X" for x in range(0,qNumber)]
        for k in range(0,qNumber):
             outLine[k:k+1] = [rearrangeAnswer(rearrangedGivenAnswersMatrix[j][k],4,rearrangedQAnswerOrderMatrix[j][k])] #rearrangeAnswer( ]
        outMatrix.append(outLine)

    return outMatrix



# It creates a matrix containing the scores for each version and each question
def makePointsMatrix(verNumber, qNumber, AnswersMatrix, keyinMatrix):

    pointsMatrix = []

    # print AnswersMatrix
    for j in range(0,verNumber+1):
        pointsLine = [1 for x in range(0,qNumber)]
        for k in range(0,qNumber):
            keyinList = list(keyinMatrix[k][1]) # it is used for the case in which there are multiple answers
            if AnswersMatrix[j][k] == "-" or AnswersMatrix[j][k] == "":
                pointsLine[k:k+1] = [int(keyinMatrix[k][3])] # points for empty answer
            elif AnswersMatrix[j][k] == keyinList[0]:
                pointsLine[k:k+1] = [int(keyinMatrix[k][2])] # points for correct answer
            elif len(keyinList)>1:
                # print keyinList
                # print len(keyinList)
                if AnswersMatrix[j][k] == keyinList[1]:
                    pointsLine[k:k+1] = [int(keyinMatrix[k][2])] # points for correct answer
                elif len(keyinList)>2:
                    # print keyinList
                    if AnswersMatrix[j][k] == keyinList[2]:
                        pointsLine[k:k+1] = [int(keyinMatrix[k][2])] # points for correct answer
                        # print keyinList
                    elif len(keyinList)>3:
                        if AnswersMatrix[j][k] == keyinList[3]:
                            pointsLine[k:k+1] = [int(keyinMatrix[k][2])] # points for correct answer
                        else:
                            pointsLine[k:k+1] = [0]
                    else:
                        pointsLine[k:k+1] = [0]
                else:
                    pointsLine[k:k+1] = [0]
            else:
                pointsLine[k:k+1] = [0]
        pointsMatrix.append(pointsLine)

    # print pointsMatrix
    return pointsMatrix




# It sums the scores on each line of a pointsMatrix
def makeScoresList(verNumber, qNumber, pointsMatrix):
    scoresList = []

    for j in range(0,verNumber+1):
        scoresList[j:j+1] = [0]
        for k in range(0,qNumber):
            scoresList[j] = scoresList[j] + pointsMatrix[j][k]

    # print scoresList
    return scoresList


def makeResultsMatrix(scoresList):
    resultsMatrix = []

    for j in range(0, len(scoresList)):
        resultsMatrixLine = [0,0]
        resultsMatrixLine[0] = `j`
        resultsMatrixLine[1] = `scoresList[j]`
        resultsMatrix.append(resultsMatrixLine)

    # print resultsMatrix
    return resultsMatrix


def compareAnswerString(answerString1, answerString2, qNumber, pointsMatrix):
    index = 0
    for k in range(0,qNumber):
        if answerString1[k] == answerString2[k]:
            index = index + 1

    return index

def compareAnswerString2(answerString1, answerString2, qNumber, pointsMatrix):
    index = 0
    for k in range(0,qNumber):
        if answerString1[k] == 'A' and answerString1[k] == answerString2[k]:
            index = index + 1
        elif  answerString1[k] != '-' and answerString1[k] == answerString2[k]:
            index = index + 3
    return index


def compareAnswerString3(answerString1, answerString2, qNumber, pointsMatrix):
    index = 0
    for k in range(0,qNumber):
        if answerString1[k] == 'A' and answerString1[k] == answerString2[k]:
            index = index
        elif  answerString1[k] != '-' and answerString1[k] == answerString2[k]:
            index = index + 3
    return index



# takes the rearranged answers matrix and compares the answers for each couple of versions
def makeCorrelationMatrix(answersMatrix, verNumber, qNumber):

    correlationMatrix = []

    for j1 in range(0,verNumber+1):
        correlationLine = [0 for x in range(0,verNumber+1)]
        for j2 in range(0,verNumber):
            if j1 != j2:
                correlationLine[j2:j2+1] = [compareAnswerString(answersMatrix[j1], answersMatrix[j2], qNumber," ")]
            else:
                correlationLine[j2:j2+1] = [0]

        correlationMatrix.append(correlationLine)

    return correlationMatrix


def makeCorrelationMatrix2(answersMatrix, verNumber, qNumber):

    correlationMatrix = []

    for j1 in range(0,verNumber+1):
        correlationLine = [0 for x in range(0,verNumber+1)]
        for j2 in range(0,verNumber):
            if j1 != j2:
                correlationLine[j2:j2+1] = [compareAnswerString2(answersMatrix[j1], answersMatrix[j2], qNumber," ")]
            else:
                correlationLine[j2:j2+1] = [0]
        correlationMatrix.append(correlationLine)

    return correlationMatrix


def makeCorrelationMatrix3(answersMatrix, verNumber, qNumber):

    correlationMatrix = []

    for j1 in range(0,verNumber+1):
        correlationLine = [0 for x in range(0,verNumber+1)]
        for j2 in range(0,verNumber):
            if j1 != j2:
                correlationLine[j2:j2+1] = [compareAnswerString3(answersMatrix[j1], answersMatrix[j2], qNumber," ")]
            else:
                correlationLine[j2:j2+1] = [0]
        correlationMatrix.append(correlationLine)

    return correlationMatrix




# it defines all the global variables associated to the project,
# such as projectMatrix, projectName, projectType, versionNumber, etc.
def readProject(projectFileName):

        #### LIST OF CONSTANTS ####

    global projectMatrix
    projectMatrix = csvFileToMatrix(projectFileName, mainpath)
    print "projectMatrix: \n" + `projectMatrix` + "\n\n"
    # sys.stdout
    #matrixToCsvFile(projectMatrix, `sys.stdout`, "")

    # PROJECT NAME, TYPE AND TOTAL NUMBER OF VERSIONS
    global projectName, projectType, versionNumber, questionNumber
    projectName = projectMatrix[0][1]
    projectType = projectMatrix[1][1]
    versionNumber = int(projectMatrix[2][1])
    # print versionNumber
    questionNumber = int(projectMatrix[3][1])
    # print questionNumber

    # matrix with the order of the keys (for the version 0)
    global keyinFileName
    keyinFileName = projectMatrix[8][1]
    # print keyinFileName

    #INPUT FILE NAMES THAT ARE OUTPUT FROM MAKETEST
    global qNumberFileName, qAnswerOrderFileName, qKeyFileName, givenAnswersFileName
    qNumberFileName = projectMatrix[11][1]

    qAnswerOrderFileName = projectMatrix[13][1]
    qKeyFileName = projectMatrix[14][1]

    givenAnswersFileName = projectMatrix[16][1]

    #### END LIST OF CONSTANTS ####





def main():

        #### LIST OF CONSTANTS ####

    global mainpath
    mainpath = os.getcwd()

        #### COMMAND LINE OPTIONS ####
    parser = argparse.ArgumentParser()
    # parser.parse_args()
    parser.add_argument("project", help="the project filename")
    args = parser.parse_args()
    projectFileName = args.project
    # pprint args.project
    print "projectFileName: " + projectFileName + "\n"

    # readProject defines all the global variables associated to the project
    readProject(projectFileName)


    # matrix with the order of the keys (for the version 0)
    keyinMatrix =  csvFileToMatrix(keyinFileName, mainpath + "/input" )
    # print keyinMatrix


    # matrix with the order of the questions
    qNumberMatrix =  stripMatrix(csvFileToMatrix(qNumberFileName, mainpath + "/input" ))
    # print qNumberMatrix

    # matrix with the order of the answers in the form of strings, e.g. '1234'
    qAnswerOrderMatrix = stripMatrix(csvFileToMatrix(qAnswerOrderFileName, mainpath + "/input" ))
    # print qAnswerOrderMatrix

    givenAnswersMatrix = stripMatrix(csvFileToMatrix(givenAnswersFileName, mainpath + "/input" ))
    # print givenAnswersMatrix

    rearrangedGivenAnswersMatrix = rearrangeQAMatrix(versionNumber, questionNumber, givenAnswersMatrix, qAnswerOrderMatrix, qNumberMatrix)
    # print rearrangedGivenAnswersMatrix

    matrixToCsvFile(rearrangedGivenAnswersMatrix,  projectName + "-rearranged-answers" + ".csv", mainpath + "/output")

    pointsMatrix = makePointsMatrix(versionNumber, questionNumber, rearrangedGivenAnswersMatrix, keyinMatrix)

    scoresList = makeScoresList(versionNumber, questionNumber, pointsMatrix)

    resultsMatrix = makeResultsMatrix(scoresList)
    # print resultsMatrix

    matrixToCsvFile(resultsMatrix,  projectName + "-results" + ".csv", mainpath + "/output")

    # print rearrangedGivenAnswersMatrix[0]

    correlationMatrix = makeCorrelationMatrix(rearrangedGivenAnswersMatrix, versionNumber, questionNumber)
    # print correlationMatrix

    matrixToCsvFile(correlationMatrix, projectName +  "-correlation1" + ".csv", mainpath + "/output")

    correlationMatrix2 = makeCorrelationMatrix2(rearrangedGivenAnswersMatrix, versionNumber, questionNumber)
    # print correlationMatrix2

    matrixToCsvFile(correlationMatrix2,  projectName + "-correlation2" + ".csv", mainpath + "/output")

    correlationMatrix3 = makeCorrelationMatrix3(rearrangedGivenAnswersMatrix, versionNumber, questionNumber)
    # print correlationMatrix3

    matrixToCsvFile(correlationMatrix3,  projectName + "-correlation3" + ".csv", mainpath + "/output")


main()