# Sources

## X lists
Read the lists with x_get_list_tweets (max_results 100, tweet.fields created_at,public_metrics,author_id) every morning. Map author_id to username with x_get_list_members. Paginate with meta.next_token where a list exceeds one page.

### L1 - Frontier and AGI discourse, list id 1953471997347766403, 79 members
Lab leaders, safety researchers, economists and commentators.
- Tier 1 builders: sama, demishassabis, DarioAmodei, ylecun, JensenHuang, alexandr_wang, JeffDean, DrJimFan, ilyasut, bcherny.
- Tier 2 researchers: DKokotajlo, allTheYud, So8res, alexolegimas, SchmidhuberAI, drfeifei.
- Tier 3 commentators: emollick, dwarkesh_sp, CaseyNewton, sebkrier.
- Tier 4 aggregators: rohanpaul_ai, Dr_Singularity, TrueAIHound and similar. They carry volume, never primacy; in a recent 100-post sample one aggregator wrote 31 of them.
Use L1 to see arguments before they become articles.

### L2 - Labs, products and benchmarks, list id 1948109170089316589, 100+ members
Official company and product accounts plus evaluators: AnthropicAI, claudeai, ClaudeDevs, OpenAI, OpenAIDevs, AIatMeta, deepseek_ai, huggingface, MistralAI, Alibaba_Qwen, Kimi_Moonshot, cursor_ai, perplexity_ai, ManusAI, ElevenLabs, arena, ArtificialAnlys, SemiAnalysis_, berkeley_ai, StanfordAILab.
Use L2 for release detection and benchmark movement; these post first, newsletters follow hours later.

### L3 - Accelerators, investors and startup programmes, list id 1992323030195060948, 37 members
ycombinator, a16z, sequoia, 500GlobalVC, Techstars, GoogleStartups, seedcamp, join_ef, AntlerGlobal, SOSV, rockstart, PlugandPlayTC, StartX, MassChallenge, Sbootcamp, Platform6tre, DIGITALEUROPE and similar.
Use L3 for deal flow and commercial diffusion: which applications are being funded, which sectors hire, where Nordic and EU programmes put money. Announcements are marketing, so treat them as weak evidence unless a filing, round size or product follows.

## Scoring with X
S = 2P + N + L, where P = 1 if a primary source exists, N = number of distinct newsletter senders, L = 1 if a tier 1 or tier 2 account, or an official lab account, posted the item before it appeared in newsletters.
Discount aggregator-only stories. L3 counts as confirmation of diffusion, not as primacy. X is early warning, newsletters are confirmation, papers and official documents are primacy.

## Engineering reference
Machine Learning Systems, mlsysbook.ai, Harvard CS249r, two volumes, MIT Press 2026. Principles-first account of how ML systems are built, optimised and deployed: roofline reasoning, memory bandwidth, utilisation, orchestration overhead, fleet-scale infrastructure, with labs, TinyTorch and a simulator.
Use it to test claims against arithmetic and to translate capability into compute, bandwidth and energy terms. If a claim implies utilisation or bandwidth the hardware cannot deliver, that is a finding.

## Newsletters
AI Supremacy, AI as Normal Technology, Claude's Notebook, Linas's Newsletter, AI Frontiers, Cosmos Institute, and any clearly AI-focused sender in the inbox.

## Primary sources
arXiv and Hugging Face trending, provider release notes and model cards, GitHub activity, EU AI Act and Finnish regulatory publications, NBER, IEA, Statistics Finland, funding and labour-market data.

## Standing background
Two sources set the frame for what we look for. They are read for framing, not cited as evidence.

- normaltech.ai (Arvind Narayanan, Sayash Kapoor). AI as a normal technology: diffusion, adoption, economics and policy, not a single superintelligence event. Use it to keep the brief on technologies-in-use and to resist capability hype; check its AI-policy and evaluation work when a claim rests on benchmarks.
- ai-2040.com (Plan A). A scenario in which frontier development is deliberately slowed and made transparent to 2040. Use it as a contrast case: it describes an institutional path we can test against, not a forecast we adopt. Never present its timeline as our own forecast.

## Five levels of impact
Every edition should say which level a change touches, and the political section should follow from it:
1. Political - who decides, with what mandate, under what accountability.
2. Social - how people coordinate, trust and sort themselves.
3. Institutional - rules, courts, agencies, professional standards.
4. Organisational - how firms and public bodies actually run the work.
5. Individual - what a person can do, know, claim or refuse.
A signal that touches only one level is still publishable; a thesis that claims all five at once needs evidence at more than one.
