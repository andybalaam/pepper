
class Characters:
    @staticmethod
    def is_satisfied_by(other):
        try:
            iter(other)
            # TODO: check type of items?
            return True
        except:
            return False
