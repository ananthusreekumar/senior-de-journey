import csv
import json
from datetime import datetime

def extract(filepath):
    print(f"[EXTRACT] Reading file:{filepath}")
    records=[]
    with open(filepath,'r') as f:
        reader=csv.DictReader(f)
        for row in reader:
            records.append(row)
    print(f"[EXTRACT] Found {len(records)} records")
    return records

def transform(records):
    print(f"[TRANSFORM] Processing {len(records)} records...")
    cleaned = []
    skipped = 0

    for record in records:
        try:
            # ← ADD THIS VALIDATION BLOCK
            if not record.get("name", "").strip():
                raise ValueError("name cannot be empty")

            cleaned_record = {
                "id": int(record["id"]),
                "name": record["name"].strip().title(),
                "amount": round(float(record["amount"]), 2),
                "processed_at": datetime.now().isoformat()
            }
            cleaned.append(cleaned_record)
        except (ValueError, KeyError) as e:
            print(f"[TRANSFORM] Skipping bad record {record} → {e}")
            skipped += 1

    print(f"[TRANSFORM] Clean: {len(cleaned)} | Skipped: {skipped}")
    return cleaned

def load(records, output_filepath):
    print(f"[LOAD] Writing {len(records)} records to {output_filepath}")
    with open(output_filepath,'w') as f:
        json.dump(records,f,indent=2)
    print(f"[LOAD] Done")

#SAMPLE DATA
def create_sample_data(filepath):
    sample = """id,name,amount
1,alice smith,100.50
2,BOB JONES,200.75
3,carol white,300.00
4,bad_record,not_a_number
5,david brown,450.25
6,,150.00
7,eve davis,999.99"""
    with open(filepath, 'w') as f:
        f.write(sample)
    print(f"[SETUP] Sample data created at {filepath}")

if __name__=="__main__":
    print("="*40)
    print("MINI ETL PIPELINE STARTING")
    print("="*40)
    input_file="week0-python/raw_data.csv"
    output_file = "week0-python/cleaned_data.json"

    create_sample_data(input_file)
    raw = extract(input_file)
    cleaned = transform(raw)
    load(cleaned, output_file)

    print("=" * 40)
    print("  PIPELINE COMPLETE ✅")
    print("=" * 40)

