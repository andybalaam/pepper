from pepper2like.outfile import OutFile
from pepper2like.type_check import type_check

class PartLineLog:
    def __init__(self, out):
        type_check(OutFile, out)
        self.out = out

    def info(self, msg):
        self.out.write(msg)

class Log:
    def __init__(self, out):
        self.out = out
        self.part_line = PartLineLog(out)
    def info(self, msg):
        self.out.write("%s\n" % msg)

Log.part_line = PartLineLog
