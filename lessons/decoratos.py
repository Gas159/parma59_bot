from datetime import datetime as dt

def typed(type_: [int | str]):
    def real_dec(func):
        def wrapper(*args, **kwargs):
            for arg in args:
                if not isinstance(arg, type_):
                    raise ValueError('Некорректный тип данных!')
            start = dt.now()
            result = func(*args, **kwargs)
            print(f'Time of function: {dt.now() - start}')
            return result
        return wrapper
    return real_dec

@typed(int)
def calc1(a: int, b: int) -> int:
    return a + b


# @typed(str)
def calc2(a: str, b: str) -> str:
    return a + b


calc2 = typed(str)(calc2)('a', 'b')
print(calc2)
# print(calc2)
print(calc1(1, 2))

#
# calc = real_dec(calc)
# q = calc(1,2)
# print(q)
