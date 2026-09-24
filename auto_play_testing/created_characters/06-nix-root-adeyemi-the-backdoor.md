# Nix "Root" Adeyemi, the Backdoor

*Built by: subagent, seed: Someone native to the cyberpunk sprawl whose "magic" is hacking and chrome. Specifically stress-test what happens when they get dragged into the High Fantasy realm and everything re-skins, 2026-09-23.*

*Rules source: `rulebook.tex` + `chapters/`.*

## Concept

Nix grew up in the crawlspaces under a megacorp arcology. They learned to
code before they learned to read, and at fourteen a back-alley ripperdoc
put a jack in the base of their skull. Since then Nix has lived in the net:
they slip into buildings through the air conditioning's control code,
drive stolen drones and wipe themselves off every camera feed. In the
flesh they're pale, twitchy and bad with people. They trust a system more
than a face, because a system always does what its rules say.

Then the wound in the world opened under a data-centre raid, and Nix fell
through into a land with no electricity, no network and no rules they can
read. The deck in their hands turned into a slate of carved sigils. The
jack in their skull turned into a brand that burns when they touch an
enchanted thing. The question the character exists to answer is: *is a
hacker still a hacker when there's nothing left to hack?*

## Priorities

| Column | Letter | Rank |
|---|---|---|
| Magic  | **A** | 4 |
| Stuff  | **B** | 3 |
| Body   | **C** | 2 |
| Skills | **D** | 1 |

The letter-to-rank mapping (A=4 … D=1) isn't stated outright anywhere.
It's inferred from the Priority Matrix prose matching each column's rank
table (e.g. Magic A "fucking wizard" = Magic rank 4).

## Stats

Stat Points: Body rank 2 → **4**, Skills rank 1 → **0**. Total **4**.
All Stats start at 1.

| Stat | Raise | Cost |
|---|---|---|
| Body | 1 → 2 | 1 |
| Mind | 1 → 2 → 3 → 4 | 1 + 1 + 1 = 3 |
| Face | stays 1 | 0 |
| **Total** | | **4 / 4** |

- Mind 5 was out of reach: 1→4 costs 3, and the doubled fifth pip costs 2
  more, so 5 points total. Nix only has 4.
- **Body 2 · Mind 4 · Face 1**
- **Weird 3** (Magic 4 − 1)
- **Pools:** Body 2 / Mind 4 / Face 1. Weird has no pool.

## Body Tag (1, from Body rank 2)

- `Neural Jack` (custom, GM-approved). *Home form:* a skull-jack plus
  wetware that lets Nix plug straight into machines and feel their
  systems as a sense. It adds a die when Nix is physically interfacing
  with a system.

Chrome is an interesting case. The Body chapter says Body Tags are
"inherent. No one can steal them," which fits a skull-jack better than
calling it gear, so it goes here rather than in Stuff.

## Skills (4, from Skills rank 1)

- `Hacking` (Mind), `Perception` (Mind), `Stealth` (Body), `Craft` (Mind)

## Magic (12 tags, Weird 3, 2 Feats): netrunning

The Cyberpunk chapter says Magic *is* hacking there, so all of Nix's
hacking lives here.

- **Techniques (4):** `Perceive` (read systems), `Control` (override, take
  command), `Destroy` (crash, brick, fry), `Transform` (rewrite code,
  spoof)
