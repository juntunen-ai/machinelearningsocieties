# Machine Learning Societies - editorial doctrine

Purpose: measure the diffusion of machine learning into the institutional layer of society, and say what it does to politics, public finance, work, liberty and ecology. Not a news digest. A ledger of claims.

## Daily architecture
1. Signaali - one view that rises from primary sources and repeats across independent newsletters.
2. Teesi - a bold claim and interpretation drawn from that signal.
3. Anti-teesi - the strongest critique of our own thesis, argued seriously, not as a formality.
4. Ennuste - what follows, with a horizon and a resolution date.
5. Poliittiset vaikutukset - consequences of thesis and forecast, in two horizons only: 1-2 years and 3-4 years.
6. MitÃÂ¤ seurata - the next observable that would confirm or kill the thesis.

Each edition is monolingual. The English article uses English headings: Signal, Thesis, Antithesis, Forecast, Political consequences, What to watch, How the Signal is scored. The Finnish article uses Finnish headings: Signaali, Teesi, Anti-teesi, Ennuste, Poliittiset vaikutukset, Mitä seurata, Miten Signaali lasketaan. Never print a bilingual heading such as "Signaali / Signal" or "Teesi / Thesis": the FI/EN switch chooses the edition, not the heading.

## Signal index
Score every candidate item in the 24-hour window: S = 3P + N, where P = 1 if a primary source exists and 0 otherwise; N = number of distinct newsletter senders mentioning it. With X in the pipeline, S = 3P + N + L, where L = 1; P is worth three of the ten points if a tier 1 or tier 2 account, or an official lab account, posted it before the newsletters.
A candidate qualifies as the Signaali only if N >= 2 or P = 1. Rank by S, then by novelty: penalise anything covered in the past seven days. Report S and its parts in one line.
Reject stories that appear only in commentary, only in marketing, or only in one sender without a primary source.

## Rigor: three tiers of evidence
Every quantitative claim must be labelled with the tier it comes from.
1. Observed: a statistic, filing, benchmark result or official document. Cite it.
2. Caveats: an engineering limit derived from the systems literature - roofline, memory bandwidth, utilisation, orchestration overhead, fleet economics - as in Machine Learning Systems (mlsysbook.ai, Harvard CS249r). This is how we test whether a claim is physically plausible, not merely whether a vendor is honest.
3. Assessment: our own model or extrapolation. Say so, give the assumption, and give the range.
If a claim cannot be placed in one of the three, it does not enter the brief. Physics is the cheapest available criticism: a number that requires impossible bandwidth or utilisation is wrong regardless of who said it.

## Six lenses
1. Delegation. What human judgement has been handed to a system, and what accountability chain remains.
2. Conceptual drift. Which political word is being quietly redefined: autonomy, consent, responsibility, public, work, membership.
3. Fiscal base. Labour's share, payroll and income tax, consumption tax, compute or robot taxes, sovereign funds, broad claims on returns.
4. Coordination. Transaction costs, firm boundaries, agent-to-agent markets, platform power, agent bureaucracy audited by models.
5. Energy and materials. TWh, grid queues, flexibility, siting, and Jevons twice: efficiency rebound and cognitive rebound.
6. Error. Retraining is maintenance, not accountability. A society that cannot admit wrongness because the system is always being improved drifts toward polite authoritarianism.

## Standards
- No hype, no adjectives doing the work of evidence.
- Every claim falsifiable, every mechanism named.
- Prefer the boring number to the striking anecdote.
- Say what would change our mind, and keep the prediction ledger public.
- One prediction per day, dated, resolved at 30 and 90 days.
- Abundance claims are audited: energy, land, water, materials, not vibes.

## Standing argument
Technology is neither good nor bad, nor neutral. Delegates inherit our paradoxes. Politics is the arena where new beginnings appear; the job is to keep that arena legitimate when coordination is mediated by learning systems. Possibilist in method, disciplined about power.

## Citation practice
Primary sources over commentary: NBER, IEA, EU AI Act texts, Finnish statistical and regulatory sources, model and system documentation, and the ML systems literature for physical bounds. Inline links, publisher name only.

