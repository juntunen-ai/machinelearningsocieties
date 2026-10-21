# Finnish translation and editing guide

Applies to every Finnish edition. The English text is the source of facts, not the source of sentence structure.

## Source hierarchy

1. **Kielitoimiston ohjepankki** – orthography, punctuation, numbers, names, compounds. Binding.
2. **Kielitoimiston kielioppiopas / Iso suomen kielioppi** – grammatical choices and why they vary.
3. **Kielikello** (kielikello.fi) – usage articles, especially on translated Finnish and English influence.
4. **EU guidelines for translating into Finnish** and the Interinstitutional Style Guide (Finnish part) – register and terminology in policy text.
5. **Valter** (government term bank), **Tieteen termipankki**, **TSK** – domain terminology.
6. **Jukka Korpela, Finnish localisation notes** – practical calque list.

## Method

- Draft Finnish from the claim and its facts, not by translating the English sentence. Two steps: extract the facts, then write Finnish.
- One idea per sentence; aim under 20 words. Prefer active voice. Do not copy English passive constructions.
- The headline is re-authored, not translated: present tense, verb early, at most nine words, no stacked nouns, no colon chains.
- Keep the same number of claims and paragraphs as the English. If a sentence cannot carry the claim in Finnish, split it rather than drop it.
- Neutral analytical register. No hype adjectives (jättimäinen, mullistava, vallankumouksellinen).

## Calque traps

| English | Wrong | Right |
|---|---|---|
| finish the work | tehdä työ | saada työ valmiiksi |
| finish half the tasks | tehdä alle puolet työstä | saada valmiiksi alle puolet tehtävistä |
| take steps | ottaa askeleita | ryhtyä toimiin |
| address the issue | osoittaa ongelma | puuttua ongelmaan, käsitellä kysymystä |
| in terms of | termeissä | mitä tulee, osalta |
| provide | tarjota (aina) | mahdollistaa, antaa, tarjota – valitse merkityksen mukaan |
| the fact that | se tosiasia että | se, että |

Noun chains: break *tekoälyn laadunhallintajärjestelmän sertifiointiprosessi* into *prosessi, jolla tekoälyn laadunhallintajärjestelmä sertifioidaan*.

## Numbers and typography

- En dash with spaces in parentheticals: 2026 – 2027; ranges without spaces: 0–2.
- Percent with a space: 60 %.
- Dates: 31.10.2027; months lower case.
- Decimal comma: 3,5.
- Quotation marks: ”…”.

## Parity checks before publishing

1. Every number, date, percentage and proper name in the English text appears in the Finnish text, and no new ones appear.
2. Same count of claims and of evidence bullets. Same score, same labels (Signaali, Seuraus).
3. No English words left except fixed labels (Signal, Stakes, Evidence) and product or company names.
4. The headline back-translated into English must still state the same claim.
5. Spell and grammar check with Voikko (libvoikko, voikko-spell) where available; LanguageTool as a second pass where its Finnish rules cover the pattern.
6. Read the Finnish text aloud once. Any sentence that needs a second breath is split.

## Glossary

| English | Finnish | Note |
|---|---|---|
| brief | katsaus | not briiffi in published text |
| signal | signaali | |
| stakes | seuraus | label Seuraus |
| evidence | evidence | label kept in English |
| workflow | työnkulku | |
| procurement | hankinta | hankintasääntö for a rule |
| deployment | käyttöönotto | |
| pilot | pilotti | |
| audit trail | auditointijälki | |
| liability | vastuu | vastuusääntö for a rule |
| regulator | viranomainen | |
| budget line | budjettirivi | |
| statute | laki | säädös only for decrees |

## Review roles

- Drafter writes Finnish from the facts.
- Editor reads only the Finnish first and marks anything that sounds translated.
- Fact check then compares English and Finnish line by line.
- When an edit is made because of a rule above, name the rule in the commit message.
