def count_list(lst: list, aim) -> int:
    """查看指定列表中目标元素所存在的数量"""
    count = 0
    for ele in lst:
        if ele == aim:
            count = count + 1
    return count


def del_list_aim(lst: list, aim) -> list:
    """删除指定列表中的所有元素"""
    while aim in lst:
        lst.remove(aim)
    return lst