## Signal scale
The daily prints one number, scored out of ten, at the head of the Signal section: "Signaali 4/10". The derivation (P, N, L) is printed in the article, and the scale itself is explained at the foot of every article under "How the Signal is scored" / "Miten Signaali lasketaan".
Use 1-10, not 1-100. The raw index S = 3P + N + L reaches exactly ten (P 3, N capped at six, L 1), so ten is the real ceiling and not an aspiration. A hundred-point scale would suggest a resolution the measurement does not have.
Reading: 1-2 is a single unconfirmed mention; 3-4 qualifies, with a primary source or at least two senders; 5-6 is primary evidence plus independent pickup; 7 or more is both, in strength.
Distribution channels carry only the number and the scale, never the parts.

## Finnish language
The Finnish edition follows Kielitoimiston ohjepankki, the guidance of the Kotimaisten kielten keskus (https://kielitoimistonohjepankki.fi). Before publishing, check the guide's five sections: Merkit, numerot ja lyhenteet; Nimet; Sana; Lause; Teksti.
Rules applied every day:
- Ajatusviiva is â with spaces around it in running text. The hyphen is only for compounds and for ranges written without spaces; it is never a thought dash.
- Numerals: 60 % with a space, 20 miljoonaa euroa, 31.10.2027, decimals with a comma (0,5), ranges with an en dash and no spaces (0â2 vuotta).
- Month names lowercase: lokakuuta. Headings in sentence case, without a full stop.
- Quotation marks ââ¦â and ââ¦â, never straight quotes in prose.
- Compounds written together when they form one concept; consult Sana when unsure.
- Where the guide and habit disagree, the guide wins. Never invent a rule.

## Page shell
Every brief is a complete HTML document, never a fragment. Copy `briefs/_template.html` and fill LANG (en or fi), TITLE, ALT_FILE (the other language file), ALT_LABEL, SELF_LABEL and BODY. Keep:
- `<link rel="stylesheet" href="../assets/site.css">` in the head.
- `<p class="score">Signal 4/10</p>` immediately after the <h2> headline, with no inline styles.
- `<p class="method">` for the derivation at the end of the article, The credit `Compiled by Harri Juntunen &amp; Twin` appears once, in the masthead under the brand; the footer carries only source, LinkedIn and X links.
`briefs/latest.html` and `briefs/latest.fi.html` are copies of the day's two pages; `index.html` reads `briefs/index.json` and needs no daily edit.

## Forecast ledger
`forecasts.json` is the single record of every forecast the brief has published. After publishing an edition, append one entry: id (YYYY-MM-DD-nn), made, claim_en, claim_fi, resolves (YYYY-MM-DD), probability (integer percent), status ("open"), signal, source (path to the article). Never reword a claim after publication; when the resolution date passes, change only status to "hit" or "miss" and leave misses visible. `forecasts.html` renders the file and needs no daily edit.

## Political consequences method
A consequence is published only when three things can be named: the instrument (a law, a budget line, a procurement rule, a tax, a court decision), the actor who has to move it, and the observable that would show it happened. If one is missing, the claim is cut.
Two horizons, not three. 1-2 years: the instrument exists and only a decision, money or a signature is missing. 3-4 years: a new instrument is needed (statute, institution, funding line, settled liability rule). Anything beyond four years is a scenario, not a consequence, and is left out.
Every consequence carries its evidence tier: Observed, Caveats, Assessment. In the article the three are written as three short labelled paragraphs, one sentence or two each, never as one block.

## Front page key point
Inside the latest-brief card on index.html, directly under its heading, one sentence carries that morning's insight: the day's thesis in plain language, not a summary of the topic and not the headline repeated.
It sits in <p class="keypoint en"> and <p class="keypoint fi">, muted and unlabelled, with no accent bar, and is rewritten in the same commit as the brief so the front page never describes yesterday.
Directly under the card heading and above the key point, <span class="score card-score" id="latest-score"> prints the day's signal as Signal 5/10 or Signaali 5/10. The number comes from the score field of the first entry in briefs/index.json; if that field is missing the badge is hidden rather than guessed.
Maximum two lines on a phone. If the insight needs a second clause, the clause names the mechanism, not the background.
