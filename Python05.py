# 元编程（在运行时改变程序的行为）
# 7.1　装饰器基础知识
# 装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）,装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象。
# 装饰器的一大特性是，能把被装饰的函数替换成其他函数。第二个特性是，装饰器在加载模块时立即执行。
#
registry = []
def reg(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func
@reg
def fun1():
    print('running fun1()')
@reg
def fun2():
    print('running fun2()')
def fun3():
    print('running fun3()')

def main():
    print('running main()')
    print('registry ->', registry)
    fun1()
    fun2()
    fun3()

# main()
''' 
注意，register 在模块中其他函数之前运行（两次）。调用 register 时，传给它的参数是被装饰的函数。
函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。比如在Python04中import Python05时，注销掉main()，
任然会输出：
    running register(<function fun1 at 0x000002325B9AF760>)
    running register(<function fun2 at 0x000002325B9AF7F0>)
运行结果：
    running register(<function fun1 at 0x000001D34A19A200>)
    running register(<function fun2 at 0x000001D34A19A4D0>)
    running main()
    registry -> [<function fun1 at 0x000001D34A19A200>, <function fun2 at 0x000001D34A19A4D0>]
    running fun1()
    running fun2()
    running fun3()

装饰器函数与被装饰的函数在同一个模块中定义。实际情况是，装饰器通常在一个模块中定义，然后应用到其他模块中的函数上。
reg装饰器返回的函数与通过参数传入的相同。实际上，大多数装饰器会在内部定义一个函数，然后将其返回。

'''

# 7.4　变量作用域规则
# b = 6
# def funb(a):
#     print(a)
#     print(b)
# funb(3)  # 3  6

b1 = 6
def funb1(a):
    global b1
    print(a)
    print(b1)
    b1=9
funb1(3) # 3  6
print(b1) # 9