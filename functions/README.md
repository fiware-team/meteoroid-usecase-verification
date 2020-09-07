# Meteoroid Functions

本ユースケース検証で開発した Function は下記の2つである。

1. Signage Controller Function (signage-controller.py)
2. Aggregation Function (aggregation.py)

## 1.Signage Controller (signage-controller.py)

Signage Controller Function は、Analysis Entity の更新通知を Orion から受け取ることによって実行されるイベントドリブンファンクションである。
Analysis に含まれる検出された人物IDをもとに年齢情報を含む Person Entity を Orion から取得し、年齢に応じた広告コンテンツを表示するためサイネージ API を制御する。

### Meteoroid への設定方法

```bash
meteoroid function create SignageController singnage-controller.py --language python:3
+---------------------+---------------------------------+
| Field               | Value                           |
+---------------------+---------------------------------+
| id                  | 1                               |
| code                |                                 |
| language            | python:3                        |
| binary              | False                           |
| main                |                                 |
| version             | 0.0.1                           |
| parameters          | []                              |
| fiware_service      |                                 |
| fiware_service_path | /                               |
| name                | SignageController               |
+---------------------+---------------------------------+
```

```bash
meteoroid endpoint create signage /update post 1
+---------------------+-------------------------------------------------------------------------------------+
| Field               | Value                                                                               |
+---------------------+-------------------------------------------------------------------------------------+
| id                  | 1                                                                                   |
| url                 | https://192.168.28.10:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/signage/update |
| fiware_service      |                                                                                     |
| fiware_service_path | /                                                                                   |
| name                | signage                                                                             |
| path                | /update                                                                             |
| method              | post                                                                                |
| function            | 1                                                                                   |
+---------------------+-------------------------------------------------------------------------------------+
```

```bash
meteoroid subscription create 1 '
{
    "description": "Meteoroid Subscription",
    "subject": {
        "entities": [
            {
                "idPattern": ".*",
                "type": "Analysis"
            }
        ],
        "condition": {
            "expression": {
                "q": "numberOfDetectedPerson>0"
            }
        }
    },
    "notification": {
    },
    "expires": "2040-01-01T14:00:00.00Z",
    "throttling": 1
}'
+-----------------------+--------------------------+
| Field                 | Value                    |
+-----------------------+--------------------------+
| id                    | 1                        |
| fiware_service        |                          |
| fiware_service_path   | /                        |
| endpoint_id           | 2                        |
| orion_subscription_id | 5f51a52bd9d315f846e98fd4 |
+-----------------------+--------------------------+
```

## 2.Aggregation (aggregation.py)

Aggregation Function は、1日の年代別入場者数を1日1回集計する定期実行ファンクションである。
FIWARE の 時系列データベースである Quantum Leap から前日の00時00分00秒から23時59分59秒までの Analysis データを取得し年代別入場者数を集計する。

### Meteoroid への設定方法

```bash
meteoroid function create Aggregation aggregation.py
+---------------------+----------------+
| Field               | Value          |
+---------------------+----------------+
| id                  | 2              |
| code                |                |
| language            | python:default |
| binary              | False          |
| main                |                |
| version             | 0.0.1          |
| parameters          | []             |
| fiware_service      |                |
| fiware_service_path | /              |
| name                | Aggregation    |
+---------------------+----------------+
```

```bash
meteoroid schedule create Aggregation "30 0 * * *" 2
+-----------------+-------------+
| Field           | Value       |
+-----------------+-------------+
| name            | Aggregation |
| schedule        | 30 0 * * *  |
| function        | 2           |
| trigger_payload |             |
| startDate       |             |
| stopDate        |             |
| id              | 1           |
+-----------------+-------------+
```
