#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

# 自定义自动更改scrapy提取代码，省去部分重复劳动时间(和item.py同一目录)
###################################################################################
# 自定义提取信息
infos = ['url', 'title', 'pic_url']
# 自定义xpath规则
rules = ['//*[@id="content"]/h1/span[1]/text()', '//*[@id="content"]/h1/span[1]/text()',
         '//*[@id="content"]/h1/span[1]/text()']
# 自定义更改的文件
filename = ['mymodel.txt', 'items.py', 'spiders/douban.py']

# 查找标志
item_sign = ['# 001']
spider_sign = ['# 001', '# 002']
model_sign = ['##001', '##002', '##003', '##004']
mymodel_sign = ['{info}', '{rule}']
###################################################################################
for info, rule in zip(infos, rules):

    # 提取model里的格式模板
    with open(filename[0], 'r+', encoding='utf-8') as file_model:
        list_model = file_model.readlines()
        new_model = []

        n1 = n2 = n3 = n4 = 0
        for line in list_model:
            if model_sign[0] in line:
                n1 = list_model.index(line)
            elif model_sign[1] in line:
                n2 = list_model.index(line)
            elif model_sign[2] in line:
                n3 = list_model.index(line)
            elif model_sign[3] in line:
                n4 = list_model.index(line)

            # 使用给定的变量替换
            if mymodel_sign[0] in line:
                line = line.replace(mymodel_sign[0], info)
            if mymodel_sign[1] in line:
                line = line.replace(mymodel_sign[1], rule)
            new_model.append(line)
        style1 = new_model[n1 + 1:n2]
        style2 = new_model[n2 + 1:n3]
        style3 = new_model[n3 + 1:n4]

    # 更改item.py
    with open(filename[1], 'r+', encoding='utf-8') as file_item:
        list_item = file_item.readlines()
        n = 0
        # 找到标志行
        for line in list_item:
            if item_sign[0] in line:
                n = list_item.index(line)
        # 将style1中的格式插入
        for x in style1:
            list_item.insert(n, x)
            n += 1
        # 将列表按行写入文件
        with open(filename[1], 'w+', encoding='utf-8') as ffile_item:
            ffile_item.writelines(list_item)

    # 更改spider.py
    with open(filename[2], 'r+', encoding='utf-8') as file_spider:
        list_spider = file_spider.readlines()
        m1 = m2 = 0
        # 找到标志行
        for line in list_spider:
            if spider_sign[0] in line:
                m1 = list_spider.index(line)
            if spider_sign[1] in line:
                m2 = list_spider.index(line)
        # 将style1中的格式插入
        for x in style2:
            list_spider.insert(m1, x)
            m1 += 1
            m2 += 1
        for y in style3:
            list_spider.insert(m2, y)
            m2 += 1
        # 将列表按行写入文件
        with open(filename[2], 'w+', encoding='utf-8') as ffile_spider:
            ffile_spider.writelines(list_spider)
