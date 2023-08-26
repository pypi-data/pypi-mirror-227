"""这是一个打印出全部数组内容的模块.
我们可以通过设置数组去调用该模块中的打印函数"""


def print_lol(the_first, indent=False, level=0):
    # 通过循环递归去判断是否是list数组去无限打印每个结果
    for each_item in the_first:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)


def print_file(filename='/tmp/speaker.txt'):
    """读取文件对话内容，并处理加工后打印出来。"""
    newdata = []
    fp = None

    try:
        data = open(filename)

        for each in data:
            try:
                (role, line_spoken) = each.split(':', 1)
                print(role, end='')
                print(' said: ', end='')
                print(line_spoken, end='')
                newdata.append(role+' said: '+line_spoken)
            except ValueError:
                pass

        data.close()
    except IOError:
        print('The data file is missing!')

    try:
        fp = open(filename+'.bak', 'w')
        for eachdata in newdata:
            print(eachdata, end='', file=fp)
    except IOError:
        print('File error!')
    finally:
        fp.close()
