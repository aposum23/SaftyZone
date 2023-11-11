import os

result_dir =""
cur_dir = f'D:/dataset/cameras/'
items = os.listdir(cur_dir)
print(items)
for item in items:
    if os.path.isdir(f'{cur_dir}/{item}'):
        print(f'{item}')
