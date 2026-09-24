# Rules Recommendations from the Character-Build Playtest

*Compiled 2026-09-23 from ten character builds in this directory (01–10).
Each playtester built one character strictly by the rules, rolled it
through four scenarios, then reflected on the process.*

**Source key** (the numbers in brackets throughout):

| # | Character | Build (Body/Stuff/Skills/Magic) | Seed |
|---|---|---|---|
| 01 | Tamsin Vey, the Lamplighter | C/A/D/B | (main session) |
| 02 | Hum, the Hive That Walks | A/D/C/B | Monstrous |
| 03 | Ambrose Pell, fraud prophet | D/B/A/C | Face grifter |
| 04 | Ysolde Crane, folded scholar | D/C/B/A | Frail archwizard |
| 05 | Dr. Ines Calloway, coroner | C/B/A/D | Mundane expert |
| 06 | Nix "Root" Adeyemi, netrunner | C/B/D/A | Cyberpunk native |
| 07 | Odile Marchbank, 81 | D/B/A/C | Very old / underestimated |
| 08 | Idris Kell & Tallow | D/A/C/B | Companion |
| 09 | Winnie Baste, caterer | D/B/C/A | Comedic / Food |
| 10 | Kesh, the Salt-Cured | A/D/B/C | Shirt on back |

Where playtesters proposed *different* fixes for the same problem, all
options are listed so the authors can choose between them.

---

## Top Priorities (raised by the most playtesters)

| Issue | Raised by | Chapter |
|---|---|---|
| Target-number guidance is placeholder text; no pool size can be judged | all 10 | For the GM |
| "Your First Skill Adds +1" reads as if only one Skill counts | 02 03 05 07 09 10 (+06) | Skills / How to Play |
| When do Feats need a roll, and which Stat? | 02 03 04 05 06 07 10 | Special Feats |
| Item tier does nothing for characters with a high Stat | 02 03 05 06 10 (+01) | Stuff |
| "Acting through" an item has no limits (Face via a dog, Weird via a building) | 01 03 04 06 08 09 | Stuff / How to Play |
| No minimum pool size; frail characters drain Coherence | 03 04 05 07 08 09 10 | How to Play |
| Coherence has no refill rule, and Coherence 0 acts as a full heal | 03 04 06 07 09 10 | How to Play / GM |
| The 5-tag cap does all the balancing; near-duplicate tags fill it | 02 03 06 08 09 10 | How to Play / Magic |
| Weird loopholes (teleport beats lifting, items lift Weird, Weird skips pool penalty) | 03 04 06 08 09 10 | Magic |
| Does a Feat-granting item cost Stuff Points? | 01 05 07 08 09 | Stuff / Special Feats |

---

## What's Working (keep these)

Almost every playtester praised the same things:

