#!/usr/bin/env python3
import json

latest_attempts = {}

with open("payments.jsonl", "r") as f:
  for line in f:
    line = line.strip()
    if not line:
      continue
    try:
      event = json.loads(line)
    except json.JSONDecodeError:
      continue

    if "txn_id" not in event or not event["txn_id"]:
      continue

    txn_id = event["txn_id"]
    ts = event.get("ts", "")

    if txn_id not in latest_attempts or ts > latest_attempts[txn_id].get(
        "ts", ""
    ):
      latest_attempts[txn_id] = event

total = 0.0
count = 0

for event in latest_attempts.values():
  if event.get("status") == "success":
    try:
      amount_str = str(event.get("amount", "0")).replace(",", "")
      total += float(amount_str)
      count += 1
    except (ValueError, TypeError):
      continue

with open("expected.txt", "r") as f:
  expected = int(f.read().strip())

if count != expected:
  print(
      f"Check failed: counted {count} successful payments, expected"
      f" {expected}."
  )
else:
  print(f"Check passed: {count} successful payments.")
  print(f"Your code: KOYA-{round(total)}")