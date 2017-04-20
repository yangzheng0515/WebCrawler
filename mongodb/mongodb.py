import pymongo

client = pymongo.MongoClient('localhost', 27017)
walden = client['walden']
sheet_tab = walden['sheet_tab']

# path = '/home/yz/test'
# with open(path, 'r') as f:
#     lines = f.readlines()
#     for index, line in enumerate(lines):
#         data = {
#             'index': index,
#             'line': line,
#             'words': len(line.split())
#         }
#         # print(data)
#         sheet_tab.insert(data)  # insert_one(data)

for item in sheet_tab.find():
    print(item)

# sheet_tab.find({'words': {'$ls': 5}})

