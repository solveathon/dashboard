import csv
import json

file = open('responses.csv', 'r', encoding='utf-8')

reader = csv.reader(file)

format = {
  "data": [
  ]
}

# Create a json file based on the given format
# ID number is increased by 1 for each row

id_counter = 1

for row in reader:
    format['data'].append({
        "id": id_counter,
        "team_name": f"Team {row[-1]}",
        "table_no": row[1],
        "team_leader": row[3],
        "campus": "VIT Chennai",
        "total_points": "0",
        "status": "Pending",
        "image": ""
    })
    id_counter += 1
# Write the json data to a file
with open('dataFinal.json', 'w') as json_file:
    json.dump(format, json_file)