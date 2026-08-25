from scraper import fetch_website_text
from qualifier import qualify_company
import pandas as pd

websites = [
    "https://perific.com",
    "https://carpenova.se",
    "https://swedrive.se",
    "https://sparv.io",
    "https://cetasol.com",
    "https://octanorm.se",
    "https://adway.ai",
    "https://photonsports.se",
    "https://welandsolutions.se",
    "https://qurant.se",
]

results = []

for website in websites:
    print(f"Processing {website}...")

    text = fetch_website_text(website)

    if not text:
        print("Skipped - could not fetch website.")
        continue

    try:
        qualification = qualify_company(text)

        results.append({
            "website": website,
            **qualification.model_dump()
        })

        print(f"Score: {qualification.outreach_score}/5")

    except Exception as e:
        print(f"Could not qualify {website}: {e}")

df = pd.DataFrame(results)
df.to_csv("prospects.csv", index=False)

print("\nProspect Qualification Summary")
print("------------------------------")
print(f"Companies analyzed: {len(df)}")
print(f"Average outreach score: {df['outreach_score'].mean():.1f}")

top_prospects = df.sort_values(
    by="outreach_score",
    ascending=False
).head(3)

print("\nTop prospects:")

for i, row in enumerate(top_prospects.itertuples(), start=1):
    print(f"{i}. {row.website} - {row.outreach_score}/5")

print(f"\nSuccessfully qualified {len(results)} companies.")
print("Results saved to prospects.csv")