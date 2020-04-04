import json


def read_data():
    with open('data.json', 'r') as f:
        return json.load(f)


def write_data(my_data):
    with open('data.json', 'w') as f:
        json.dump(my_data, f)


mp = read_data()
arr = []
for i in mp.keys():
    if mp[i] < 0:
        arr.append(i)
for i in arr:
    mp.pop(i)
write_data(mp)
