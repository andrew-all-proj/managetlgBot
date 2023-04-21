

list_input = [("Alexander_1", "Paul_1"),
              ("Anna", "Petetr_1"),
              ("Elizabeth", "Petetr_1"),
              ("Petetr_2", "Alexei"),
              ("Petetr_3", "Anna"),
              ("Paul_1", "Petetr_3"),
              ("Alexei", "Petetr_1"),
              ("Nicolaus_1", "Paul_1")]


def find_couple(find, list_input):
    count = 1
    ch = 0
    leng = len(list_input)
    while True:
        if find == list_input[ch][0]:
            count = count + 1
            find = list_input[ch][1]
            ch = 0
        ch = ch + 1
        if ch == leng:
            break
    return count

def find(list_input):
    dict_res = {}
    for couple in list_input:
        count = find_couple(couple[1], list_input)
        dict_res[couple[0]] = count
    return dict_res

result_dic = find(list_input)
for i in sorted(result_dic):
    print(i, result_dic[i])



