# Mini Prospect Qualifier

A small Python tool that analyzes company websites and estimates how suitable each company is for B2B LinkedIn outreach services.

The tool fetches the visible text from each company's homepage, sends the text to Google's Gemini API, validates the structured response and saves the results to a CSV file.

## How it works

The pipeline is:

`Company website → Homepage text → Gemini → Structured data → CSV + Summary`

For each company, the tool returns:

* A one-sentence description of what the company does
* Industry
* Estimated company size
* LinkedIn outreach score from 1–5
* A short reason for the score

The final results are saved to `prospects.csv`, and a short summary with the average score and top prospects is printed in the terminal.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/emmykristina/mini-prospect-qualifier.git
cd mini-prospect-qualifier
```

### 2. Create and activate a virtual environment

Create the environment:

```bash
python -m venv .venv
```

Activate it:

```bash
Windows (Git Bash):
source .venv/Scripts/activate
```
```bash
macOS/ Linux:
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add a Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git and should not be committed.

### 5. Run the tool

```bash
python main.py
```

The results will be saved to:

```text
prospects.csv
```

## Error handling

Website requests use a timeout and basic error handling. If one website cannot be fetched, the program reports the error, skips that company and continues processing the remaining websites.

For example, during development `carpenova.se` returned a `403 Forbidden` response. Instead of stopping the complete pipeline, the tool skips the website and continues with the next company.

The structured LLM response is validated with Pydantic, including validation that the outreach score is between 1 and 5.

## LLM uncertainty

One area where I noticed uncertainty was the estimated company size.

During testing, Gemini sometimes returned values such as `Small`, `Medium`, `51-200 employees` or `Unknown`. The homepage often does not contain enough information to make an accurate company size estimate, so this value should not automatically be treated as factual.

For a more robust version, I would define fixed size categories in the schema, for example:

* `1-10`
* `11-50`
* `51-200`
* `201-500`
* `500+`
* `Unknown`

I would also allow the model to explicitly return `Unknown` when there is not enough evidence instead of forcing it to estimate.

Another thing I noticed during testing was that outreach scores can vary slightly between runs. Because the score is an LLM assessment rather than a deterministic calculation, I would treat it as a qualification signal rather than an absolute answer.

## Scaling from 10 to 10,000 companies

The current version processes companies one at a time, which is simple and works well for a small number of websites.

For 10,000 companies, I would change the architecture rather than simply running the current loop with a larger list.

Some important changes would be:

* Use asynchronous/concurrent requests to fetch multiple websites efficiently.
* Add retry logic and rate limiting for both websites and the LLM API.
* Use a database instead of relying only on a CSV file.
* Save results continuously so processing can resume after a failure instead of starting again.
* Use a queue and multiple workers to process companies in parallel.
* Track API usage, token usage and cost.
* Add more detailed logging for failed websites and LLM requests.
* Cache already processed companies to avoid unnecessary API calls.

For a larger production system, scraping and LLM analysis could also be separated into different processing stages so they can scale independently.

## Project structure

```text
mini-prospect-qualifier/
├── main.py
├── scraper.py
├── qualifier.py
├── test_qualifier.py
├── prospects.csv
├── requirements.txt
├── .gitignore
└── README.md
```

* `main.py` – runs the complete pipeline
* `scraper.py` – fetches and extracts homepage text
* `qualifier.py` – sends the text to Gemini and validates the structured result
* `test_qualifier.py` – simple test of the scraper + LLM qualification
* `prospects.csv` – example output from the latest run