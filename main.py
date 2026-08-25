from scraper import fetch_website_text
from qualifier import qualify_company


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


print(f"\nSuccessfully qualified {len(results)} companies.")