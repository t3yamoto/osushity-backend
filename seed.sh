#!/bin/sh

TABLE_NAME=osushity-backend-dev-sushi_chains

aws dynamodb put-item --table-name ${TABLE_NAME} --item '{"id": {"S": "kura"}, "document_url":{"S":"http://www.kura-corpo.co.jp/common/pdf/kura_allergen.pdf"}, "last_modified_at": {"S": "2019-01-01 00:00:00+0900"}, "name": {"S":"無添くら寿司"}, "parser": {"S": "KuraAllergyParser"}}'
aws dynamodb put-item --table-name ${TABLE_NAME} --item '{"id": {"S": "sushiro"}, "document_url":{"S":"http://www3.akindo-sushiro.co.jp/pdf/menu/allergy.pdf"}, "last_modified_at": {"S": "2019-01-01 00:00:00+0900"}, "name": {"S":"あきんどスシロー"}, "parser": {"S": "SushiroAllergyParser"}}'

