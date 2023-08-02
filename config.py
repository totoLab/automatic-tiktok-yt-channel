import json
import os

def update_compilation_db(db_path, category):
    d = {}
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            d = json.load(f)

    if "limit" not in d:
        d["limit"] = 5
    limit = int(d["limit"])

    if "tmpFile" not in d:
        d["tmpFile"] = "service_files/tmpFile.json"
    tmpFile = d["tmpFile"]

    if "compilations" not in d:
        d["compilations"] = {"number": 0}
    dd = d["compilations"]

    if category not in dd:
        print("Category doesn't exists in db.")
        sys.exit()
    ddd = dd[category]

    if "url" not in ddd:
        print(f"Url doesn't exists in {category=}.")
        sys.exit()
    url = ddd["url"]

    if "number" not in dd[category]:
        ddd["number"] = 0

    compilation_number = int(ddd["number"]) + 1
    ddd["number"] = compilation_number

    folder_path = os.path.dirname(db_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(db_path, "w") as f:
        json.dump(d, f, indent=4)

    return limit, tmpFile, url, compilation_number

if __name__ == "__main__":
    update_compilation_db("service_files/config.json", "test")