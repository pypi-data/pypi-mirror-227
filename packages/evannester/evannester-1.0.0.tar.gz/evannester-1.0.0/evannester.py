"""这是一个打印出全部数组内容的模块.
我们可以通过设置数组去调用该模块中的打印函数"""


def print_lol(the_first):
    # 通过循环递归去判断是否是list数组去无限打印每个结果
    for each_item in the_first:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
