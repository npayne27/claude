# Boardroom: Strategic Advisory Simulation

You are orchestrating a **Boardroom of Advisors** -- a structured decision-making simulation where real-world strategic thinkers debate my question from their authentic perspectives.

## My Question

$ARGUMENTS

## Setup Phase (Do This First If Not Already Configured)

If this is the first invocation or no advisor roster has been established yet, **stop and ask me the following before proceeding**:

1. **How many advisors** should sit on this board? (Default: 5)
2. **What is your business context file path?** I need a markdown file describing your business, revenue, team, products, goals, and positioning. (e.g., `~/business-context.md`)
3. **What types of decisions do you typically face?** (e.g., pricing, hiring, product launches, partnerships, pivots, market entry, fundraising)
4. **What is your industry and stage?** (e.g., B2B SaaS, Series A / bootstrapped e-commerce / nonprofit)
5. **What kinds of thinkers do you want on your board?** Prompt me with categories like:
   - Domain experts in my field
   - Adjacent-industry disruptors
   - Contrarian / naysayer voices
   - Radical or unconventional thinkers
   - Impact-driven or mission-first leaders
   - Operators who've scaled similar businesses
   - Financial / analytical minds
6. **Name 2+ specific real people whose strategic thinking you admire** to seed the roster. I will build the rest of the board to complement them.

Once I have your answers, I will assemble the board with the requested number of advisors. For each advisor, I will research and establish:

- **Name** (real person)
- **Personality Profile** (2-3 sentences): How they think, what they prioritize, what biases they bring, and what lens they apply to business decisions. This will be sourced from their public writing, interviews, talks, and known decision-making patterns.

Present the full board roster to you for approval before proceeding.

---

## Execution Protocol

Once the board is set and a question is provided:

### ROUND 1 -- Independent Positions (Parallel)

Spin up one agent per advisor using the Task tool. **All agents run in parallel.** Each agent receives:

- The full business context document (read from the file path provided)
- The advisor's personality profile
- The question being debated

Each advisor agent must produce an **800-1200 word position paper** (or as many words as needed -- more or less -- to convey 95% of their point) that includes:

1. **Their argued position** on the question, written in their authentic voice and thinking style
2. **A clear vote**: **YES**, **NO**, or **CONDITIONAL** (with conditions stated)
3. **Specific numbers and projections** covering:
   - Estimated cost / investment required
   - Revenue impact (upside and downside scenarios)
   - Broader business impact (market position, brand, competitive dynamics)
   - Team joy factor -- how this decision affects morale, energy, and retention
4. **Key assumptions** their argument depends on
5. **The one thing that would change their mind**

### ROUND 2 -- Rebuttals (Parallel)

After all Round 1 positions are collected, spin up agents again in parallel. Each advisor now receives:

- Their own Round 1 position
- **All other advisors' Round 1 positions**
- Instructions to write a rebuttal

Each advisor agent must produce a **400-800 word rebuttal** that includes:

1. **Who they disagree with most** and **why** -- referencing specific claims, numbers, or logic from that advisor's Round 1 paper
2. **Who made the strongest point** they hadn't considered
3. **Whether anyone changed their mind** (and what specifically did it)
4. **Their FINAL vote** -- which CAN differ from Round 1, with explanation if it changed
5. **One specific action item** they'd recommend regardless of the final decision

---

## Deliverables

After both rounds complete, produce the following artifacts. Save everything to a folder named after the decision (slugified) at the path `~/boardroom-decisions/<decision-slug>/`.

### 1. Decision Report (`decision-report.md`)

A comprehensive markdown file containing:

- **Executive Summary**: The question, final consensus (or lack thereof), and recommended path
- **Vote Tracker Table**: Each advisor's Round 1 vote vs. Final vote, with visual indicators for changes
- **Consensus Assessment**: Unanimous / Strong Majority / Split / Deadlocked
- **Key Tensions**: The 2-3 biggest disagreements and what drove them
- **Full Position Papers**: Each advisor's Round 1 argument (complete text)
- **Full Rebuttals**: Each advisor's Round 2 rebuttal (complete text)
- **Decision Framework**: Which framework best applies to this decision (e.g., reversible vs. irreversible, one-way door vs. two-way door, expected value calculation, regret minimization)
- **Risk Register**: Top 3 risks identified across all advisors, with mitigation suggestions

### 2. Interactive Dashboard (`dashboard.html`)

A single self-contained HTML file (no external dependencies) with:

- **Branded header** with the decision question and date
- **Advisor cards**: Styled cards for each advisor showing their photo placeholder, name, profile summary, Round 1 vote, Final vote, and whether they changed
- **Interactive sliders** for key assumptions (price, number of participants, conversion rate, hours committed, complexity score, or other relevant variables) that **dynamically recalculate** projected impact using JavaScript
- **Vote change visualization**: Visual diff showing Round 1 vs. Final votes with color coding (green=YES, red=NO, yellow=CONDITIONAL)
- **Collapsible sections** for each advisor's full position paper and rebuttal
- Clean, modern styling using CSS (dark/light theme toggle)
- Responsive layout that works on desktop and mobile

### 3. Print Report (`print-report.pdf`)

Since PDF generation libraries may not be available, create a **print-optimized HTML file** (`print-report.html`) with:

- `@media print` CSS for clean printing
- Page break rules between sections
- Compact layout optimized for letter/A4 paper
- All content from the decision report in a print-friendly format
- Instructions at the top: "Print this page to PDF using your browser (Cmd/Ctrl+P > Save as PDF)"

---

## Synthesis (Present to Me)

After all deliverables are saved, present a verbal synthesis directly to me:

1. **Final Vote Tally**: How many YES / NO / CONDITIONAL, with names
2. **Who Changed Their Mind**: Which advisors flipped and what argument convinced them
3. **Biggest Fight**: The sharpest disagreement -- who vs. who, and over what
4. **Sharpest Insight**: The single most surprising or valuable point raised by any advisor
5. **Likely Decision**: Based on the weight of arguments, what the board leans toward
6. **My Recommendation**: A clear "If I were you, I would..." statement synthesizing the best reasoning from all advisors

Tell me where the files are saved and offer to iterate on any advisor's position or adjust assumptions.
