
class Callable:
    @staticmethod
    def is_satisfied_by(other):
        def x():
            pass
        return other.__class__ == x.__class__
