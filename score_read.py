import json
import os
async def all_score_read():
        if("personal_score.json" not in os.listdir()):
            with open("../personal_score.json", "w") as w:
                w.write("{}")
        with open("../personal_score.json", 'r') as r:
            data = json.load(r)
        return data
async def sort_score():
    data = await all_score_read()
    data = dict(sorted(data.items(), key=lambda x: x[1]["personal score"], reverse=True))
    with open("../personal_score.json", "w") as w:
        json.dump(data, w)
    return 0
