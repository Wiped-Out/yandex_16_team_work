import json

# ready_data = ''
# with open('persons_data.json', 'r') as file:
#     data = json.load(file)
#     data['items'] = data['items'][::3]
#     for index, item in enumerate(data['items']):
#         item.pop('role')
#         item.pop('film_ids')
#         data['items'][index] = item
#     ready_data = json.dumps(data)
# with open('persons_data.json', 'w') as file:
#     file.write(ready_data)

with open('persons_data.json', 'r') as file:
    data = json.load(file)
    data = json.dumps(data)
    ready_data = data.replace('uuid', 'id')

with open('persons_data.json', 'w') as file:
    file.write(ready_data)
