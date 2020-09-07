import datetime as dt
import json
import requests


def main(params):
    """
    1日の年代別入場者数を集計する

    1. 1日分のAnalysisデータをQuantum Leapから取得し、人物IDのユニークなリストを作成
    2. 人物IDリストに含まれるPersonデータを取得し、年齢分布リストを作成
    3. 年代別入場者数をOrionへ登録

    Parameters
    ----------
    params : dict
        Action呼び出し時のパラメーター。OrionやQuantumLeapのIPアドレスが含まれる。
    """

    orion_host = params.get('orion_host', 'http://orion:1026')
    ql_host = params.get('ql_host', 'http://quantumleap:8668')

    # 1
    target_day = dt.datetime.now() - dt.timedelta(days=1)
    from_date = target_day.strftime("%Y-%m-%dT00:00:00")
    to_date = target_day.strftime("%Y-%m-%dT23:59:59")
    person_ids = get_unique_person_ids(ql_host, from_date, to_date)
    # 2
    age_group = [0] * 10
    for person_id in person_ids:
        person = requests.get(f'{orion_host}/v2/entities/{person_id}').json()
        if int(person["age"]["value"] / 10):
            age_group[int(person["age"]["value"] / 10)] += 1
    # 3
    data = {"id": "stadium1", "type": "DailyVisitorsByAge"}
    requests.post(f'{orion_host}/v2/entities',
                  data=json.dumps(data),
                  headers={"Content-Type": "application/json"})
    daily_visitors_by_age = {
        "10": {"type": "Number", "value": age_group[1]},
        "20": {"type": "Number", "value": age_group[2]},
        "30": {"type": "Number", "value": age_group[3]},
        "40": {"type": "Number", "value": age_group[4]},
        "50": {"type": "Number", "value": age_group[5]},
        "60": {"type": "Number", "value": age_group[6]},
        "70": {"type": "Number", "value": age_group[7]},
        "80": {"type": "Number", "value": age_group[8]},
        "90": {"type": "Number", "value": age_group[9]},
        "dateModified": {"type": "DateTime",
                         "value": dt.datetime.now().isoformat()},
        "fromDate": {"type": "DateTime", "value": from_date},
        "toDate": {"type": "DateTime", "value": to_date}
    }
    resp = requests.post(f'{orion_host}/v2/entities/stadium1/attrs',
                         data=json.dumps(daily_visitors_by_age),
                         headers={"Content-Type": "application/json"})
    if resp.status_code == 204:
        return {"status": "ok"}
    else:
        return {"status": "ng"}


def get_unique_person_ids(ql_host, from_date, to_date):
    queries = {"type": "Analysis", "fromDate": from_date, "toDate": to_date,
               "limit": 10000, "offset": 0}
    person_ids = []
    while True:
        resp = requests.get(
            f'{ql_host}/v2/entities/OOL_FA/attrs/detectedPersons/value',
            params=queries
        )
        person_ids_list = resp.json().get("values")
        if person_ids_list:
            for detected_person_ids in person_ids_list:
                for person_id in detected_person_ids:
                    if person_id:
                        person_ids.append(person_id)
            queries["offset"] += queries["limit"]
        else:
            break
    return sorted(set(person_ids), key=person_ids.index)


if __name__ == '__main__':
    params = {
        'orion_host': 'http://192.168.28.10:31026',
        'ql_host': 'http://192.168.28.10:30668'
    }
    main(params)
