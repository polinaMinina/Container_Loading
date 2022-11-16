from py3dbp import Packer, Bin, Item

import json
import copy
from pprint import pprint

# import time
# start_time = time.time()

pprint(1130)

from sys import argv
script, path = argv
out_file_name = path[path.rfind('/')+1:]

class Cargo_group:

    def __init__(self, mass, size, count, cargo_id):
        self.mass = mass
        self.size = size
        self.count = count
        self.cargo_id = cargo_id

    def get_cargo_param(self, kind='height'):
        if kind == 'length':
            return int(self.size[1])
        elif kind == 'width':
            return int(self.size[0])
        elif kind == 'height':
            return int(self.size[2])
        elif kind == 'weight':
            return int(int(self.mass))
        elif kind == 'count':
            return int(self.count)
        else:
            raise ValueError("Разрешено только [length, width, height, value, instance]")


def get_cargo_size(data):  # получает размер контейнера в трех измерениях (длина, ширина, высота ) из t файла
    cargo_size_data = data['cargo_space']['size']
    return [int(cargo_size_data['width']), int(cargo_size_data['length']), int(cargo_size_data['height'])]

def get_cargo_mass(data):  # получает размер контейнера в трех измерениях (длина, ширина, высота ) из json файла
    cargo_mass_data = data['cargo_space']['mass']
    return int(cargo_mass_data)

def get_cargo_carrying_capacity(data):
    cargo_cp_data = data['cargo_space']['carrying_capacity']
    return int(cargo_cp_data)

def get_cargo_groups(data):  # заносит все виды ящиков в список с элементами класса Cargo_group
    cargo_groups = []
    for i in data['cargo_groups']:
        mass = int(i['mass'])
        size = [int(i['size']['length']), int(i['size']['width']), int(i['size']['height'])]
        count = int(i['count'])
        cargo_id = str(i['group_id'])

        cg = Cargo_group(mass, size, count, cargo_id)
        cargo_groups.append(cg)
    return cargo_groups


with open(path) as f:
    data = json.load(f)

cargo_size_data = get_cargo_size(data)
cargos = get_cargo_groups(data)

packer = Packer()

a = Bin('box', cargo_size_data[1], cargo_size_data[0], cargo_size_data[2], 100000000000)
packer.add_bin(a)

cnt = 0
for item in cargos:
    for cargo in range(item.count):
        cnt += 1
        packer.add_item(Item(str(cnt), item.get_cargo_param('width'), item.get_cargo_param('length'), item.get_cargo_param('height'), item.get_cargo_param('weight'), item.cargo_id))
        packer.pack()


volume_used = 0
total_weight = 0
volume_not_used = 0

cargo_default_text = {
    "sort": 1,
    "stacking": True,
    "turnover": True,
    "type": "box"
}
packed_cargos = {}

for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    count = 0

    for item in b.items:
        count+=1
        print("====> ", item.string())
        volume_used += item.get_volume()
        total_weight += item.weight
        #cnt += 1
        posit = [0, 0, 0]
        posit[0] = (item.position[0] + item.dimension[0]) / 2
        posit[1] = (item.position[1] + item.dimension[1]) / 2
        posit[2] = (item.position[2] + item.dimension[2]) / 2

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())
        volume_not_used += item.get_volume()
        #cnt += 1

    print("***************************************************")
    print("***************************************************")

volume = cargo_size_data[0] * cargo_size_data[1] * cargo_size_data[2]
print("ЗАполненность:", volume_used / volume * 100)
#print(total_weight)
#print(volume_used)
print(volume_not_used)
volume_left = volume - volume_used
print(volume_left)
#print(volume)
#print(volume_used + volume_not_used)


# TO JSON
import nums_from_string

output_info = {
    'cargoSpace':
        {
            'loading_size':
                {
                    'width': (int(b.string().split('x')[1].split('(')[1]) / 1000),
                    'length': (int(b.string().split('x')[2]) / 1000),
                    'height': (int(b.string().split('x')[3].split(',')[0]) / 1000)
                },

            'position':
                [
                    (int(b.string().split('x')[2]) / 1000) / 2,
                    (int(b.string().split('x')[3].split(',')[0]) / 1000) / 2,
                    (int(b.string().split('x')[1].split('(')[1]) / 1000) / 2

                ],
            'type': 'pallet'
        },
    'cargos': [
    ],
    'unpacked': []
}

for b in packer.bins:
    for item in b.items:
        output_info['cargos'].append({
            "calculated_size": {
                "height": int(item.dimension[2]) / 1000,
                "length": int(item.dimension[1]) / 1000,
                "width": int(item.dimension[0]) / 1000
            },
            "cargo_id": item.cargo_id,
            "id": int(item.string().split('(')[0]),
            "mas": item.string().split('x')[2].split(',')[0],
            "position": {
                "x": (int(item.position[1]) + int(item.dimension[1]) / 2) / 1000,
                "y": (int(item.position[2]) + int(item.dimension[2]) / 2) / 1000,
                "z": (int(item.position[0]) + int(item.dimension[0]) / 2) / 1000
            },
            "size": {
                "height": int(item.dimension[2]) / 1000,
                "length": int(item.dimension[1]) / 1000,
                "width": int(item.dimension[0]) / 1000
            },
            "sort": 1,
            "stacking": "True",
            "turnover": "True",
            "type": "box"

        })



for b in packer.bins:
    for item in b.unfitted_items:
        output_info['unpacked'].append({
            "group_id": 1,
            "id": int(item.string().split('(')[0]),
            "mass": item.string().split('x')[2].split(',')[0],
            "position": {
                "x": -5,
                "y": 0.5,
                "z": -5
            },
            "size": {
                "height": int(item.string().split('x')[0].split('(')[1]) / 1000,
                "length": int(item.string().split('x')[2].split(',')[0]) / 1000,
                "width": int(item.string().split('x')[1]) / 1000
            },
            "sort": 1,
            "stacking": "True",
            "turnover": "True",
        })
'''
output_info['unpacked'].append(
    {
        "sort": 1,
        "stacking": "True",
        "turnover": "True",
    })
'''
pprint(output_info)
with open('output/'+out_file_name, "w", encoding='utf-8') as f:
    json.dump(output_info, f, ensure_ascii=False, indent=4)

# print("--- %s seconds ---" % (time.time() - start_time))