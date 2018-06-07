#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import execjs
import time
import copy
import random

js1 = """
        function numberTransfer(a) {
            for (var b = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$^!|",
            c = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$", d = 65, e = "!", f = "^", 
            g = a < 0 ? f: "", a = Math.abs(a), h = parseInt(a / d), i = [a % d]; h;) g += e,
            i.push(h % d),
            h = parseInt(h / d);
            for (var j = i.length - 1; j >= 0; j--) g += 0 == j ? c.charAt(i[j]) : c.charAt(i[j] - 1);
            return a < 0 && (g = f + g),
            g
        }
        """


def run_js1(a):
    c = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$"
    d = 65
    e = "!"
    f = "^"
    g = "^" if a < 0 else ""
    a = abs(a)
    h = int(a / d)
    i = [a % d]
    while 1:
        if h == 0:
            break
        g += e
        i.append(h % d)
        h = int(h / d)
    for j in list(range(len(i)))[::-1]:
        g += list(c)[i[j]] if j == 0 else list(c)[i[j] - 1]
    return g


# n = 999999999
# ctx1 = execjs.compile(js1)
# print(ctx1.call('numberTransfer', -n))
# print(ctx1.call('numberTransfer', n))
# print(run_js1(-n))
# print(run_js1(n))

js2 = '''
        function arrTransfer(a) {
            for (var b = [a[0]], c = 0; c < a.length - 1; c++) {
                for (var d = [], e = 0; e < a[c].length; e++) 
                d.push(a[c + 1][e] - a[c][e]);
            b.push(d)
            }
            return b
        }
        '''


def run_js2(a):
    b = [a[0]]
    for c in range(len(a) - 1):
        d = []
        for e in range(len(a[c])):
            d.append(a[c + 1][e] - a[c][e])
        b.append(d)
    return b


js3 = """ function encode2(a, b) {
            for (var c = b.length - 2,
            d = b.slice(c), e = [], f = 0; f < d.length; f++) {
                var g = d.charCodeAt(f);
                e[f] = g > 57 ? g - 87 : g - 48
            }
            d = c * e[0] + e[1];
            var h, i = parseInt(a) + d,
            j = b.slice(0, c),
            k = [20, 50, 200, 500],
            l = [],
            m = {},
            n = 0;
            f = 0;
            for (var o in k) l.push([]);
            for (var p = j.length; p > f; f++) h = j.charAt(f),
            m[h] || (m[h] = 1, l[n].push(h), n++, n == l.length && (n = 0));
            for (var q, r = i,
            s = "",
            t = k.length - 1; r > 0 && !(t < 0);) r - k[t] >= 0 ? (q = parseInt(Math.random() * l[t].length), s += l[t][q], r -= k[t]) : t -= 1;
            return s
        }
        """


def encode_js(a):
    # ctx1 = execjs.compile(js1)
    # ctx2 = execjs.compile(js2)
    # c = ctx2.call('arrTransfer', a)
    c = run_js2(a)
    b = '|'
    d = []
    e = []
    f = []
    for g in range(len(c)):
        d.append(run_js1(c[g][0]))
        e.append(run_js1(c[g][1]))
        f.append(run_js1(c[g][2]))
        # d.append(ctx1.call('numberTransfer', c[g][0]))
        # e.append(ctx1.call('numberTransfer', c[g][1]))
        # f.append(ctx1.call('numberTransfer', c[g][2]))
    return ''.join(d) + b + ''.join(e) + b + ''.join(f)


def move(start, end, m):
    """移动小步"""
    n = 20
    for i in range(1, n + 1):
        x = (end[0] - start[0]) / n
        y = (end[1] - start[1]) / n
        if len(m) == 0:
            m.append([int(start[0] + x * i), int(start[1] + y * i), 100])
            time.sleep(100 / 1000)
        else:
            tt = random.randint(10, 20)
            m.append([int(start[0] + x * i), int(start[1] + y * i), m[-1][2] + tt])
            time.sleep(tt / 1000)
    return m


