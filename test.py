from ClassSpy import ClassSpy

class testClass(ClassSpy):
    foo = 0
    bar = 0

if(__name__ == "__main__"):
    test = testClass()
    test.bar = 2
    test.foo = 5
    test.bar = test.foo + 1
    test.fizz = 10
    test.foo = test.fizz + test.bar
    test.fizz *= 10

    test.save_connections()
    test.plot()