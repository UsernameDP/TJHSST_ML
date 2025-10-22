from naivebayes import *
import sys

args = sys.argv[1:]

train_file = args[0]
test_file = args[1]

output = naiveBayes(train_file)
results = testNaiveBayes(test_file, output)
logMetrics(results)