# data_str = '23,29,1528382293041,26,29,54,32,29,69,45,29,79,54,29,92,60,29,102,67,29,110,74,31,118,78,31,125,83,31,134,88,31,143,93,31,152,113,32,193,122,32,215,123,32,227,125,32,236,128,32,247,129,32,256,131,32,291,132,32,297,132,34,484,131,36,493,129,40,504,125,42,514,124,43,523,118,48,530,112,54,539,107,56,548,96,63,559,90,69,568,87,72,578,83,74,587,77,78,605,74,79,613,72,82,623,69,84,630,67,86,640,66,90,660,62,92,670,62,93,679,60,96,689,58,97,701,57,98,711,57,100,726,56,101,734,55,102,741,53,103,751,52,105,762,50,106,774,47,107,785,41,114,813,40,116,821,38,117,888,37,118,905,39,118,1104,44,118,1113,49,118,1123,54,118,1131,62,119,1143,68,119,1152,75,119,1160,82,119,1167,88,119,1175,92,119,1184,105,119,1213,113,119,1222,116,119,1230,118,119,1237,122,119,1246,123,119,1253,124,119,1261,129,119,1279,131,119,1319,131,119,1469'
# data_str = '28,27,1528037390715,28,29,57,31,29,74,33,29,84,37,29,93,41,29,104,49,29,115,53,29,124,56,29,133,58,29,142,65,29,152,73,27,164,78,27,172,84,27,183,91,27,190,107,27,225,113,27,236,116,27,247,118,27,255,120,26,263,124,26,281,125,26,289,126,26,308,126,26,518'
# data_str = '28,27,1528037390716,28,29,57,31,29,74,33,29,84,37,29,93,41,29,104,49,29,115,53,29,124,56,29,133,58,29,142,65,29,152,73,27,164,78,27,172,84,27,183,91,27,190,107,27,225,113,27,236,116,27,247,118,27,255,120,26,263,124,26,281,125,26,289,126,26,308,126,26,518'
# data_str = '28,23,1528382538602,29,23,60,31,23,79,42,23,87,57,24,99,66,24,110,70,24,121,83,24,131,90,24,142,97,24,150,117,25,185,123,25,197,136,25,207,141,25,217,146,25,226,151,25,241,154,25,249,154,25,347'
# data_str = '133,27,1528383354930,131,33,77,131,35,89,130,47,101,130,49,110,129,55,117,129,60,125,127,65,133,127,70,152,125,73,159,125,75,168,125,82,175,125,88,183,125,90,190,125,94,198,125,102,206,125,116,229,125,122,241,125,125,253,125,126,264,125,129,274,125,131,285,125,132,317,125,132,336'
# data_list = data_str.split(',')
# data = []
# for i in range(len(data_list)):
#     if i % 3 == 0:
#         data.append([int(data_list[i]), int(data_list[i + 1]), int(data_list[i + 2])])
# print(data)
# result = encode_js(data)
# print(result)


def get_data_env(x):
    data_dict = {}
    data_dict['1'] = [30, 30]
    data_dict['2'] = [130, 30]
    data_dict['3'] = [30, 130]
    data_dict['4'] = [130, 130]
    # l = ['1234', '1243', '1324', '1342', '1423', '1432',
    #      '2134', '2143', '2341', '2314', '2413', '2431',
    #      '3124', '3142', '3214', '3241', '3421', '3412',
    #      '4123', '4132', '4213', '4231', '4321', '4312',
    #      ]
    # for x in l:
    d1 = data_dict[list(x)[0]]
    d2 = data_dict[list(x)[1]]
    d3 = data_dict[list(x)[2]]
    d4 = data_dict[list(x)[3]]
    f1 = copy.deepcopy(d1)
    f1.append(int(time.time() * 1000))
    m = []

    m = move(d1, d2, m)
    m = move(d2, d3, m)
    m = move(d3, d4, m)
    n = [83, 170, 258, 345, 431, 520, 630, 743, 854, 973, 1083, 1195, 1299, 1394, 1480, 1578, 1675, 1770, 1863, 1960,
         2053, 2146, 2238, 2325, 2413, 2496, 2584, 2672, 2759, 2872, 2984, 3096, 3208, 3322, 3428, 3525, 3613, 3699,
         3785, 3876, 3963, 4050, 4140, 4226, 4312, 4398, 4486, 4575, 4666, 4752, 4867, 4979, 5082, 5192, 5299, 5386,
         5477, 5565, 5653]
    m.pop()
    m = [[x[0], x[1], y] for x, y in zip(m, n)]
    m.insert(0, f1)
    # print(m)
    data_enc = encode_js(m)
    return data_enc


# k = get_data_env('1234')
# print(k)
def run_js3(b, id):
    ctx3 = execjs.compile(js3)
    path_enc = ctx3.call('encode2', str(b), id)
    return path_enc

# get_data_env('1234')
