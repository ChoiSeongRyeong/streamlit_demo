import os
import json
import pandas as pd

from icecream import ic

WORKDIR = "/app"

def getYearList()-> list:
    return ["~2002"] + [str(yyyy) for yyyy in range(2003, 2016)]

def getYearDirectoryConfig(year):
    YearDirectoryConfigPath = os.path.join(WORKDIR, f"data/result/{year}/directory.json")
    ic(YearDirectoryConfigPath)
    assert os.path.exists(YearDirectoryConfigPath)
    with open(YearDirectoryConfigPath) as f:
        YearDirectoryConfig = json.load(f)
        if YearDirectoryConfig["children"]:
            YearDirectoryConfig["dir_children_names"] = pd.DataFrame(YearDirectoryConfig["children"])["name"]
        else:
            return None
    return YearDirectoryConfig