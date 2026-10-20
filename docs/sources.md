# Sources

## X lists
Read both with x_get_list_tweets (max_results 100, tweet.fields created_at,public_metrics,author_id) every morning. Map author_id to username with x_get_list_members. Paginate with meta.next_token where a list exceeds one page.

### L1 - Frontier and AGI discourse, list id 1953471997347766403, 79 members
Lab leaders, safety researchers, economists and commentators.
- Tier 1 builders: sama, demishassabis, DarioAmodei, ylecun, JensenHuang, alexandr_wang, JeffDean, DrJimFan, ilyasut, bcherny.
- Tier 2 researchers: DKokotajlo, allTheYud, So8res, alexolegimas, SchmidhuberAI, drfeifei.
- Tier 3 commentators: emollick, dwarkesh_sp, CaseyNewton, sebkrier.
- Tier 4 aggregators: rohanpaul_ai, Dr_Singularity, TrueAIHound and similar. They carry volume, never primacy; in a recent 100-post sample one aggregator wrote 31 of them.
Use L1 to see arguments before they become articles: what the frontier thinks about capability, control, economics and legitimacy.

### L2 - Labs, products and benchmarks, list id 1948109170089316589, 100+ members
Official company and product accounts, plus evaluation outfits: AnthropicAI, claudeai, ClaudeDevs, OpenAI, OpenAIDevs, AIatMeta, deepseek_ai, huggingface, MistralAI, Alibaba_Qwen, Kimi_Moonshot, cursor_ai, perplexity_ai, ManusAI, ElevenLabs, arena, ArtificialAnlys, SemiAnalysis_, berkeley_ai, StanfordAILab.
Use L2 for release detection and benchmark movement. These accounts post first; newsletters arrive hours later.

## Scoring with X
S = 2P + N + L, where P = 1 if a primary source exists, N = number of distinct newsletter senders, L = 1 if a tier 1 or tier 2 account, or an official lab account, posted the item before it appeared in newsletters.
Discount aggregator-only stories. X is early warning, newsletters are confirmation, papers and official documents are primacy.

## Engineering reference
Machine Learning Systems, mlsysbook.ai, Harvard CS249r, two volumes, MIT Press 2026. Principles-first account of how ML systems are built, optimised and deployed: roofline reasoning, memory bandwidth, utilisation, orchestration overhead, fleet-scale infrastructure, with labs, TinyTorch and a simulator.
Use it to test vendor and consultancy efficiency claims against arithmetic, and to translate capability into compute, bandwidth and energy terms. If a claim implies a utilisation or bandwidth that the hardware cannot deliver, that is a finding, not a footnote.

## Newsletters
AI Supremacy, AI as Normal Technology, Claude's Notebook, Linas's Newsletter, AI Frontiers, Cosmos Institute, and any clearly AI-focused sender in the inbox.

## Primary sources
arXiv and Hugging Face trending, provider release notes and model cards, GitHub activity, EU AI Act and Finnish regulatory publications, NBER, IEA, Statistics Finland, funding and labour-market data.
