# ClassSpy
Python tool for inspecting object side effects

Some times you have code that uses a python object as a central data structure to complete a complicated calculation. We all know we shouldn't have code with side effects, but sometimes we do it on accident. Class spy is a tool that allows you to see how variables within the datastore are connected, allowing you to find unintentional coupling and other difficult to debug issues. This project was conceived because I inherited a large project that followed this pattern and was tasked to clean it up. The generated graph for this project looked a little like this:

![complicated.png](https://github.com/mudkipmaster/ClassSpy/raw/master/readmeImages/complex.png)

Obviously this is an extreme example, but for a simpler example consider the following code:

```
test.bar = 2
test.foo = 5
test.bar = test.foo + 1
test.fizz = 10
test.foo = test.fizz + test.bar
test.fizz *= 10
test.buzz = test.fizz
```

Already this starts to get confusing. To analyze this using ClassSpy, simply modify the class of `test` so that it extends `ClassSpy` and add a few extra lines to your code which results in this:

![simple.png](https://github.com/mudkipmaster/ClassSpy/raw/master/readmeImages/simple.png)

This example code can be found in `test.py`

## Limitations
This tool uses line numbers and file names to determin whether a get and set are related, this means that if an assignment spans multiple lines it will not be correctly identified. Additionally in the case of variables that are set within if statements that are dependent on other variables, this relation will also not be captured. This feature is something I would like to add in the future
