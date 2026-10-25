# Machine Learning Societies

Bilingual (English / Finnish) daily analytical brief and public forecast ledger tracking technological diffusion: how machine learning spreads through politics, the economy, work, and law.

Compiled by **Harri Juntunen** & [Twin](https://twin.so).

- **Short version:** Delivered to the WhatsApp community every morning at 07:30 (`Europe/Helsinki`).
- **Full editions & forecast ledger:** Published on Firebase Hosting at [https://machine-learning-societies.web.app](https://machine-learning-societies.web.app).

## Repository Structure

- `index.html` — Landing page, featured latest brief, and bilingual archive
- `about.html` — Methodology, analytical lenses, and scoring rules
- `forecasts.html` & `forecasts.json` — Public ledger of dated, probabilistic forecasts
- `briefs/index.json` — Archive index (newest first, with EN/FI titles, scores, and summaries)
- `briefs/YYYY-MM-DD.html` & `briefs/YYYY-MM-DD.fi.html` — Archived daily editions
- `briefs/latest.html` & `briefs/latest.fi.html` — Most recent edition
- `feed.xml` & `feed.fi.xml` — RSS 2.0 feeds (English and Finnish)
- `background.md` — Standing editorial context and analytical framework (ignored from public CDN deploy)
- `firebase.json` & `.firebaserc` — Firebase Hosting configuration (`machine-learning-societies`)
