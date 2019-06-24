def functionA():
    print("a1")
    from test import functionB
    print("a2")
    functionB()
    print("a3")

def functionB():
    print("b")

print("t1")

class Stack:

    def __init__(self):
        self.items = []
    def Push(self,item):
        self.items.append(item)
    def Pop(self):
        return self.items.pop()
    def isEmpty(self):
        return self.items == []
    def Peek(self):
        return self.items[len(self.items)-1]


if __name__ == "__main__":
    s = Stack()
    s.Push(1)
    s.Push(2)
    s.Push(3)
    s.Push(4)
    print(s.Peek())
    print(s.Pop())

