# from Cryptodome.Cipher import ARC4
# from base64 import b64encode
# key = b"shaoshuai"
# cip = ARC4.new(key)
# after = cip.encrypt("I'm ss".encode())
# cip = ARC4.new(key)
# before = cip.decrypt(after)


def rc4_crypt(key, data):
    def rc4_init(key):  # 256 == 0xff
        s_box = [i for i in range(256)]
        k_box = [ord(key[i % len(key)]) for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + s_box[i] + k_box[i]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
        return s_box
    s_box = rc4_init(key)
    data = list(data)
    i, j, t = 0, 0, 0
    for k in range(len(data)):
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        data[k] ^= s_box[t]
    return bytes(data)

#
# import time
# import functools
# def clock(func):
#     @functools.wraps(func)
#     def clocked(*args, **kwargs):
#         t0 = time.perf_counter()
#         result = func(*args)
#         elapsed = time.perf_counter() - t0
#         name = func.__name__
#         arg_str = ','.join(repr(arg) for arg in args)
#         kwargs_str = ','.join('%s=%r' % (k, v) for k,v in sorted(kwargs))
#
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str+','+kwargs_str, result))
#         return result
#     return clocked
#
# str = """有不少的回答认为这个问题非常搞笑，提出的说法包括“我们会接触到外语”，
# “人可以模仿不熟悉的读音”等等。但是，我提一个问题大家思考。很多中国人，甚至是旅居国外多年操流利的英语的人士，
# 仍旧把that读作zat或tsat，相应的很多南亚和东南亚的人士把that读作dat。在这里“我们会接触到外语”、
# “人可以模仿不熟悉的读音”这两条为什么就不起作用了呢？实际上，题主的这个问题，并不搞笑，我觉得写一个学士学位论文是足够了的。
# 它至少涉及两个问题：汉语普通话音系结构、第二语言习得中的语音处理。我下面的回答主要针对普通话音系结构来简单说一下。
# 我们从小学习的汉语拼音，其实质是将普通话音系拆成声母、韵母（包括介母）、声调三个部分归类学习，然后再由三个部分组合成普通话语音。
# 但是如果我们把这三个元素列成表格的话，我们会发现，并不总是能够填满表格。那些缺失的地方就是普通话音系中不使用的音节。
# 我们以bpmf、zcs及两组鼻音韵母为例：
#
# 作者：付佳杰
# 链接：https://www.zhihu.com/question/48461515/answer/371872696
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。"
# """
# @clock
# def test_Cryptodome():
#     key = b"shaoshuai"
#     cip = ARC4.new(key)
#     after = cip.encrypt(str.encode())
#     cip = ARC4.new(key)
#     before = cip.decrypt(after)
#     print(before)
#
# @clock
# def test_myrc4():
#     a = rc4_crypt(b"shaoshuai", str.encode())
#     b = rc4_crypt(b"shaoshuai", a)
#     print(b)
#
# if __name__ == '__main__':
#     test_Cryptodome()
#     test_myrc4()
#     """
#     使用库会快很多
#     """