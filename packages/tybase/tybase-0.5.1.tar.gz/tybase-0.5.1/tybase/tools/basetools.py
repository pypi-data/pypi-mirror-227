from math import ceil


def chunk(lst, size):
    # 列表分组,传入列表对其进行分组
    return list(
        map(lambda x: lst[x * size:x * size + size],
            list(range(0, ceil(len(lst) / size)))))
