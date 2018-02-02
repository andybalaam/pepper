
class OutFile:
    @staticmethod
    def is_satisfied_by(other):
        try:
            other.write
            return True
        except AttributeError:
            return False
