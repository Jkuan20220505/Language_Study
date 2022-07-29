# 输入和输出
# x = input()
# y = input()
# print(int(x)*int(y))

# ranks = [str(n) for n in range(2, 11)]+list('JQKA')   #属于列表list
# print(ranks)
# for a in range(len(ranks)):
#     print(ranks[a])
#
# suits = 'spades diamonds clubs hearts'.split()
# print(suits[1:3])
import matplotlib
'''
    假如一个网店制定了下述折扣规则:
    • 有 1000 或以上积分的顾客，每个订单享 5% 折扣。
    • 同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。
    • 订单中的不同商品达到 10 个或以上，享 7% 折扣。
'''
from collections import namedtuple
Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def total(self):
        return self.price * self.quantity

class Order: # 上下文
    def __init__(self, customer, cart1, promotion=None):
        self.customer = customer
        self.cart = list(cart1)
        self.promotion = promotion
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
        '''
            print(Order(....)) 等同于执行 print(Order(....).__repr__())，程序的输出结果是一样的（输出的内存地址可能不同）

            和 __init__(self) 的性质一样，Python 中的每个类都包含 __repr__() 方法，因为 object 类包含 __reper__() 方法，
            而 Python 中所有的类都直接或间接继承自 object 类。

            默认情况下，__repr__() 会返回和调用者有关的 “类名+object at+内存地址”信息。
            当然，我们还可以通过在类中重写这个方法，从而实现当输出实例化对象时，输出我们想要的信息。
            
            格式化字符串:
                基本语法是通过 {} 和 : 来代替以前的 %。format 函数可以接受不限个参数，位置可以不按顺序。
                print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))
            数字格式化:
                print("{:.2f}".format(3.1415926)) 输出3.14
                2.71828	  {:.0f}	3	不带小数
                '{:b}'.format(11)    1011   二进制    #b、d、o、x 分别是二进制、十进制、八进制、十六进制
                : 号后面带填充的字符，只能是一个字符，不指定则默认是用空格填充。
        '''


def fidelity_promo(order):
     """为积分为1000或以上的顾客提供5%折扣"""
     return order.total() * .05 if order.customer.fidelity >= 1000 else 0
def bulk_item_promo(order):
     """单个商品为20个或以上时提供10%折扣"""
     discount = 0
     for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
            # print(.2 * 8)
            # print(0.2 * 8)    两者效果一样
     return discount
def large_order_promo(order):
     """订单中的不同商品达到10个或以上时提供7%折扣"""
     distinct_items = {item.product for item in order.cart}
     if len(distinct_items) >= 10:
         return order.total() * .07
     return 0

# def语句最后显示函数计算结果的语句有用print的，也有用return的，def函数其实运行完return之后其实就结束了

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5),LineItem('apple', 10, 1.5),LineItem('watermellon', 5, 5.0)]
print(Order(ann, cart, fidelity_promo))  #(对象，商品，函数)
print(Order(ann, cart, bulk_item_promo))
print(Order(ann, cart, large_order_promo))

# best_promo 迭代一个函数列表，并找出折扣额度最大的
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
def best_promo(order):
    return max(promo(order) for promo in promos)
print(best_promo(Order(ann,cart)))

# 处理模块的函数: 使用 globals 函数帮助 best_promo 自动找到其他可用的 *_promo 函数，
#     1、内省模块的全局命名空间，构建 promos 列表
promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']
#     2、内省单独的 promotions 模块，构建 promos 列表

import Python05  #可以直接运行Python05.py

'''
    与上面获得promos函数列表的方案相比，这个使用@promotion装饰器的方案有几个优点:
        • 促销策略函数无需使用特殊的名称（即不用以 _promo 结尾）。
        • @promotion 装饰器突出了被装饰的函数的作用，还便于临时禁用某个促销策略：只需把
        装饰器注释掉。
        • 促销折扣策略可以在其他模块中定义，在系统中的任何地方都行，只要使用 @promotion
        装饰即可。
        
    promotion 把 promo_func 添加到 promos 列表中，然后原封不动地将其返回。
    @promotion 装饰的函数都会添加到 promos 列表中。
'''

promos1 = []
def promotion(func):
    promos1.append(func)
    return func

@promotion
def fidelity(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
def best_promo(order):
    return max(promo(order) for promo in promos1)

print(best_promo(Order(ann,cart)))