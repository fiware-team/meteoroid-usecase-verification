import json
import requests


def main(params):
    """
    1.Analysisのデータを受けてPerson IDを取り出す
    2.全てのPerson IDを取得して年齢分布Listを作成する
    3.最も多い年齢に対応するImageObjectを取得する
    4.ImageObjectのURLをサイネージアプリに通知する

    Parameters
    ----------
    params : dict
        Action呼び出し時のパラメーター。SubscriptionのBodyを含む
    """

    signage_url = params['signage_url']

    # 1
    analysis = params['data'][0]
    person_ids = analysis['detectedPersons']['value']

    # 2
    age_groups = [0] * 10
    for person_id in person_ids:
        resp = requests.get(f'http://orion:1026/v2/entities/{person_id}',
                            params={"type": "Person"})
        person = resp.json()
        age = person['age']['value']
        age_groups[int(age / 10)] += 1

    # 3
    max_age_group = age_groups.index(max(age_groups))
    resp = requests.get('http://orion:1026/v2/entities/ad%02d' % max_age_group)
    image_object = resp.json()

    # 4
    body = {"url": image_object["contentUrl"]["value"]}
    headers = {'content-type': 'application/json'}
    resp = requests.post(signage_url, data=json.dumps(body), headers=headers)
    if resp.status_code == 200:
        return {"status": "ok"}
    else:
        return {"status": "ng"}


if __name__ == "__main__":
    params = {
        "signage_url": "192.168.28.200"
    }
    main(params)
