from tqdm import tqdm


class dataType:
    def __init__(self):
        self.__fd = open('data.txt', 'r')
        self.__total = 0
        self.__correct = 0

    def get_train_line(self):
        while True:
            line = self.__fd.readline().strip()
            if len(line) > 0:
                return line

    def getTestLine(self):
        # FIXME: logical is not modified for this task
        while True:
            self.__buffer = self.__fd.readline().strip()
            line = self.__buffer
            for word in line.split():
                line = line.replace(word, word.split('/')[0])
            if len(line) > 0:
                return line

    def testLine(self, line):
        # FIXME: logical is not modified for this task
        lineList = line.split()
        bufferList = self.__buffer.split()
        l = len(lineList)
        for i in range(l):
            self.__total += 1
            if lineList[i].split('/')[1] == bufferList[i].split('/')[1]:
                self.__correct += 1

    def report(self):
        print('Accuracy = %.5f' % (self.__correct / self.__total))


def driver(train_lines=100, testLines=None, train_function=None, posTagFunction=None):
    data = dataType()

    tqdm.write("Training start!")
    for _ in tqdm(range(train_lines)):
        line = data.get_train_line()
        train_function(line)

    # tqdm.write("Evaluate start!")
    # for i in tqdm(range(testLines)):
    #     data.testLine(posTagFunction(data.getTestLine()))
    #
    # tqdm.write("Report start!")
    # data.report()
