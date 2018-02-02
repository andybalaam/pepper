def type_check(type_, instance):
    if "is_satisfied_by" in type_.__dict__:
        assert type_.is_satisfied_by(instance)
    else:
        assert instance.__class__ == type_
