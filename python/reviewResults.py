import sys
import os
import argparse
from itertools import izip

def compare(args):

	with open(args.prediction) as prediction, open(args.expected) as expected:
		numItems = 0
		numCorrectGuesses = 0
		print 'Prediction : Expected'
		for a, e in izip(prediction, expected):
			numItems += 1
			a = a.strip()
			e = e.strip()
			
			expectedClass = e.split('\t')[1]
			predictions = a.split('\t')[1].split(':')
			classScores = []

			predictedClass = -1
			maxScore = -1
			for prediction in predictions:
				if (not prediction.strip()):
					continue

				parts = prediction.split(',')
				if (parts[1] > maxScore):
					maxScore = parts[1]
					predictedClass = parts[0]


			print str(predictedClass) + '            ' + expectedClass

			if (predictedClass == str(expectedClass)):
				numCorrectGuesses += 1

	print str(numCorrectGuesses) + ' correct guesses out of ' + str(numItems)


def validateArgs(args):
    if not os.path.isfile(args.prediction):
        print 'Invalid prediction file provided.'
        sys.exit(-1)
    if not os.path.isfile(args.expected):
        print 'Invalid expected file provided.'
        sys.exit(-1)

def main(argv):
      parser = argparse.ArgumentParser()
  
      parser.add_argument('prediction', help='Output from DSSTNE predict.')
      parser.add_argument('expected', help='Expected output.')  
  
      args = parser.parse_args()
      validateArgs(args)

      compare(args)
  
if __name__ == '__main__':
    main(sys.argv)