- **Forms (3):** `Magic` (in a realm where magic = hacking, "raw magical
  power itself; the stuff of spells" reads as *code itself*), `Image`
  (spoofed feeds, AR overlays, holograms), `Mind` (AIs, as "incorporeal
  spirits")
- **Specific (5):** `Networks`, `Drones`, `Locks` (electronic locks and
  access control), `Surveillance` (cameras, trackers, sensor grids),
  `Lightning` (overloading circuits, arcing power)

Count: 4 + 3 + 5 = **12** ✔

- **Magic Feat 1: Turn Invisible** (Action). *Ghost Protocol*: Nix wipes
  themself out of every camera, optic implant and sensor feed nearby.
- **Magic Feat 2: Read Minds** (Action). *Wetware Sniffing*: Nix reads
  the surface signals leaking from a person's neural implants.

## Stuff (7 points, 4 tags, 1 Feat, Lifestyle: Well Off)

Max Tier 3. Nothing bought above rank 3.

| Item | Category | Tier | Cost | Tags |
|---|---|---|---|---|
| **The Mongrel**, a hand-built cyberdeck | Gadget ("breaks into digital systems") | 3 | 3 | `Adaptive`, `Hard-to-Trace` |
| **Smartlink holdout pistol** | Weapon | 2 | 2 | `Concealable` |
| **Armoured hoodie** | Light Armour | 2 | 2 | `Discreet` |

- Points: 3 + 2 + 2 = **7 / 7** ✔
- Tags: 2 + 1 + 1 = **4 / 4** ✔ (`Adaptive` and `Hard-to-Trace` come from
  the Lockpick Rig / Signal Jammer example tags, which fit a deck)
- **Stuff Feat: See Through Solid Matter** (Action). *Scanner Rig*: a
  terahertz overlay implanted in Nix's left eye. The Feat catalogue's
  item text allows "implanted". It's treated as a free prop that comes
  with the Feat (same ruling as Tamsin's Loupe).
- **Lifestyle: Well Off** (automatic at rank 3, no points spent). Good
  clothes, spending money, good tools.

## Feat Total

Magic 4 → 2, Stuff 3 → 1, Body 2 → 0, Skills 1 → 0. **3 Feats**: Turn
Invisible, Read Minds, See Through Solid Matter.

---

## Arrival: the Re-Skin in High Fantasy

This is the heart of the seed. Every line on the sheet, and what the rules
say happens to it:

| Sheet line | Sprawl form | High Fantasy form | Rule that governs it | Clear? |
|---|---|---|---|---|
| Stats / pools | — | unchanged; pools refill to full on arrival | *Recovering Your Pools* | ✔ |
| `Neural Jack` | skull-jack | **Sigil-Brand**: a rune-scar that burns when Nix touches enchanted things and lets them feel how a working is built | Body Tags "stay exactly as powerful, even as they take on a new shape" | Partly. See Issue 2 |
| `Hacking` skill | netrunning, electronics | **???** | *No re-skin rule exists for Skills* | ✘ See Issue 1 |
| `Perception`, `Stealth`, `Craft` | — | unchanged, all make sense | — | ✔ |
| Magic tags | code | sorcery: `Networks` → ley lines, `Drones` → constructs/golems, `Surveillance` → scrying wards, `Locks` → locks & wards, `Lightning` → lightning, `Magic` → literally magic | "decide together what Magic looks like there"; tags "re-dress themselves" | Techniques and Forms yes, Specifics no. See Issue 4 |
| Turn Invisible | ghosted off camera feeds | an invisibility glamour | Feats re-skin, "function identically" | Mechanically ✔, fictionally strained. See Issue 7 |
| Read Minds | sniffing neural implants | plain telepathy (no one here has implants) | same | same |
| The Mongrel (Gadget 3) | cyberdeck | **Sigil-Slate**: a slate of carved runes that "reads" a ward. The Gadget examples even list a *Cipher Wand* | *Re-Kitting on Arrival* | ✔ (but see Issue 3 on who decides) |
| Pistol (Weapon 2) | smartlink holdout | hand crossbow, sleeve-hidden | reskin table: Weapon 2 = "sturdy blade or hunting bow" | ✔ |
| Hoodie (Light Armour 2) | armoured hoodie | quilted gambeson under a traveller's cloak | Armour example list | ✔ (fantasy reskin table omits Armour, though) |
| Terahertz eye | implant | a seer's crystal monocle, or the eye just turns milky-silver | Stuff Feat re-skins "along with the rest of your gear" | ✔, but an implant being "gear" is odd. See Issue 2 |
| Lifestyle | eddies | a purse of silver | — | ✔ |

---

## Four Scenarios

### 1. Cyberpunk: the vault under Hesketh Tower (Mind, home turf)

Nix jacks into a maintenance port three floors below Hesketh-Amaro's
data vault. They need to get through the building's ICE, take over the
vault's maglock and pull one file without tripping the trace.

- **What resists:** a system → **Mind**.
- **Base:** acting through the Mongrel → Max(Tier 3, Mind 4) = **4**. The
  deck's tier contributes nothing, because Nix's own Mind is higher.
- **Candidate tags (10):** `Hacking`, `Neural Jack` (physically jacked
  in), `Control` (take the maglock), `Destroy` (crash the ICE),
  `Perceive` (find the file), `Networks`, `Locks`, `Magic` (code as
  magic), `Adaptive` (unfamiliar ICE), `Hard-to-Trace` (the trace is
  part of the stakes)
- **Applied (5, at the cap):** `Hacking` + `Neural Jack` + `Control` +
  `Locks` + `Networks`
- **Pool: 9 dice.** Five applicable tags are left over. The cap is the
  only thing keeping this from being a 14-die roll.

### 2. High Fantasy: the bronze warden (Mind, then Weird)

Day two in the new realm. A temple golem, bronze and humming with
binding-runes, is walking toward the party's fighter, who is pinned under
rubble. Nix slaps the Sigil-Slate against its chest plate and tries to
"hack" it.

**Roll A: breaking its bindings.**

- **What resists:** the table's AI row says Face "if the AI has a will of
  its own; Mind if it is only rules to outwit." The GM rules that a golem
  is only rules → **Mind**.
- **Base:** through the Sigil-Slate → Max(Tier 3, Mind 4) = **4**
- **Generous re-skin ruling** (Specific tags, Body tag and Skill all
  translate):
  `Control` + `Magic` ("beings made from it", which is literally a golem) +
  `Drones` → constructs + `Neural Jack` → Sigil-Brand (hand on the runes)
  + `Adaptive` (a very unfamiliar lock) = **5 at the cap**, with `Hacking`
  and `Locks` left over → **9 dice**
- **Strict re-skin ruling** (only Techniques/Forms re-dress; Specifics,
  the custom Body Tag and `Hacking` stay literal, and there's no
  electronics here): `Control` + `Magic` + `Adaptive` + `Destroy`
  (unmaking the binding) + `Perceive` (reading the rune-lattice) = **still
  5** → **9 dice**
- **Result: 9 dice either way.** With 12 Magic tags, the tag cap soaks up
  everything the re-skin takes away. See Issue 5.

**Roll B: riding it.** Nix pushes their mind into the now-open golem.

- **What resists:** the table says "Upload your mind into an unsecured
  drone" is Weird, and after Roll A it's unsecured → **Weird 3**. No item
  tier applies (the rules never say an item can stand in for Weird).
- **Tags:** `Control` + `Magic` + `Mind` (Nix's own mind moving) +
  `Drones` (generous ruling) + `Neural Jack` (generous ruling) = **5**.
  Under the strict ruling it's `Control` + `Magic` + `Mind` = 3.
- **Pool: 8 dice** (generous) / **6 dice** (strict).
- **Then** Nix, driving the golem, heaves the rubble off the fighter.
  That's Body, "the rubble resists," through an object: Max(golem's tier,
  Body 2). **The rules give no tier for an object you don't own.** The
  GM has to invent one. The same goes for what happens to Nix's Body pool
  if someone smashes the golem while Nix is riding it. See Issue 9.

### 3. High Fantasy: bandits on the King's Road (Body, with a Feat)

Night ambush. Six bandits, one with a crossbow trained on the party's
cart. Nix triggers **Turn Invisible**, creeps around the treeline, and
then drops a lightning bolt on the crossbowman.

- **Turn Invisible:** a Feat, so no roll. The cyberpunk fiction ("ghosted
  off camera feeds") doesn't work against bandits with ordinary eyes, but
  Feats "function identically regardless of source," so Nix vanishes
  anyway.
- **Roll A: the creep.** The Magic chapter says sneaking while invisible
  is "whatever sneaking always is." Base **Body 2** (as the Skills list
  defaults; "what resists?" gives no clean answer for being unseen).
  Tags: `Stealth` = 1. **Pool: 3 dice**, exactly what a visible Nix would
  roll. The Feat changed nothing on the dice. Whether it lowers the
  target number is up to the GM, and *Setting the Target Number* is
  still lorem ipsum.
- **Roll B: the bolt.** Striking a body → **Body 2**. Nix could fire the
  Tier-2 hand crossbow instead: Max(2, 2) = 2 with no applicable tags,
  because they have neither `Archery` nor `Firearms`, and `Concealable`
  only applies to *hiding* the weapon. Casting is better:
  `Destroy` + `Lightning` = 2. Does the lightning give away Nix's
  position? Almost certainly: "a fast dash or a shout gives you away."
- **Pool: 4 dice.** A Magic-A hacker is a weak fighter, as intended. If
  the crossbowman hits back, a Body pool of 2 takes two hits before Nix
  is at −1 die.

### 4. Space Adventure: DOCKMOTHER says no (Face)

Station *Calliope*'s docking intelligence, DOCKMOTHER, has locked the
party's shuttle in its clamps over an unpaid tariff. This one is a
sapient AI, proud and prickly. Nix wants to talk it into letting them go.

- **What resists:** the AI has a will of its own → **Face 1** (per the
  table). Nix argues for Mind; the GM says no.
- **Can the deck lend its tier?** The Mongrel (re-skinned as a
  quantum-lattice slate) is what Nix is talking *through*. *Stats from
  Objects* doesn't restrict which Stat an item can replace: "compare
  that item's own tier to whichever base Stat the action would normally
  use." Read literally → Max(Tier 3, Face 1) = **3**. Read in spirit (a
  deck isn't a charm school) → **1**. See Issue 8.
- **Tags:** `Hacking` ("other Stats may apply if the fiction supports
  it") + `Control` (compel) + `Mind` (AI as an incorporeal spirit) +
  `Networks` + `Neural Jack` (jacked into the dock port) = **5, at the
  cap**. `Read Minds` doesn't add dice; it just tells Nix that
  DOCKMOTHER is lonely.
- **Pool: 6 dice** (Face 1 + 5) or **8 dice** (deck tier 3 + 5).
- **Risk:** Face pool 1. One failure puts Nix at Face 0 and −1 die on
  every Face roll in this realm until something repairs their standing,
  because rest won't. Even so, the socially worst character in the party
  rolls 6–8 dice here, because tags outweigh the Stat.

---

## Things Noticed While Building

### Re-skinning gaps (the seed's focus)

1. **Skills have no re-skin rule.** Body Tags, Magic tags, Stuff and
   Feats each get explicit "re-skins in a new realm" text. Skills get
   nothing, except the Intro's "Your skills travel with you." That leaves
   `Hacking` ("Electronics, security systems, and information networks")
   in High Fantasy as either (a) dead, (b) partially alive via "security
   systems" = locks and wards, or (c) re-skinned to something like
   `Warding`. The *Your First Skill* example (Craft covers lockpicking)
   suggests (b), but it's GM fiat. Realm-bound skills (`Hacking`,
   `Piloting` a starship, and so on) need a stated rule, especially
   since Change Points, the obvious fix, have no rule for how you earn
   them.
2. **Chrome has no home column.** A cyber-eye can be a Body Tag ("can't be
   stolen"), a Body Feat ("Deep-Spectrum Eyes"), or a Stuff Feat ("Scanner
   Rig ... implanted"). The Stuff chapter's own example is "a translator
   implant". The choice matters: Stuff can be "smashed, stolen, or left
   behind" (so implants can be ripped out) and comes back free next
   realm, while Body can never be lost. Cyberpunk is where players will
   ask this first, and the Cyberpunk chapter's "Body in Cyberpunk"
   section is lorem ipsum.
3. **Who decides the re-skin?** *Re-Kitting on Arrival* says "you decide
   what that thing actually is." The Advancement example says your
   motorcycle "ordinarily … would become a horse," which implies a
   default mapping. The High Fantasy reskin table is "a starting point."
   *Travel Between Realms* is lorem ipsum, so an involuntary drag gives
   no procedure at all. It's also unclear whether a player can *refuse*
   a re-skin without spending a Persistence Point. And fixing the deck
   as a deck with a Persistence Point is a trap: it becomes a useless
   brick in a realm with no network.
4. **Specific Magic tags have no parent for hackers.** Specifics must be
   "more specific in application than the Techniques and Forms", but no
   Ars Magica Form covers machines, data or electricity. So what are
   `Networks`, `Drones` and `Locks` narrower *than*? `Lightning` has two
   possible parents (`Fire` "heat and light" vs. `Air` "weather"). Worse,
   nothing says whether a Specific keeps its *scope* when it re-skins:
   `Networks` touches everything in the sprawl, but its fantasy form,
   "ley lines," could touch almost nothing. Body Tags promise to "stay
   exactly as powerful"; Magic tags and custom Body Tags don't get a
   matching promise that actually holds in play (`Neural Jack` only
   survives if the GM lets it become the Sigil-Brand).
5. **For Magic A, re-skinning costs nothing.** In Scenario 2 the strict
   and generous rulings both land on 9 dice, because 12 tags vs. a
   5-tag cap leaves 7 spares. Realm-shock only hurts characters with few
   tags. That's probably backwards if the game wants arrival in a
   strange realm to feel disorienting, and it means the most
   "setting-bound" concept (a hacker) is barely affected by losing its
   setting.
6. **The `Magic` Form's scope depends on the realm.** Where "Magic is
   hacking," the Form described as "raw magical power itself; the stuff
   of spells" arguably covers *all code*, which is almost every roll in
   the sprawl. In High Fantasy it covers golems, wards and spells. A
   single Form tag that becomes near-universal in one realm should be
   called out, or the Cyberpunk chapter should say what it maps to.
7. **Feat mechanics beat Feat fiction, but the book never says so for
   this case.** Ghost Protocol (camera-wiping) and Wetware Sniffing
   (implant-reading) only make sense against chromed targets, yet "a
   Feat functions identically regardless of source," so they work on
   fantasy peasants and even on un-chromed sprawl-dwellers. That's
   probably right, but the rules should say outright that "mechanics
   hold, and the fiction bends to fit."

### Other ambiguities / gaps

8. **Item tier can replace *any* Stat.** Nothing restricts which Stat
   *Stats from Objects* applies to. A Tier-3 deck used as the channel
   for a Face roll (Scenario 4) lifts Face 1 to 3. The same argument
   covers a Tier-4 "Luxurious" car for seduction or a Fortress for
   intimidation. The rule should limit tier to the Stat the item actually
   *does the work of*.
9. **Objects you don't own.** *Stats from Objects* covers "a car, a rifle,
   a warhorse", not just your own Stuff, but gives no guidance on the
   tier of a hijacked golem, a stolen drone or a borrowed terminal. The
   spell table says "a terminal's tier can stand in for your Mind"
   without saying who sets that tier. And while Nix rides the golem,
   whose Body pool takes the damage?
10. **Hacking the skill vs. hacking the Magic.** In Cyberpunk, a Magic-D
    character with the `Hacking` skill and a Magic-A netrunner both roll
    Mind for the same mainframe, and the netrunner stacks the skill *on
    top of* their hacking-magic tags. The book never says what
    "magic-hacking" can do that "skill-hacking" can't (Weird uploads? Feats?).
    Without that, the Hacking skill is either redundant for netrunners
    or a cheap substitute for Magic.
11. **The deck is the netrunner's worst item.** With Mind 4, the Tier-3
    deck never supplies the base (Scenario 1). The Magic chapter's
    showcase rule ("hacking … through a computer terminal uses the
    terminal's tier") helps the party's *bruiser* far more than the
    hacker. For Nix, 3 Stuff Points bought 2 tags. That's a general
    problem (item tier is dead weight for high-Stat characters), and it's
    at its worst for the archetype the rule was written around.
12. **Is a cyberdeck a Gadget?** Gadgets do "one specific, useful thing"
    and the book warns against "a spell wearing a disguise." A deck that
    lends its tier to *every* hacking roll is exactly that. Gadget,
    Weapon, or a new "Tool/Interface" category? The book's own "cutting
    deck" example in *How to Play* suggests decks were intended, but no
    category fits.
13. **Feats don't touch dice or targets.** Invisible Nix sneaks with the
    same 3 dice as visible Nix (Scenario 3). Unless the GM lowers the
    target (no guidance exists), Turn Invisible is purely narrative. A
    line like "a Feat that fits the action lowers the target by 1, or
    makes the roll unnecessary" would fix it.
14. **Coherence 0 is a reward, not a catastrophe.** The GM chapter's
    "reliable go-to" for Coherence 0 is tearing the party into the next
    realm. But entering a new world refills every pool to full *and*
    returns all lost Stuff at full Tier. A party on the ropes should
    *want* to crash Coherence. (Coherence's own refill is still a `\todo`.)
15. **Mind vs. Face for constructs and AIs is a lever the player can
    pull.** "Has a will of its own" is a GM call, and a Face-1 hacker
    will always argue that the golem or AI is "only rules." The table
    has one AI row. It needs a rule of thumb, e.g. "if it can be
    persuaded, it's Face."

### Balance concerns

- **Weird 3 + 5 tags = 8 dice.** The book reassures that "Weird never
  rises above 3, so a wizard who wants to move boulders *reliably* still
  does best to get strong." For a Magic-A character with 12 tags that
  reassurance doesn't hold: Nix's Weird-based golem upload rolls 8 dice,
  while their Body 2 punch rolls 2–4. The Weird cap is meaningless once
  tags fill the cap.
- **Face 1 still rolls 6+ dice** whenever the target is a machine with a
  will. With enough broad tags, a dump Stat stops being a real
  weakness. The only thing that bites is the pool of 1 (one failure →
  permanent −1 until the fiction repairs standing).
- **The 5-tag cap does all the balancing for Magic A.** In three of
  four scenarios Nix had 5+ applicable tags and at least 2 left over.
  Tags Known 12 mostly buys *coverage* (always hitting 5), not bigger
  pools. That's fine, but the rank-4 Magic table's 12 feels like far
  more than needed, especially compared with Skills A's 14, where every
  skill is narrower.

---

## Reflection on the Build Process

### What seemed good

- **Building was fast and easy to audit.** Every column is a fixed
  budget read straight off one table: points, tags, Feats. Nix went
  from concept to finished sheet in about ten decisions, and every
  number on the sheet traces back to a single table row. The arithmetic
  sections above are short because the system is.
- **The double-cost fifth pip bites at exactly the right moment.** With
  4 Stat Points, "Mind 5 or Mind 4 plus Body 2?" was a real choice with
  a real cost. That one rule does a lot of work.
- **"What resists?" is a good question.** It settled the golem breach
  (Mind), the upload (Weird), the rubble (Body) and the AI (Face)
  quickly, and each answer felt earned rather than looked up. The
  spell table's edge cases (unsecured drone = Weird, secured = Mind
  first) mapped straight onto a fantasy golem. That's strong evidence
  the principle generalises across realms.
- **One tag, one die, whatever the source.** Stacking a skill, a Body
  tag, an item tag and magic tags on one roll never needed a special
  case. The 5-tag cap is simple and nearly impossible to get wrong at
  the table.
- **The Stuff catalogue re-skins well.** Weapon 2 → hand crossbow and
  Gadget 3 → Sigil-Slate both took seconds, and the Gadget example list
  already had a *Cipher Wand* waiting. The "a kind of thing, not a
  specific thing" design works.

### What seemed bad

- **Tags swamp Stats.** Nix's Face 1 rolled 6–8 dice and Weird 3 rolled
  8. Once a character has broad tags, the Stat is mostly a tiebreaker,
  and the one place a low Stat really shows is the size of its pool.
  That undercuts both "magic expresses who you are via Body/Mind/Face"
  and the "get buff to move boulders" answer.
- **12 Magic tags against a 5-tag cap is mostly waste.** In three of four
  scenarios Nix had spare tags. Magic A doesn't buy bigger pools; it
  buys never missing the cap, plus immunity to losing tags on re-skin.
  That makes Magic A feel better on paper than in play, and it removes
  the pressure the seed was meant to test.
- **Item tier is dead weight for the specialist.** The netrunner's
  signature deck never set the base. 3 Stuff Points bought 2 tags. The
  archetype the terminal rule was written for gets the least from it.
- **Feats sit outside the dice engine.** Turn Invisible and Read Minds
  changed nothing about any roll. They're cool as flavour, but they
  have no mechanical hook, so a Feat's value depends entirely on how
  generous the GM is.
- **Too much of the realm material is placeholder text.** The seed asked
  me to stress-test High Fantasy and Cyberpunk. Both chapters are
  mostly lorem ipsum, and the Cyberpunk chapter has no reskin table at
  all. The core question ("what does chrome become?") had no text to
  test against.

### What was cool

- **The re-skin table was the best part of the exercise.** Walking each
  sheet line through the realm shift (jack → Sigil-Brand, deck → rune
  slate, camera-ghosting → glamour) made a strong character moment.
  The fiction of "Nix trying to read a golem like code" came straight
  out of the rules.
- **The golem scenario played beautifully.** Breach (Mind), then upload
  (Weird), then heave the rubble through the golem (Body, via an
  object) is a three-step sequence where each step used a different
  Stat for a principled reason. It's the best showcase of the engine I
  found.
- **Realm-relative magic is a great idea.** "Magic is hacking here,
  sorcery there" gives a hacker a real reason to be the party's wizard
  after the crossing. The concept almost builds itself.
- **Face 0 and "rest doesn't restore Face"** made Nix's social weakness
  feel like a lasting story fact rather than a number.

### What was disappointing

- **The seed's premise didn't bite mechanically.** I expected getting
  dragged into fantasy to hurt a hacker, with lost tags, a useless
  skill and a scramble to adapt. Instead it cost Nix zero dice. The
  interesting tension exists only in the fiction. For a game built
  around "what kind of person are you when the world changes?", that's
  the biggest miss I found.
- **There's no procedure for the crossing itself.** *Travel Between
  Realms* is lorem ipsum, so the moment the seed centres on (being
  dragged through) has no rules: no roll, no cost, no decision point.
- **Change and Persistence Points have no rules for earning them.** The
  natural answer to "my Hacking skill is dead here" is a Change Point,
  and the natural answer to "keep my deck a deck" is a Persistence
  Point. Neither can actually be earned, so the advancement system
  can't be tested.
- **Custom tags are balanced only by GM taste.** The printed Body Tags
  come in carefully weighted pairs, but the cyberpunk archetype needs
  custom ones (`Neural Jack`), and there's no guidance on sizing or
  re-skinning them.

### What was unclear

- Whether Skills re-skin, and who decides any re-skin: player, GM or a
  default table (Issues 1 and 3).
- Where chrome belongs: Body, Stuff or Feat (Issue 2).
- What a Specific tag must be narrower *than* when no Form covers the
  domain, and whether it keeps its scope when it re-skins (Issue 4).
- Which Stats an item tier may replace, and what tier an object you
  don't own has (Issues 8 and 9).
- What magic-hacking does that the Hacking skill doesn't (Issue 10).
- Whether Action Feats need a roll, and whether a Feat ever changes a
  target number (Issue 13).
- The letter-to-rank mapping (A=4 … D=1). I had to infer it.
- How to judge "has a will" for constructs and AIs (Issue 15).

### Recommendations to improve the system

1. **Make realm-crossing cost something mechanically.** On arrival, any
   tag (skill, Body, Magic Specific, item) whose domain doesn't exist in
   the new realm goes **dormant** until the player re-skins it through
   play: one scene of adapting, a roll, or a Change Point. Pair this
   with an explicit rule: *mechanics hold, and the fiction bends to
   fit*. That gives the game's central premise a real moment at the
   table instead of a free cosmetic swap. It also fixes the "Magic A
   is immune" problem only if paired with #2.
2. **Rebalance tag counts against the 5-tag cap.** Either cut Magic 4 to
   around 8–9 Tags Known and Skills 4 to around 10, or let tags beyond
   the cap do something (e.g. every 2 spare applicable tags lowers the
   target by 1). Separately, cap the number of tags on a Weird roll at
   the Weird value itself (so the pool maxes at 6 at Weird 3). Then
   "Weird tops out low, so strength still pays" is actually true.
3. **Limit and sharpen item tier.** An item's tier replaces only the
   Stat for the work the item physically does (a deck for hacking, not
   for charming an AI). Let tier add +1 die when it's *below* your Stat,
   so the specialist's signature gear always matters. And say that
   unowned objects use a GM-set tier from 1 to 4, with a one-line
   guideline.
4. **Give Feats a hook into the roll.** When a Feat clearly applies to
   an action, either skip the roll or lower the target by 1. That makes
   Turn Invisible matter for sneaking without inflating dice pools.
5. **Write the missing rules the cyberpunk archetype needs.** Say where
   chrome goes (recommend: "your choice of Body Tag or Stuff; Body can't
   be lost, Stuff can be upgraded"). Add a Cyberpunk reskin table and a
   sentence on skill-hacking vs. magic-hacking (e.g. only Magic can use
   Weird on systems, grant Feats or touch un-networked targets).
   Finally, give the `Magic` Form a mapping per realm.
6. **Close the Coherence loophole.** If Coherence 0 drags the party into
   the next realm, don't give them a full pool refill and all their lost
   Stuff back. Arrive with pools at half, or carry a scar tag. Otherwise
   the catastrophe is the best healing in the game.
