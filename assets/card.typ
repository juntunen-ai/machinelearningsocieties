// Machine Learning Societies — daily card
// Usage: typst compile assets/card.typ card.pdf && pdftoppm -png -r 150 card.pdf card
// Edit only the five values below; the layout is fixed.

#let kicker = "MACHINE LEARNING SOCIETIES"
#let dateline = "21.10.2026 · Signaali 5/10"
#let headline = [Laboratoriot eivät enää myy malleja, ne ostavat paperityön.]
#let footer = "juntunen-ai.github.io/machinelearningsocieties"

#set page(width: 20.32cm, height: 10.5cm, margin: (x: 1.7cm, y: 1.25cm), fill: rgb("#fdfdfb"))
#set text(font: "DejaVu Sans", size: 9.5pt, fill: rgb("#61707f"))
#text(weight: "bold", tracking: 2.2pt)[#kicker]
#v(3pt)
#dateline
#v(8pt)
#rect(width: 2.4cm, height: 3pt, fill: rgb("#1f4fd8"))
#v(12pt)
#text(font: "DejaVu Serif", weight: "bold", size: 27pt, fill: rgb("#12161a"))[#headline]
#v(1fr)
#text(size: 8.5pt)[#footer]
