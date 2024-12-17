from script import Computer

def test_1():
    c = Computer([2, 6], 0, 0, 9)
    c.run()
    assert c.reg_b == 1

def test_2():
    c = Computer([5, 0, 5, 1, 5, 4], 10, 0, 0)
    c.run()
    assert c.outputs == [0, 1, 2]

def test_3():
    c = Computer([0, 1, 5, 4, 3, 0], 2024, 0, 0)
    c.run()
    assert c.outputs == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert c.reg_a == 0

def test_4():
    c = Computer([1, 7], 0, 29, 0)
    c.run()
    assert c.reg_b == 26

def test_5():
    c = Computer([4, 0], 0, 2024, 43690)
    c.run()
    assert c.reg_b == 44354
