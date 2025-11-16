import pandas as pd
from elasticsearch import Elasticsearch, helpers

# === CONFIGURATION ===
ES_ENDPOINT = "https://my-elasticsearch-project-dda276.es.us-central1.gcp.elastic.cloud:443"
ES_API_KEY = "cTdKYmk1b0JwZFN4YXEwSVBhT2I6YVp6d0hMU2hpY2wyNWFwX0t2RlpkZw=="
CSV_PATH = "Incidents per Server and Mainframe LPAR per month.csv"
INDEX_NAME = "aiops_incidents"

# === CONNECT TO ELASTIC ===
es = Elasticsearch(
	ES_ENDPOINT,
	api_key=ES_API_KEY,
	verify_certs=False
)

if not es.ping():
	print("❌ Connection failed! Please check endpoint or API key.")
	exit()
else:
	print("✅ Connected to Elasticsearch!")

# === READ CSV ===
df = pd.read_csv(CSV_PATH)
print(f"Read {len(df)} rows from {CSV_PATH}")

# === DELETE ALL DOCUMENTS TO REMOVE DUPLICATES ===
try:
	es.delete_by_query(index=INDEX_NAME, body={"query": {"match_all": {}}})
	print(f"✅ Cleared index - ready for fresh upload")
except Exception as e:
	print(f"⚠️ Clear note: {e}")

# === UPDATE INDEX MAPPING FOR TICKET PRIORITY ===
try:
	es.indices.put_mapping(
		index=INDEX_NAME,
		body={
			"properties": {
				"Ticket Priority": {"type": "keyword"}
			}
		}
	)
	print(f"✅ Updated mapping for '{INDEX_NAME}'")
except Exception as e:
	print(f"⚠️ Mapping update note: {e}")

# === CONVERT DATE FIELDS ===
date_columns = ['Opened Date', 'Ticket Resolved Date', 'Ticket Closed Date', 'Target Finish Date']
for col in date_columns:
	if col in df.columns:
		df[col] = pd.to_datetime(df[col], format='%b %d, %Y %I:%M %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# === ADD DATE-ONLY FIELD ===
if 'Opened Date' in df.columns:
	df['Opened Date Only'] = pd.to_datetime(df['Opened Date'], errors='coerce').dt.strftime('%b %d')

# === CONVERT PRIORITY TO P1, P2, P3 FORMAT ===
if 'Ticket Priority' in df.columns:
	df['Ticket Priority Text'] = 'p' + df['Ticket Priority'].astype(str)

# === PREPARE ACTIONS FOR BULK API (UPDATE MODE) ===
actions = [
	{
		"_op_type": "index",
		"_index": INDEX_NAME,
		"_id": str(row['Ticket Number']),
		"_source": row.dropna().to_dict()
	}
	for _, row in df.iterrows()
]

print(f"Uploading {len(actions)} documents to index '{INDEX_NAME}'...")

# === BULK UPLOAD WITH ERROR HANDLING ===
try:
	success, failed = helpers.bulk(es, actions, stats_only=False, raise_on_error=False)
	print(f"✅ Uploaded: {success}, Failed: {failed}")
	
	if failed:
		print("\n❌ Failed documents:")
		for item in failed[:5]:  # Show first 5 failures
			print(f"  - {item}")
except Exception as e:
	print(f"❌ Error: {e}")