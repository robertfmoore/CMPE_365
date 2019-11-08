from heapq import *

class HuffmanNode(object):

    def __init__(self, freq, value=None, zero=None, one=None):
        self.freq = freq
        self.value = value
        self.zero = zero
        self.one = one

    def __str__(self):
        #dont need this
        string = str(self.freq) +','+ str(self.value)
        return string

    def gen_code(self,pre_code=''):
        if self.value:
            print(self.value)
            return {self.value:pre_code}
        dic = self.zero.gen_code(pre_code +'0')
        dic.update(self.one.gen_code(pre_code + '1'))
        return dic

    def __lt__(self, other):
        return self.freq < other.freq

    def __add__(self, other):
        tmp_freq = self.freq + other.freq
        return HuffmanNode(tmp_freq, zero=self, one=other)

a = [(1,1),(2,2),(3,3),(4,4),(5,8),(6,2),(7,2)]
nodes = [HuffmanNode(x[1],value=x[0]) for x in a]
heapify(nodes)

while len(nodes)>1:
    node_1 = heappop(nodes)
    node_2 = heappop(nodes)
    tmp = node_1 + node_2
    heappush(nodes,tmp)

root = heappop(nodes)

huff_code = root.gen_code()

print(huff_code)




print([str(x) for x in nodes])
