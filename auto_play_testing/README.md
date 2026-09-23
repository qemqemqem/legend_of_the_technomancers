# Auto Play Testing (experimental)

Seeded menu-based character and situation generation with OpenRouter-assisted
action selection. The model gets a readable sheet headed by every base option
(Body, Mind, Face, Weird when available, and each item's tier), followed by all
tag IDs. It returns `action_plan`, `base_stat`, and `tags`. Python validates
ownership and listed base values, caps selected tags at five, then computes the
dice pool and outcome probabilities. AI judgments about **fictional**
plausibility still require human review. This is not a substitute for a GM.
Feats are generated for the character but are not shown in the model's sheet.
The model can choose an item by its gear ID or name; it can choose a tag by
full ID or by a unique owned tag name. Ambiguous names require full IDs.

Requires Python 3.9+; no third-party packages. From the repository root:

```sh
python3 -m auto_play_testing chart
python3 -m unittest discover -s auto_play_testing -v
export OPENROUTER_API_KEY='your key here'
python3 -m auto_play_testing run --model google/gemini-2.5-flash --max-cost 5 \
  --characters 10 --situations 10 --seed 42 --targets 1 2 3 4 --workers 8 \
  --output auto_play_testing/results
```

`chart` needs no API key. By default it writes tracked files in
`auto_play_testing/`: `dice_odds.svg` (heatmaps for partial-or-
better and full-or-critical by pool/target) and `dice_odds.csv` (exact failure,
partial, full and critical rates). `run` makes **one paid model call per
character/situation pair** using the current rulebook (tags can mix). Start with 2
characters and 2 situations to check your chosen model's JSON behavior/cost.
The runner checks live endpoint prices and reserves the whole 700-token output
allowance before each call; it refuses another request if that might exceed
`--max-cost`, including reservations for all in-flight calls. The worker pool
allows up to 8 simultaneous requests by default; lower `--workers` if your
provider rate-limits you. Rolls are seeded per trial, independent of response
order. Actual usage costs are saved with each trial. Pick a low-cost
model: this budget guard assumes the provider honors its advertised prices.
The model must support OpenRouter's `response_format: json_object`. Export the
key in your shell; the repository's `.env` file is not automatically loaded.

## Controlled dice-pool experiment

The default `run` follows legal ABCD priorities. To isolate each pillar,
`run-controlled` instead holds the other three columns at rank 2 and varies
the fourth from 1 to 4. These are intentionally **not** legal ABCD builds.
Each family shares a single all-rank-2 baseline; the other columns keep their
random choices when one column changes. Every character sees the same 1,000
unique situations, balanced across Body/Mind/Face/Weird themes and ten
templates per theme (25 distinct variations of each template). Each scene has
a distinct premise before incidental details are added, with a themed
complication and usable opening. Each situation
offers a problem, a possible opening, and incidental details, without telling
the model what action to take. Each scene is sent to exactly two characters:
one all-rank-2 baseline and one single-pillar variant from the same family.
The assignment cycles through every family/variant combination in shuffled
blocks, giving **2,000 planned calls** for 1,000 scenes, not a cross-product
of every scene and every character. The cost cap is a safety stop, not a
sampling goal. Themes
balance the sample but are never shown as prescribed stats. Given a text
character, situation, and brief dice rules, the model chooses its own objective
and action, then one of the listed base
options (Body/Mind/Face/Weird or an item's printed tier) and up to five tags
from any combination of the four domains. Python resolves names to owned
IDs and counts dice; fictional applicability is the model's judgment.
Invalid answers are excluded from results.

```sh
python3 -m auto_play_testing run-controlled --model google/gemini-2.5-flash \
  --families 6 --situations 1000 --workers 32 --seed 2042 --targets 1 2 3 4 --max-cost 2 \
  --output auto_play_testing/results/controlled-1000
python3 -m auto_play_testing.controlled_report auto_play_testing/results/controlled-1000 \
  --sheet-families 500 \
  --output auto_play_testing/controlled_report.pdf
```

The controlled PDF plots **dice, not percentages**: chosen base dice (character
stat or item tier) and applied tag dice under current rules, with 95% intervals
over independent character families. It compares each variation against its
family's rank-2 baseline on matched scenes, then reports chosen Body, Mind,
Face, Weird and Item bases and tag usage by Body, Stuff, Skills and Magic.
Base shares and domain action rates use mechanically valid rolls
as their denominator; domain tag-dice counts count each applied tag. An action
may use multiple domains. Missing or invalid AI responses are not weak
characters and cannot be used in matched comparisons. Dashed trend lines fit
four rank-level means equally (including the shared rank-2 baseline); those
rank means draw from different scene subsets. Their labeled slopes are
descriptive dice-per-rank, not estimates of a causal effect.
The AI may pursue different objectives for different builds in the same scene.
Two additional analysis pages show
the mean total number of tags owned per sheet, the pooled mean rating of all
available base options (Body/Mind/Face, Weird if positive, and every owned
item's tier), and stacked counts of owned tags by source, for every variation.
A seventh page plots those available base ratings with fitted trends.
Three sample pages show randomly selected tested character sheets, scenario
texts, and validated model action plans, including the chosen base and each
applied tag die. Sampling is reproducible from the run seed; check the raw
dataset for more examples. The 1,000 unique premises still reuse ten templates
per theme; this is not 1,000 independently authored scenarios.
These sheet metrics use 500 independently seeded offline families by default,
not the six families sent to the model; rerunning the PDF recreates the same
offline characters from the run's seed.

Run output (the default `auto_play_testing/results/` is gitignored):

- `setup.json`: generated characters and scenes, including menus, scenario
  themes and targets. The same scenes are used for every character.
- `trials.jsonl`: original action plan, chosen base, chosen tags and computed
  dice pool, plus API usage/cost. `proposal` keeps the model's original wording;
  scored `base_stat` and `tags` use canonical IDs. Normal runs also store rolls and exact outcome
  probabilities; controlled runs store one current-rule pool and its base and tags.
  Responses are written as they finish; rerunning overwrites the files.
- The program caps model-selected tags at five. `capped_tag_ids` records tags
  removed by that cap.
- `rejected.jsonl`: invalid proposals and their cost, excluded from success
  rates. The runner continues, but never silently credits invented dice.
- `report.json`: total paid calls, validated/rejected counts, and total cost.
- `request_errors.jsonl`: provider timeouts and other transient failures. A
  request with unknown billing reserves its full possible price against the
  budget; `report.json` records both known cost and that conservative bound.
- `summary.csv` (normal runs): observed and expected outcome rates grouped by
  Body rank, Body stat, other column ranks, scenario theme, target, and overall.
  `body_rank_outcomes.svg` plots expected failure, partial, full, and critical
  rates by Body rank. Exact rates avoid small-
  sample dice noise, but **do not** eliminate sampling bias in scenes/actions.

Mechanical validation cannot check whether a model's chosen action is truly
plausible, whether its chosen tags really apply, or whether it found the best
action. Review raw `action_plan` and chosen tags before using
these rates for game balance. Rejected model output is excluded, not counted as
an in-world failure; a high rejection rate biases the remaining sample.

Assumptions/limits: targets 1-4 by default are experimental (GM target-setting
guidance is unfinished). Each call starts from an undamaged copy of its
character, with no party help or multi-roll conflict. Feats are omitted from the
prompt and do not add dice. Stuff purchases use published examples of Weapons,
Vehicles, Armour, Locations, and the four described Gadgets. Stuff tags use the
published category menus or the examples for the specific Gadget purchased. The
generator buys a Tier-4 item before applying the free Stuff-4 Tier-5 capstone.
The model chooses its own base; scenario themes and target
numbers are shared across characters. A missing or null base is invalid, not
an in-world failure.
Human spot-check the proposals in `trials.jsonl` before using correlations to
change game balance. Normal ABCD builds link the pillar ranks; the controlled
off-grid design varies one pillar but still relies on model-chosen actions.