- **The ABCD priority step** is fast, forces real trade-offs, and often
  improved the concept itself ("a plain strong man wasn't allowed at
  Body A") [01 02 03 07 08 10].
- **One formula for every roll** (Stat + tags, count 4+). No subsystems to
  look up; every pool can be audited at a glance [all].
- **"What resists?"** settles most Stat choices in seconds. The *Spells and
  Their Stats* table was called "the best page in the book" [02 04].
- **The double-cost 5th pip** makes a Stat of 5 a real commitment [02 05 06 07].
- **Consequence pools = Stat rating** turns weak Stats into dramatic
  weaknesses; "rest doesn't restore Face" is excellent story fuel
  [03 05 06 10].
- **Re-Kitting on Arrival** was the favourite moment in nearly every build
  [01 02 04 06 07 08 09 10].
- **Feats as "a door dice can't open"**, and skill-sourced Feats (*Cold
  Reading*, *Structural Reading*) that make mundane experts feel legendary
  [02 03 05 07 10].
- **Max(Tier, Stat)** creates lovely emergent character moments: the frail
  rider on the mighty beast, the wheelchair stronger than its user, the
  cane doing the work [04 07 08 09].

---

## Chapter 1: Introduction (`00-intro.tex`)

- **The "1 to 10 dice" promise is broken** by empty pools (Body 1 − 1 = 0)
  and Weird 0. Update this once a pool-floor rule exists (see *How to Play*)
  [03 04 05 07].

---

## Character Creation (`01-character-creation.tex`)

- **State the letter-to-rank mapping outright** (A = rank 4 … D = rank 1).
  Right now you have to work it out by matching wording [03 06].
- **The Body D blurb, "base stats across the board", is misleading.** A
  Body-D / Skills-A character can legally have Face 5 [03].
- **"A legendary weapon" appears at Stuff B,** but the Legendary Blade is
  Tier 4, which Stuff B can't buy. Change the wording or the catalogue
  (this also appears in the Stuff chapter's "You Have…" column) [07].
- **Does Body A have to be non-human,** or does "truly strange" just mean
  exceptional? [10]
- **Warn in the matrix that Stuff mostly helps weak Stats,** if the
  tier rule stays as it is [05].

---

## Body (`02-body.tex`)

### Stat Points and maxed Stats
- **The sentence "a Body-4 character … cannot max two" is wrong** once Skills
  Stat Points are added. Body 4 + Skills C = 10 points (two 5s); Skills B = 11;
  Skills 4 = 13 [02 10]. Fixes:
  - reword it to "from Body's points alone", **or**
  - add a hard rule that no character starts with more than one Stat at 5
    [02 10], **or**
  - make the 5th pip cost more [10].

### Body A balance
- **Body A may just be the best column.** Stats count twice (dice *and*
  pools), and the jump from 6 to 9 Stat Points at rank 4 is the biggest in
  the book. The Designer's Note doesn't account for pool size [02]. Options:
  - (a) cut Body rank 4 to 8 Stat Points;
  - (b) make consequence pools a fixed size (e.g. 3 each) plus a smaller bonus;
  - (c) give Body A a mandatory **Monstrous Complication**: a weakness the
    GM can invoke (no hands, can't pass as human, vulnerable to fire) that
    costs dice or pool points when it comes up. This also fixes "monsters
    have only upsides" [02].

### Non-human characters
- **Add a "Non-Human Travellers" sidebar** [02] covering:
  - which magic Form covers your own body (your nature's Form, or a new
    `Self` Form);
  - whether physical shapeshifting can use Body instead of Weird;
  - how Lifestyle and the Face pool work for monsters (a swarm has no
    pockets; how does a creature barred from towns recover Face through
    "recognition"?);
  - 6–10 more exotic Body Tags: `Swarm`, `Amorphous`, `Armoured Hide`,
    `Huge`, `Many-Limbed`, `Alien Senses`. The current 10 are all
    humanoid-coded.
- **Where does chrome go?** A cyber-eye could be a Body Tag (can't be lost),
  a Body Feat, or a Stuff Feat (can be ripped out, returns free next realm).
  Suggestion: "your choice of Body Tag or Stuff; Body can't be lost, Stuff
  can be upgraded" [06].

### Frailty and flaws
- **Add an optional flaw tag at Body D** (`Frail`, `Young`, `Tiny`, `Old`).
  It adds a die when the flaw *helps* (being overlooked, fitting through a
  gap), and the GM may invoke it for complications. That supports kids,
  the elderly and the sickly, who are currently invisible on the sheet [07].

### Tag questions
- **Is `Natural Weapon` allowed for conditioned human fists,** and should it
  stack with `Brawling` on every punch (double-dipping on one fact)? [10]
- **Are the paired "weight class" tags** (e.g. `Strong` + `Natural Weapon`)
  meant to be taken together and stack on the same roll? [10]
- **Give guidance on sizing and re-skinning custom Body Tags;** the printed
  ones are carefully paired, but custom ones are balanced only by GM taste [06].
- **Body Stat Points are a poor buy for weapon users,** since a weapon's tier
  replaces Body in combat. This goes away if the tier rule is reformed
  (see Stuff) [07].

---

## Stuff (`03-stuff.tex`)

### Make item tier matter to everyone
- **Max(Tier, Stat) never helps a character whose Stat is 4–5,** so Stuff
  becomes "the price of tags" for specialists. Kesh (Stuff D) lost no dice at
  all on a punch [02 03 05 06 10]. Options:
  - an item whose tier is **at least** your Stat also adds +1 die (counts
    toward the cap) [03 05 02 10];
  - an item whose tier is **below** your Stat adds +1 die, so the
    specialist's signature gear always matters [06];
  - replace Max(Tier, Stat) entirely with "tier adds a die when ≥ Stat" [10];
  - tier limits what's *possible* (only a Tier-3 lab can identify a
    designer toxin at all) [05];
  - a Location can spend its tier as a one-off "home ground" bonus [03];
  - at minimum, state plainly that Stuff mainly helps weak Stats [05].
- **The Tier-5 capstone reaches 10 dice on its home ground with no
  effort.** Probably balanced by being limited to that place; worth
  playtesting [01].

### Limit and define "acting through"
- **Define "acting through" with a short list:** "the item is doing the
  work: the blade strikes, the car moves, the terminal computes, the
  fortress's walls, staff or sensors perform the action. Merely standing in
  a place or wearing a thing isn't acting through it" [03]. Open cases:
  how much of an island counts as the lighthouse [01]; ramming or dodging
  in a wheelchair [04]; running out of your own chapel [03].
- **An item's tier should replace only the Stat for its category's
  purpose:** Vehicle for movement, pursuit and ramming; Weapon for attacks;
  Location for actions that use the place; Gadget for its one trick's Stat.
  **Never Face** unless the item is built for social use [06 08 09].
  (Examples of the exploit: a Tier-3 deck charming an AI [06]; a Tier-5 dog's
  "puppy eyes" [08]; persuading "through" a food truck [09].)
- **Two items at once** (a bow fired from a mount): the one doing the action
  supplies the base [08].
- **One item launching another** (a ladle hurling a ham): say which tier
  counts [09].
- **State that items can't supply Weird** (or cap Max(Tier, Weird) at 3).
  Otherwise a Tier-4 teleporter or a Tier-3 chapel breaks "Weird never rises
  above 3" [03 04].

### Objects you don't own
- **Give unowned objects a GM-set tier of 1–4** with a one-line guideline
  (hijacked golem, stolen drone, borrowed terminal) [06 10].
- **Improvised or found items are Tier 1–2 with 0–1 tags and break on a
  failure,** so a Stuff-D character can grab things but can't rely on them.
  Right now "whatever's lying around" has no rule at all [10].
- **Whose pool takes damage** while you ride a hijacked golem? [06]

### Damage, armour, healing
- **Add a damaged state between "fine" and "lost."** A consequence can
  *mark* an item (−1 Tier, or one tag unusable until repaired or healed); a
  second mark means it's lost. That gives companions, ships and mechs a way
  to be hurt, and gives repair something to restore [08].
- **Armour's tier currently does nothing.** There are no defence rolls, so
  armour tier never enters a pool, and Tier 2 and Tier 4 armour are
  identical except for price [03 08]. Suggestion: armour tier (or half of it)
  cancels that many points of Body loss per scene [03].
- **Say what healing or repairing Stuff restores** [08].

### Companions
- **Add a Companion entry (Tiers 2–4)** with a tag menu in the usual paired
  weight classes: `Loyal`/`Fierce`, `Keen Nose`/`Watchful`, `Swift`/`Sturdy`,
  `Clever`/`Trained`, `Mount`/`Small`. When the companion does the work,
  roll Max(Tier, the Stat the action uses) + the companion's tags + any PC
  Skills for directing it. `Mount` can take over what Vehicle does for
  creatures [08].
- **Say whose tags apply when a companion acts on its own** [08].
- **Let Stuff Feats target the item:** "your Vehicle or Companion gains this
  Feat instead of you" [08].
- **Warn about custom Feats that undo the only drawback.** Tallow's "Comes
  When Called" turned *Losing Your Stuff* into a minor inconvenience [08].

### Feat items
- **Do Feat-granting items cost Stuff Points?** Every build that took a
  Stuff Feat treated the item as free, but nothing says so [01 05 07 08 09].
- **Is the Feat lost when its item is stolen?** Stuff can be stolen for the
  rest of a realm, but Feats "always travel with you" [07].

### Lifestyle
- **Allow a lower Lifestyle than your rank** ("poor servant with one
  priceless animal" is forced to be Rich) [08].
- **Can cash stand in for a roll** (bribes, purchases)? [08]
- **Does "good tools" ever supply a tag or tier,** and does it make a cheap
  Gadget redundant? [05 07]
- **Lifestyle is an unlimited ammo supply** (endless hams) — probably fine,
  but worth a line [09].

### Catalogue
- **Make Stuff C less samey:** 3 tags at rank 2 instead of 2, or a free
  Tier-1 trinket. Right now it produces the same two-item sheet every time [04].
- **A cyberdeck fits no category.** Gadgets "do one thing" and the book warns
  against "a spell wearing a disguise", which describes a deck exactly.
  Consider a Tool/Interface category; the book's own "cutting deck" example
  implies decks were intended [06].
- **Can an item take a tag from another category's menu** (`Kitchen` ≈
  Location `Workshop` on a Vehicle)? [09]
- **Give the GM a pressure lever for Stuff D** (they're always the one without
  supplies, a disguise or a way in). *Losing Your Stuff* can't touch someone
  who owns nothing [10].

---

## Skills (`04-skills.tex`)

### Stacking
- **Rewrite or rename "Your First Skill Adds +1."** As written it adds
  nothing to the tag rule, and its heading makes it look as if only the first
  Skill counts. Whether Skills A is strong or weak depends on this one
  sentence [02 03 05 07 09 10]. Suggested names: "No Penalty for Lacking a
  Skill" [03] or "No Skill, No Penalty" [10]. Then pick one:
  - **every applicable Skill adds a die** like any tag, up to the cap
    (majority recommendation, matches Magic) [02 03 05 10]; **or**
  - **one Skill per roll**, other tag types stack [07].
- **Add a narrowness rule for invented Skills,** matching Magic's Specific
  tags: an invented Skill must be narrower than a printed one [05].
- **Add an anti-redundancy rule:** "two tags describing the same act count
  once" (e.g. `Deception` + `Performance` + `Playing Harmless` on one lie)
  [07]. Body and Stuff tags are in paired weight classes; Skills have no
  such guard [07].

### Choosing the Stat
- **Skills and How to Play disagree.** Skills says "the Stat sets the
  approach"; How to Play and Magic say choose by what resists. A specialist
  can reframe almost anything as a roll on their 5 [03]. Suggested wording:
  "Choose the Stat by what resists *your chosen approach*; the player picks
  the approach, the GM may veto one that doesn't fit the fiction" [03].
- **Give invented Skills a default Stat** [08].

### Catalogue
- **18 printed skills vs 14 Skills Known at rank 4** means the choice is
  really which 4 to skip. Enlarge to about 24–30 entries [05], or reduce
  Skills Known at ranks 3–4 (to about 10 at rank 4) [05 06 10].
- **Add the skills the book itself uses:** `Larceny` and `Driving` (How to
  Play examples) and `Animal Handling` (named in a Feat) [07 08].
- **`Firearms` ("and ranged weapons") overlaps `Archery`.** Which applies to
  a re-kitted bow? [05]
- **Add a re-skin rule for Skills.** Body Tags, Magic, Stuff and Feats all
  have one; Skills don't. Is `Hacking` dead in High Fantasy, partly alive
  (locks and wards), or re-skinned to `Warding`? [06]

### Designer's Note
- **The "1 tag ≈ 0.5 Stat Point" exchange rate breaks down above the tag
  cap,** and assumes every tag is equally likely to apply; the 13th and 14th
  skills rarely come up [05 10].

---

## Magic (`05-magic.tex`)

### Fence off Weird
- **Teleporting always beats lifting for a weak wizard.** "Get buff to lift
  boulders" is undercut by the next FAQ, "or just teleport them." Ysolde:
  2 dice to lift, 5 to fold [04].
- **Add an intent clause to "what resists?":** "If the purpose of the effect
  is to move, harm or change a creature or a heavy object, use the Stat that
  would resist doing it directly, however you describe it." This closes the
  "fold the floor he's standing on" loophole [04].
- **"Weird never deals harm; the harm is always a second roll against what
  resists it."** Add spell-table rows for *Drop a conjured anvil on a guard*
  and *Hurl a conjured ham* [09].
- **Cap the tags on a Weird roll at the Weird value** (max 6 dice at Weird
  3), so "Weird tops out low" is actually true. Weird 3 + 5 tags currently
  gives 8 dice [06].
- **Items can't supply Weird** (see Stuff) [03 04].
- **Weird skips the empty-pool penalty,** so repeated Weird self-heals keep
  pools topped up at no cost [04 08 10]. Options: give Weird its own pool
  that drains Coherence directly, or forbid Weird self-heals while any of
  your pools is at 0, or limit them to 1 point once per scene [10].

### Mundane actions and Weird
- **"Heal a willing ally" is Weird,** so read literally a mundane surgeon
  rolls Weird 0 [05 07]. Fix: "Weird is only for effects that *could not
  happen* without Magic. If a mundane action could achieve the same result,
  use the Stat that action would use." Move the healing row to Mind [05 07].
- **"What resists?" is written for all actions but only tested on magic.**
  If nothing resists a mundane action, it just happens or uses the Stat for
  the difficulty (surgery is Mind) [07].
- **"What resists?" has no answer for stealth or perception.** Being seen
  isn't matter, a puzzle or a will; the table says "sneaking past them is a
  separate roll" without naming the Stat [03].

### One roll or two?
- **Give a single rule of thumb.** Invisibility-then-sneak is two rolls; the
  fireball scare is one. Illusions, summons and conjure-and-drop fall in
  between [03 04 09]. Proposals:
  - "roll the effect separately only if it lasts past the action that uses
    it" [04];
  - "if it's aimed at someone's will and used at once, it's one roll on that
    Stat; if it has to exist first and is used later, roll Weird, then roll
    again" [03].

### Edge cases for the spell table
- **A paralysing nerve-strike:** "striking" (Body) or "changing a creature"
  (Face)? [10]
- **Targeting the surroundings** (teleport the floor, armour or air) dodges
  "changing a creature is Face." The intent clause above fixes this [04].
- **Constructs and AIs:** "has a will" is a GM call a Face-1 player will
  always argue toward Mind. Rule of thumb: "if it can be persuaded, it's
  Face" [06].
- **Clarify "Food" in the spell table** as an example theme, not a Part III
  realm [09].

### Healing and transformation
- **Say what healing restores:** e.g. 1 pool point per success, once per scene
  per target [04]. Currently "the GM decides" is the only guidance [08 10].
- **Say what self-transformation grants:** e.g. one temporary tag for a scene,
  never a Stat change [04].

### Tags
- **Stop near-synonyms filling the cap.** `Animal` ⊃ `Food` ⊃ `Ham` all
  describe one ham [09]. Options:
  - "one object, one tag per layer": only the narrowest nested tag plus one
    Technique counts [09];
  - at most one Specific tag per roll [09];
  - a Specific tag can't name a single individual (`Tallow`) [08];
  - "two tags that describe the same trait count once" [08].
- **Say what a Specific tag must be narrower than** when no Form covers the
  domain: space/teleportation [04], machines/data/electricity [06], luck,
  time. Is `Food` legal? It cuts across Plant/Animal/Water/Fire [09].
  `Lightning` has two possible parents [06].
- **Do Specific tags keep their scope when they re-skin?** `Networks` covers
  everything in the sprawl but "ley lines" almost nothing in fantasy [06];
  `Insects` → "drones" is a 2-die swing decided by GM mood [02]. Proposed
  rule: "Every tag reskins with its realm. Its *narrowness* travels, its
  *object* translates" [02].
- **Which Form covers a non-human's own body?** `Body` is "humans and
  humanlike bodies" [02].
- **Rename the Form `Body`** (e.g. `Flesh`); "roll Body + `Body`" is confusing
  out loud [10].
- **If tags aren't a prerequisite, what do they restrict?** Can a Magic-2
  character attempt any Weird effect with 1 die and no relevant tags? [07]
- **Base 0:** "with a base of 0, you cannot attempt the action unless a tag or
  item supplies a base" makes Magic D a real limit [05].

### Rank balance
- **Magic C is weak:** Weird 1 equals an untrained Stat, and 3 tags mostly pile
  onto rolls you'd make anyway. At 1 tag ≈ 0.5 SP, Magic 2 ≈ 2 points of value
  vs Body 2 ≈ 4.5 [03 07]. Options:
  - raise Magic 2 to 4 tags, or set Weird to at least 2 at Magic 2 [03];
  - make Weird 1/2/3/4 by rank [07];
  - let Magic-C characters add Weird as a bonus whenever a magic tag applies [07].
- **Magic A buys breadth, not power.** 12 tags against a 5-tag cap mostly go
  unused, and Magic A + Body D can never reach a Stat of 5 [04 06 09].
  Proposals pull in opposite directions:
  - make it stronger: raise the tag cap to 6 on Magic rolls, give Magic A
    1 Stat Point, or allow one "signature" tag combination counting as an
    extra tag [04];
  - make it smaller: cut Magic 4 to about 8–9 Tags Known [06].
- **Magic Feats should do something casting can't.** Blink either duplicates a
  wizard's Weird teleport or is strictly better than it. Keep teleport-type
  Feats out of Magic, or let a Magic Feat make one Weird effect always a full
  success [04].
- **Say how themed or non-elemental magic re-dresses** under "Magic is
  hacking / science" [07 09] (see Realms).

---

## Special Feats (`07-special-feats.tex`)

### Rolls
- **Say when a Feat needs a roll.** Fly says "only when in doubt"; Read Minds,
  Turn Invisible, Blink and See Through Solid Matter say nothing, while the
  spell table makes the same effects Face or Weird rolls
  [02 03 04 05 06 07 10]. Consensus wording:
  - **Continuous** Feats never need a roll to function [02].
  - **Action** Feats: "A Feat makes the impossible *possible*, not *certain*.
    Roll when something resists (a guarded mind, a lead-lined wall); don't
    roll when nothing does" [02 05 07].
  - Then align the Read Minds / Turn Invisible rows in the spell table and
    list the Feat–spell overlaps [05 07].
- **Which Stat when a Feat is rolled?** Two proposals:
  - "choose the Stat by what resists; the Feat's source column never changes
    the Stat" [10];
  - "use Weird for a Magic source, [Stat] for other sources" [04].
- **Give Feats a hook into the dice:** when a Feat clearly applies, skip the
  roll or lower the target by 1. Invisible Nix sneaks with the same dice as
  visible Nix [06]; Read Minds told Ambrose what the envoy feared and changed
  no number [03].
- **Say outright that Feats removing a consequence remove the roll** (Needs
  No Air, Never Sleep, Eat Anything) [09].

### Scope and fiction
- **State the principle "mechanics hold, and the fiction bends to fit"**
  [06], or say that the source's fiction *can* shrink a Feat [02]. Test
  cases: a "pours through cracks" Walk Through Walls vs a seamless vault
  [02]; Master Misdirection invisibility vs a thermal camera [07];
  implant-reading telepathy on un-chromed peasants [06].
- **Consider a narrower scope for skill-sourced Feats** (Structural Reading
  sees through flesh and ordinary walls, not vaults) so "mundane" still means
  something. Ines had more impossible powers than a Magic-A wizard's column
  grants [05].
- **Needs No Air:** does it cover vacuum cold and decompression, or only
  suffocation? [05]

### Caps and calibration
- **Answer the open Feat-stacking TODO;** consider a cap [05 10].
- **Give custom Feats a worked example and calibration.** Is "what you eat
  can hurt you" as big as "gravity"? [09]
- **Add a limitation dial:** a GM-approved restriction (Pantry Step needs a
  cupboard at both ends) could earn an extra tag slot, a second use, or a
  cheaper source. Right now narrowing a Feat earns nothing [09].

### New Feats
- **Add social Feats** so Face characters have options that fit [03]:
  - *Unforgettable* — anyone who has met you remembers you and your name,
    across language and realm;
  - *Speak Any Tongue* — a Languages-style Feat for people;
  - *Words as Law* — once per scene, one plain sentence is believed as
    literally true unless disproven in front of the listener.
- **Companion-facing Stuff Feats** ("your mount can fly") [08] (see Stuff).

---

## How to Play (`11-how-to-play.tex`)

### Choosing the Stat
- **Settle Stat selection in one place.** Magic says "a will resists → Face";
  Conflicts says "a display of strength might roll Body to shake their
  Face". For Kesh that's 8 dice vs 4 on the same threat [10]. Recommendation:
  always choose by what resists, and let `Strong` count as a tag on the
  Face roll [10]. See also the approach-vs-resistance fix under Skills [03].

### Pool floor and being taken out
- **Define a 0-die pool** (Body 1 with an empty pool; Weird 0)
  [03 04 05 07]. Options:
  - pools never drop below 1 die [04 07];
  - 0 dice is an automatic failure [03];
  - at 0 dice, roll 1 die and a 6 counts only as a partial success [04];
  - with a base of 0 you can't attempt the action without a tag or item [05].
- **Add a "taken out" rule.** When a PC's pool is empty and they take another
  hit, the party chooses between that PC leaving the scene and paying
  Coherence. That makes frailty the character's problem, not a hidden drain
  on the party [07].

### The 5-tag cap
- **The cap, not the sheet, is what limits specialists.** High ranks grant
  12–17 tags; most fights become Stat + 5 = 10 [02 03 06 09 10]. Options:
  - reduce Skills Known, Body Tags and Magic Tags at ranks 3–4 [06 10];
  - cap tags per column (e.g. no more than 2 from any one column) [10];
  - let spare applicable tags lower the target (every 2 spare → −1) [06];
  - anti-synonym rules (see Skills and Magic) [07 08 09].

### Coherence
- **Write the Coherence refill rule** [03 04 06 07 09 10].
- **Consider a per-character Coherence draw limit** so one Body-D build can't
  drain it alone [09].
- **Make sure Coherence 0 isn't a full heal.** Being torn into the next realm
  currently refills every pool and returns all lost Stuff [06 10]. Options:
  arrive with pools at half; carry a scar tag; Coherence returns only to 3;
  everyone arrives with one pool empty [06 10].

### Stats and pools
- **Stats count as both dice and health,** which makes Stat-heavy columns
  (Body) doubly valuable. See Body A balance [02].

---

## Character Advancement (`06-advancement.tex`)

- **Define how Change Points and Persistence Points are earned.** They're the
  natural answer to "my Hacking skill is dead here" and "keep my dog a dog",
  and neither can currently be earned [06 08].
- **Spending a Persistence Point to keep a deck a deck is a trap:** it becomes
  a useless brick in a realm with no network [06].
- **Let living companions re-skin within their kind** (a dog stays some kind
  of creature or creature-like machine) without a Persistence Point [08].
- **Use Change Points (or a scene of adapting) to wake dormant tags** after a
  crossing (see Realms) [06].

---

## The Shape of a Session (`12-playing.tex`)

- **Typo in the Degrees of Success table:** the Critical row says it overrides
  every tier "above"; the prose and logic say *below* [03].
- **Conflicts' "display of strength rolls Body against Face"** contradicts
  Magic (see How to Play) [10].

---

## For the Game Master (`13-gming.tex`)

- **Write the target-number section first** — every playtester flagged
  this. Suggested ladder: **1 = routine, 2 = hard, 3 = heroic, 4+ =
  legendary**, with notes on how it plays against pools of 3, 6 and 10
  [all; ladder from 02 03 10].
  - Crits are very common at the cap: 10 dice vs target 1 crits ~52% of the
    time; vs target 2, ~22% [03].
  - Expected successes: 5 at 10 dice, 3.5 at 7, 2 at 4, 1 at 2 [05].
- **Let information, positioning and Feats lower the target,** not only grow
  the pool. That gives surplus tags and Feats a job once the cap is
  reached [03 06].
- **Say when reframing the approach is legitimate.** A Face-5 grifter can turn
  most obstacles into 10-die social rolls [03].
- **Give rules for `Staffed` followers:** can they act on their own, run
  errands, fight? [03]
- **Replace the Coherence-0 "reliable go-to"** (tear into the next realm) with
  something that isn't a full heal [06 10].
- **Add a guideline on when a construct has a will** [06].
- **If a Monstrous Complication is added,** give guidance on invoking it [02].

---

## The Realms (`08`–`10`) and Travel Between Realms

- **Fill in the placeholder chapters.** Almost every realm question ran into
  lorem ipsum: Travel Between Realms, Body/Magic in Cyberpunk, realm reskin
  tables [02 03 04 05 06 07 09].
- **Write a procedure for the crossing itself** — especially an involuntary
  one. Right now there's no roll, no cost, no decision point [06].
- **Make crossing cost something.** On arrival, any tag whose domain doesn't
  exist in the new realm goes **dormant** until re-skinned through play
  (a scene of adapting, a roll, or a Change Point). Dragging a hacker into
  High Fantasy currently costs zero dice — the biggest miss for a game about
  "who are you when the world changes?" [06]. (Only bites if tag counts are
  also rebalanced; Magic A is otherwise immune [06].)
- **Say who decides a re-skin** — the player (Stuff chapter) or a default
  mapping (the Advancement "motorcycle becomes a horse" example) — and
  whether a player can refuse one without a Persistence Point [06].
- **Cyberpunk** [04 06]:
  - add a reskin table;
  - say where chrome goes (see Body);
  - map the `Magic` Form per realm — where magic is hacking it arguably covers
    all code [06];
  - say whether the `Hacking` skill and hacking-as-magic stack, and what
    magic-hacking can do that the skill can't (e.g. only Magic can use Weird
    on systems, grant Feats, or touch un-networked targets) [04 06];
  - note that Weird rarely applies in the sprawl, since almost every digital
    effect has a system pushing back [03].
- **Give one worked example per realm of non-elemental magic re-dressing**
  (e.g. "food magic in Cyberpunk: synth-flavour hacking, vat-grown
  conjuring") [09]. Say whether a tea-leaf witch's tags change look [07].
- **Re-skinning can change which Stat applies:** healing a dog is Weird,
  repairing a drone may be Mind [08].
- **Re-kitting can strand a skill** (a Tier-2 Weapon becoming a bow no longer
  fits `Firearms`); remind players they can pick any item of the same rank [05].
- **High Fantasy: *Appeal to the Gods* has no mechanic** [04].
