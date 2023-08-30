import gevent
from gevent import monkey

monkey.patch_all()

def pytest_runtestloop(session):
    task = session.config.getoption('--runTask')
    count = session.config.getoption('--current')
    print("参数--runTask:", task)
    print("参数--current:", count)
    print("待执行的用例总数", len(session.items))
    if task == 'mod':
        # 以模块为最小的执行单位
        mod_case = {}       # ===>{模块：[...],模块2：[...]}
        # 遍历所有的测试用例
        for item in session.items:
            # 获取用例的模块信息
            mod = item.module
            # 判断mod_case这个字典中是否有该模块
            if mod_case.get(mod):
                # 将用例添加到模块对应的列表中
                mod_case[mod].append(item)
            else:
                # 将模块作为key保存到mod_case中，对应的值设为空列表
                mod_case[mod] = []
                # 再将用例加入到列表中
                mod_case[mod].append(item)
        print(mod_case.values())
        # 有多少个模块开多少个协程
        gs = []
        for mod_test_case in mod_case.values():
            g = gevent.spawn(run_task, mod_test_case)
            gs.append(g)
        gevent.joinall(gs)
    else:
        # 以用例为最小的执行单位
        case_list = session.items
        gs = []
        # 根据参数，创建对应数量的协程
        for i in range(count):
            g = gevent.spawn(run_task, case_list)
            gs.append(g)
        gevent.joinall(gs)
    return True


def run_task(items):
    # 判断用例列表是否为空
    while items:
        # 获取一条用例
        item = items.pop()
        # 执行用例
        item.ihook.pytest_runtest_protocol(item=item, nextitem=None)


def pytest_addoption(parser):
    """添加参数名称"""
    # 添加参数分组
    group = parser.getgroup('pytest-henry')
    # 添加参数和帮助信息
    group.addoption('--runTask', default=None, help='并发执行的任务单位', type="string")
    group.addoption('--current', default=None, help='运行的并发数量', type="int")
