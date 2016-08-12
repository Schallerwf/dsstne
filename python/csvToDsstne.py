import sys
import os
import argparse
from random import randint

def convert(args):
    numItems = 0
    with open(args.csv, 'r') as csvFile:
        for line in csvFile:
            numItems += 1
    testValues = randomSplit(args.s.split('/'), numItems)

    csvFile = open(args.csv, 'r')
    headers = map(str.strip, getHeaders(args, csvFile))
    labelNdx = headers.index(args.label)
    classes = {}
    idNdx = -1

    if (args.id != ''):
        idNdx = headers.index(args.id)        

    # Input values for training
    inputNc = open(args.name + 'input.dsstne', 'w')
    outputNc = open(args.name + 'output.dsstne', 'w')

    # Files for testing model accuracy
    testNc = open(args.name + 'test.dsstne', 'w')
    truthNc = open(args.name + 'truth.dsstne', 'w')

    ndx = 0
    for line in csvFile:
        if (not line.strip()):
            continue

        columns = map(str.strip, line.split(args.d))

        curId = str(ndx)
        if (idNdx != -1):
            curId = columns[idNdx]

        columnNdx = 0
        inputLine = curId + '\t'
        outputLine = curId + '\t'
        for column in columns:
            if (columnNdx != labelNdx):
                inputLine += str(columnNdx) + ',' + str(column) + ':'
            else:
                if (isInt(headers[columnNdx])):
                    outputLine += str(column)
                else:
                    if column in classes:
                        outputLine += str(classes[column])
                    else:
                        classes[column] = len(classes)
                        outputLine += str(classes[column])
                
            columnNdx += 1

        inputLine = inputLine[:-1] #remove last : from line

        if (ndx in testValues):
            testNc.write(inputLine + '\n')
            truthNc.write(outputLine + '\n')
        else:
            inputNc.write(inputLine + '\n')
            outputNc.write(outputLine + '\n')

        ndx += 1

    print 'Generated .dsstne files from ' + str(ndx) + ' items.'
    print 'Classes: '+ str(classes)

    inputNc.close()
    outputNc.close()
    csvFile.close()

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def randomSplit(splitRatio, numValues):
    trainPercent = splitRatio[0]
    testPercent = splitRatio[1]
    print 'Performing random ' + str(trainPercent) + '/' + str(testPercent) + ' split of data.'

    numTestValues = int(float(testPercent)/100 * numValues)
    testValues = set()

    while(len(testValues) < numTestValues):
        testValues.add(randint(0, numValues))

    return testValues

def getHeaders(args, csvFile):
    if (args.header == ''):
        return csvFile.readline().split(args.d)
    else:
        headersFile = open(args.header, 'r')
        headers = headersFile.readline().rstrip('\r\n').split(args.d)
        headersFile.close()
        return headers

def validateArgs(args):
    if not os.path.isfile(args.csv):
        print 'Invalid CSV file provided. Exiting.'
        sys.exit(-1)
    if (args.header != ''):
        if not os.path.isfile(args.header):
            print 'Invalid header file provided. Exiting.'
            sys.exit(-1) 
    if ((int(args.s.split('/')[0]) + int(args.s.split('/')[1])) != 100):
        print 'Invalid split value. Exiting.'
        sys.exit(-1)

def main(argv):
      parser = argparse.ArgumentParser()
  
      parser.add_argument('csv', help='CSV to convert.')
      parser.add_argument('--header', default='', help='File containing csv header. Will use first line of CSV if not provided.')
      parser.add_argument('--label', required=True, help='Label for column being used as truth value.')
      parser.add_argument('--name', default='', help='Name to add to beginning of the 4 files generated. Optional.')
      parser.add_argument('--id', default='', help='CSV column to use as id for value. Default ids count from 0 up.')
      parser.add_argument('-d', default=',', help='Demilimeter for csv. Defaults to \',\'.')    
      parser.add_argument('-s', default='80/20', help='Train to split ratio. Defaults to 80/20.')
  
      args = parser.parse_args()
      validateArgs(args)

      convert(args)
  
      print('Done.')
  
if __name__ == '__main__':
    main(sys.argv)