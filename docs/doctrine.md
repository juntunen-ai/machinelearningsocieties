# Machine Learning Societies - editorial doctrine

Purpose: measure the diffusion of machine learning into the institutional layer of society, and say what it does to politics, public finance, work, liberty and ecology. Not a news digest. A ledger of claims.

## Daily architecture
1. Signaali - one view that rises from primary sources and repeats across independent newsletters.
2. Teesi - a bold claim and interpretation drawn from that signal.
3. Anti-teesi - the strongest critique of our own thesis, argued seriously, not as a formality.
4. Ennuste - what follows, with a horizon and a resolution date.
5. Poliittiset vaikutukset - consequences of thesis and forecast, split by horizon: 0-2 years, 2-5 years, 5-10 years.
6. Mitä seurata - the next observable that would confirm or kill the thesis.

## Signal index
Score every candidate item in the 24-hour window: S = 2P + N, where P = 1 if a primary source exists and 0 otherwise; N = number of distinct newsletter senders mentioning it. With X in the pipeline, S = 2P + N + L, where L = 1 if a tier 1 or tier 2 account, or an official lab account, posted it before the newsletters.
A candidate qualifies as the Signaali only if N >= 2 or P = 1. Rank by S, then by novelty: penalise anything covered in the past seven days. Report S and its parts in one line.
Reject stories that appear only in commentary, only in marketing, or only in one sender without a primary source.

## Rigor: three tiers of evidence
Every quantitative claim must be labelled with the tier it comes from.
1. Measured: a statistic, filing, benchmark result or official document. Cite it.
2. Bounded: an engineering limit derived from the systems literature - roofline, memory bandwidth, utilisation, orchestration overhead, fleet economics - as in Machine Learning Systems (mlsysbook.ai, Harvard CS249r). This is how we test whether a claim is physically plausible, not merely whether a vendor is honest.
3. Estimated: our own model or extrapolation. Say so, give the assumption, and give the range.
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
