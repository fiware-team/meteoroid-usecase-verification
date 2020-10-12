# Kafka Config

```bash
$ wsk trigger create KafkaTrigger -f /whisk.system/messaging/kafkaFeed -p brokers "[\"kafka-cp-kafka:9092\"]" -p topic subscription -p isJSONData true
```
