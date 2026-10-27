# The Unbroken Record

A data journalism essay built from the WHO Disease Outbreak News (DON) record, 1996–2025. It asks a narrower question than most outbreak dashboards: not what diseases are spreading, but which places never leave the record at all, and what that says about surveillance, endemicity, and reporting behaviour rather than about danger.

**Read it:** [live page](https://humpheryeloke.github.io/The-Unbroken-Record/) .

## What it found

- Of 228 countries and territories that appear in the WHO DON record (COVID-19's separate dashboard entries excluded), only the Democratic Republic of the Congo reported an outbreak in every single year from 1996 to 2025.
- The typical country appears in 6 of those 30 years. Twenty-nine countries appear in 15 or more.
- Sixteen countries appear exactly once. Half of those single appearances land in 2009, when pandemic influenza reached territories with no other outbreak history in the dataset at all.
- Mpox (monkeypox) went unreported anywhere on earth for 19 years after a single 1997 case, resurfaced quietly from 2016, then jumped to 53 countries in 2022 and a second wave of 35 in 2025, a pattern the piece reads as "the silence ended," not "the disease is new."

## Why this isn't a dashboard

The WHO DON dataset is an event log (one row per disease–country–year outbreak report) with no case counts, deaths, or severity data attached. That rules out questions like "how dangerous was each outbreak," but it's well suited to questions about reporting patterns over time: which places recur, which appear once, and how reporting behaviour around a single disease can look like sudden emergence when it's really a gap closing. This project leans into what the data can honestly support instead of forcing it into a KPI dashboard it can't back up.

## Repository structure

```
index.html           the published essay (self-contained, opens in any browser)
data/
  outbreaks_clean_full.csv    full cleaned dataset (3,566 rows, all diseases incl. COVID-19)
  outbreaks_noncovid.csv      COVID-19 dashboard entries removed (2,352 rows)
  country_recurrence.csv      per-country years-active, event count, disease diversity
  yearly_events.csv           non-COVID events per year, 1996–2025
  mpox_by_year.csv            mpox/monkeypox reports per year, 1996–2026
analysis/
  analyze.py            core cleaning + country recurrence analysis
  analyze2.py           disease breakdowns, one-off country detail, mpox timeline
```

## Methodology

- **Source:** WHO Disease Outbreak News index, 1996–2026, via the Humanitarian Data Exchange.
- **Exclusions:** COVID-19 "Coronavirus dashboard" entries (1,214 rows, 2020–2026) are removed throughout — they come from an ongoing dashboard feed grafted onto the dataset, not individual DON bulletins. 2026 is excluded as a partial year still being filed.
- **Unit of analysis:** distinct country–year presence which shows whether a country shows up in the record for a given year, not how many reports, cases, or deaths that year produced.
- **Known limitation:** more reporting in recent years partly reflects better surveillance infrastructure and a larger WHO reporting apparatus, not necessarily more outbreaks occurring. Reported counts are reporting counts.

## Tech

Built with Python (pandas) for the analysis and a single self-contained HTML/SVG/vanilla-JS page for the essay, no framework, no charting library, so it opens anywhere and loads instantly.

---

Built by [Humphery Eloke](https://github.com/humpheryeloke) as a self-directed portfolio project exploring public health surveillance data.
