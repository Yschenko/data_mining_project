import numpy as np
import pandas as pd
import requests
import json

REINA_DEL_CID_ARID = "bc2c7b91-c881-4088-81bd-2e041b024341"
JOHN_MAYER_ARID = "144ef525-85e9-40c3-8335-02c32d0861f3"
GEORGE_HARRISON_ARID = "42a8f507-8412-4611-854f-926571049fa0"


def songs_data_of_artist(artist_id):
    url = f"https://musicbrainz.org/ws/2/recording?query=arid:{artist_id}"
    JSONContent = requests.get(url, headers={"Accept": "application/json"})
    content = json.dumps(JSONContent.json(), indent=4, sort_keys=True)

    rec_ids_titles = {}
    records_ids = []
    titles = []
    for r in json.loads(content)['recordings']:
        records_ids.append(r['id'])
        titles.append(r['title'])
        rec_ids_titles[r['id']] = r['title']

    records_ids = ";".join(records_ids)

    url = f"https://acousticbrainz.org/api/v1/low-level?recording_ids={records_ids}&features=rhythm.bpm;rhythm" \
          f".danceability;tonal.key_key" \
          f";tonal.key_scale"
    JSONContent = requests.get(url, headers={"Accept": "application/json"})
    content = json.dumps(JSONContent.json(), indent=4, sort_keys=True)

    records_info = json.loads(content)
    records_info.popitem()
    ids = records_info.keys()
    titles = [rec_ids_titles[x] for x in ids]
    records_info = records_info.values()
    records_list = []
    for r in records_info:
        rhythm = r["0"]["rhythm"]
        tonal = r["0"]["tonal"]
        records_list.append([rhythm["bpm"], rhythm["danceability"], tonal["key_key"], tonal["key_scale"]])

    df1 = pd.DataFrame(titles, columns=['title'])
    df2 = pd.DataFrame(records_list, columns=['bpm', 'danceability', 'key', 'scale'])
    result = pd.concat([df1, df2], axis=1)
    return result


def main():
    print(songs_data_of_artist(GEORGE_HARRISON_ARID))


if __name__ == '__main__':
    main()
