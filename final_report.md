
# Final Report: IT Asset Data Operations & Insights

## Project Summary
This project demonstrates a full data engineering and analytics workflow on IT asset data, including cleaning, indexing, transformation, enrichment, and visualization to drive business insights.

---

## Phase 1: Excel Data Cleaning
**Techniques Used:**
- Removed duplicate rows based on the `hostname` field (Data → Remove Duplicates)
- Trimmed extra spaces from text fields (using `=TRIM(A2)` or Flash Fill)
- Replaced empty cells with `Unknown` for missing values
- Standardized date format in `operating_system_installation_date` to `YYYY-MM-DD`
- Saved the cleaned data as `it_asset_inventory_cleaned.csv`

---

## Phase 2: Indexing Data to Elasticsearch
**Script:** `index_data.py`
- Loaded cleaned CSV data into the `it_assets_inventory_cleaned` Elasticsearch index
- Verified successful indexing

---

## Phase 3: Data Transformation & Enrichment
**Script:** `transform_data.py`
- Reindexed data to a new index (`it_assets_inventory_enriched_final`)
- Added derived field `risk_level` ("High" if lifecycle status is EOL/EOS, else "Low")
- Calculated system age in years from installation date
- Removed records with missing, blank, or 'Unknown' hostnames and (optionally) 'Unknown' OS providers
- Deduplicated records based on `os_system_id`
- Updated existing records with new fields using `_update_by_query`

---

## Phase 4: Visualization and Insights
**Visualizations Created:**
- Assets by Country
- Lifecycle Status Distribution
- High vs Low Risk Assets
- Top OS Providers

**Screenshots:**
See `visualization_screenshots/` folder for all dashboard images.

---

## Final Business Insights and Learnings
- A significant portion of assets are at "High" risk due to EOL/EOS status.
- Certain countries (e.g., INDIA, BRAZIL) have a higher concentration of outdated systems, indicating urgent need for OS upgrades.
- Visualizations help prioritize upgrades and focus on critical risk areas.
- Data cleaning and transformation are essential for accurate analytics and decision-making.

---

## Challenges & Solutions
- **Messy Data:** Real-world data required multiple cleaning steps in Excel and Python.
- **Indexing Issues:** Ensured all records were properly formatted before upload.
- **Transformation Logic:** Used Python and Elasticsearch scripting for enrichment and updates.

---

## Conclusion
This project provided hands-on experience with the end-to-end data pipeline, from raw data to actionable business insights, using Excel, Python, and Elasticsearch.
