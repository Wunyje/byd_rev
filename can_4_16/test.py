wide_dic = {}
for i in range(4):
    temp_dic = wide_dic.setdefault(i, {})
    for j in range(5):
        temp_dic[j] = 1

print(wide_dic)
print(len(wide_dic))
print(len(wide_dic[2]))
print(len(temp_dic))