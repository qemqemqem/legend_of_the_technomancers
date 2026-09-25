"""Published character budgets and dice rules, with finite play-test menus."""

import itertools
import math
import random


COLUMNS = ("Body", "Stuff", "Skills", "Magic")
STATS = ("Body", "Mind", "Face")
BODY_STAT = (0, 1, 2, 3, 5)  # Body rank sets the Body Stat directly
BODY_TAG_COUNTS = (0, 0, 1, 2, 4)
SKILL_POINTS = (0, 0, 2, 4, 6)  # spent on Mind and Face only
SKILL_COUNTS = (0, 2, 4, 6, 9)
STUFF_POINTS = (0, 0, 3, 6, 10)
STUFF_TAG_COUNTS = (0, 0, 2, 4, 7)
MAGIC_COUNTS = (0, 0, 3, 7, 12)

BODY_TAGS = ("Strong", "Natural Weapon", "Fast", "Graceful", "Tough", "Regenerating",
             "Keen Senses", "Camouflage", "Striking", "Intimidating")
SKILLS = ("Blades", "Brawling", "Firearms", "Archery", "Athletics", "Stealth",
          "Piloting", "Persuasion", "Deception", "Intimidation", "Performance",
          "Lore", "Medicine", "Perception", "Languages", "Craft", "Survival", "Hacking")
TECHNIQUES = ("Create", "Perceive", "Transform", "Destroy", "Control")
FORMS = ("Animal", "Water", "Air", "Body", "Plant", "Fire", "Image", "Mind", "Earth", "Magic")
SPECIFICS = ("Gems", "Smoke", "Thorns", "Hearing", "Reading", "Protection", "Throwing", "Flying")
GEAR_TAGS = {
    "Weapon": ("Ranged", "Reach", "Rapid-Fire", "Returning", "Concealable",
               "Silent", "Piercing", "Explosive", "Elemental", "Disarming"),
    "Vehicle": ("Fast", "Agile", "Armoured", "Rugged", "Spacious", "Amphibious",
                 "Airborne", "Silent", "Armed", "Luxurious"),
    "Armour": ("Impact-Resistant", "Fireproof", "Sealed", "Insulated", "Flexible",
               "Lightweight", "Discreet", "Imposing", "Self-Repairing", "Anchored"),
    "Location": ("Fortified", "Hidden", "Watchful", "Connected", "Stocked",
                 "Workshop", "Welcoming", "Staffed", "Escape Route", "Commanding"),
}
GADGET_TAGS = {
    "Grappling Hook": ("Long-Range", "Strong Line", "Quick-Firing", "Retractable"),
    "Lockpick Rig": ("Precise", "Quiet", "Compact", "Adaptive"),
    "Signal Jammer": ("Wide-Area", "Selective", "Portable", "Hard-to-Trace"),
    "Nanite Patch Kit": ("Rapid", "Antitoxin", "Bone-Mending", "Reusable"),
}
GEAR_NAMES = {
    "Weapon": {2: ("Sword", "Pistol", "Sidearm"),
               3: ("Enchanted Blade", "Shotgun", "Plasma Cutter"),
               4: ("Legendary Blade", "Signature Sidearm", "Superweapon")},
    "Vehicle": {2: ("Warhorse", "Motorbike", "Hoverboard"),
                3: ("Covered Wagon", "Family Car", "Cargo Skiff"),
                4: ("War-Chariot", "Race Car", "Gunship")},
    "Armour": {2: ("Leather Jerkin", "Reinforced Jacket", "Impact-Weave Bodysuit"),
               3: ("Plate Harness", "Riot Gear", "Exo-Frame"),
               4: ("Dragon-Scale Mail", "Combat Suit", "Void-Rated Armour")},
    "Location": {3: ("Hidden Tower", "Safehouse", "Satellite Relay"),
                 4: ("Castle", "Corporate Compound", "Orbital Station")},
    "Gadget": {2: ("Grappling Hook", "Lockpick Rig"),
               3: ("Signal Jammer",), 4: ("Nanite Patch Kit",)},
}
GADGET_EFFECTS = {
    "Grappling Hook": "fires a hook and cable to haul things within reach",
    "Lockpick Rig": "picks and probes that open locks",
    "Signal Jammer": "blocks outside detection while running",
    "Nanite Patch Kit": "closes wounds, mends breaks, or purges poison",
}
FEATS = ("Fly", "Read Minds", "Form Shadow", "Needs No Air", "Never Sleep",
         "Speak with Animals", "Walk Through Walls", "Turn Invisible",
         "See Through Solid Matter", "Blink")

# Themes only balance the sample; the model chooses its base independently.
# Targets are experimental, not an as-yet-unwritten GM difficulty table.
SCENES = (
    ("Body", "At a crowded river crossing, a {foe} blocks the bridge while a merchant's cart waits in line. "
     "A half-empty ferry is tied to the downstream bank."),
    ("Body", "In the inn courtyard, a fallen {weight} pins a traveller and the innkeeper struggles "
     "to hold back onlookers. A hitched draft horse and a coil of rope stand nearby."),
    ("Body", "On a {terrain}, the ground gives way beneath a line of travellers. "
     "A scout has marked a firmer route and an abandoned supply sled stands nearby."),
    ("Body", "A merchant's caravan is trapped on a narrow road by an armed {foe} and two accomplices. "
     "A rocky side path skirts the roadblock and a cart horse paws at its harness."),
    ("Body", "Smoke fills a workshop whose roof is buckling above the workers. "
     "An open loading bay leads outside, and a water trough sits near the wall."),
    ("Body", "A scout waits across a {terrain} with heavy cargo as the weather worsens. "
     "An old winch and an intact service track are visible near your side."),
    ("Body", "At a ferry landing, a loose crate rolls toward a child as a boat begins to drift away. "
     "A deckhand holds a pole, and the gangplank is still within reach."),
    ("Body", "A pack animal bolts through the market with supplies trailing behind it. "
     "The owner calls out, and a side alley runs beside the crowded square."),
    ("Body", "On a frozen lake, cracks spread under a supply team carrying medicine. "
     "A rescue rope lies near a sled, and the far bank has low trees."),
    ("Body", "A jammed lift hangs halfway up a tower with workers inside. "
     "Its counterweight is visible through a grate, and a stairwell reaches the next landing."),
    ("Mind", "In the archives, the {barrier} has been sabotaged and repair records are out of order. "
     "A guard has a list of visitors, while a dropped badge lies under the desk."),
    ("Mind", "At a {terrain}, sentries sweep the obvious path and a trader waits with supplies. "
     "A rough patrol schedule hangs from a post beside an overgrown side route."),
    ("Mind", "Under the keep, the sealed {barrier} carries unfamiliar marks and one hinge looks new. "
     "A mason holds a diagram, and a maintenance hatch stands ajar."),
    ("Mind", "A trader reports missing cargo, but their ledger is locked and scattered receipts disagree. "
     "A clerk is nearby, and the warehouse seal looks freshly replaced."),
    ("Mind", "Patients grow weaker while a healer's three case notes disagree about the illness. "
     "An unused remedy and a water sample lie on the table."),
    ("Mind", "A damaged navigation console shows conflicting bearings as a scout eyes a growing storm. "
     "A paper chart and an intact auxiliary dial remain within reach."),
    ("Mind", "At a clinic, supplies vanish from a locked cabinet despite a watchful healer. "
     "A delivery record and a scuffed floor tile offer competing clues."),
    ("Mind", "A watchtower's warning lights flash without a visible threat. "
     "A guard has the maintenance log, and a spare circuit waits on the bench."),
    ("Mind", "A guide insists the mapped trail is safe, but travellers keep losing their way. "
     "Fresh footprints cross the path, and an old marker points uphill."),
    ("Mind", "A merchant's sealed parcel reaches the wrong recipient at a depot. "
     "The courier has a receipt, and the shipping board has been changed."),
    ("Face", "At a checkpoint, a suspicious {foe} delays the queue and keeps looking toward an empty guard post. "
     "A merchant with a stamped travel permit waits beside your party."),
    ("Face", "At a public hearing, the {foe} holds the crowd's support while a scribe records testimony. "
     "Several witnesses seem uneasy, and the schedule gives each speaker one turn."),
    ("Face", "In a gatehouse, a {foe} holds a captive as the cook arrives with supper. "
     "The keeper's superior is expected soon, and a side gate stands unlocked."),
    ("Face", "At a depot, a keeper refuses a healer's request for emergency supplies while a "
     "delivery cart waits outside. A signed allocation order is on the counter, unopened."),
    ("Face", "Two armed crews argue over a bridge, trapping a merchant's caravan between them. "
     "Their leaders are within earshot, while an old footpath skirts the dispute."),
    ("Face", "In a crowded shelter, frightened travellers reject a cook's ration plan as food runs low. "
     "A respected porter offers to vouch for someone who earns the room's trust."),
    ("Face", "At a crowded auction, a collector bids on medicine a healer needs urgently. "
     "The auctioneer knows the seller, and an unopened crate sits behind the podium."),
    ("Face", "A watch captain argues with a trader at the city gate while the queue grows restless. "
     "A clerk holds the permit ledger, and a side entrance stands unattended."),
    ("Face", "At a camp council, two scouts disagree about where to shelter from a storm. "
     "A porter has seen both sites, and the cooks have already begun packing."),
    ("Face", "A witness refuses to speak at a hearing after receiving a veiled warning. "
     "The scribe offers a quiet room, and a guard watches the exits."),
    ("Weird", "In a dry camp, a scout reports empty water skins and a week without rain. "
     "A sealed cistern stands nearby, and travellers have gathered around a cracked basin."),
    ("Weird", "At the edge of a {terrain}, an unnatural shimmering curtain separates the party "
     "from a porter across the way. A stone walkway reaches its edge, where runes pulse along the frame."),
    ("Weird", "In a field hospital, a willing ally grows weaker while a healer finds no wound. "
     "An intact medical kit sits nearby, and the patient's shadow flickers strangely."),
    ("Weird", "A beacon fills an outpost with impossible static as a scout watches a storm approach. "
     "Its outer panel is loose and an abandoned shielding coil lies beneath it."),
    ("Weird", "A luminous mist has sealed a storehouse with a trader inside and crates of food beyond the door. "
     "A roof vent is open, and the fog thins whenever the bell sounds."),
    ("Weird", "An energy surge crawls across shelter walls as a healer tends to the people inside. "
     "A grounded conductor and a broken ward marker lie next to the entrance."),
    ("Weird", "At an old shrine, a familiar voice calls from inside a sealed stone. "
     "A scholar has copied its markings, and the floor is warm to the touch."),
    ("Weird", "A patch of sky above a farm turns dark while the fields stay in sunlight. "
     "A farmer holds a weather journal, and birds circle the boundary."),
    ("Weird", "In a workshop, tools float just above their benches as a craftsperson searches for the cause. "
     "An open window and a humming metal box sit at opposite ends of the room."),
    ("Weird", "A traveller's reflection lags behind them in a hall of mirrors. "
     "A caretaker has a cloth cover, and one mirror bears a scratched symbol."),
)
SCENE_CHOICES = {
    "foe": ("mercenary", "ogre", "palace guard", "bandit captain"),
    "barrier": ("stone gate", "iron vault", "watchtower door"),
    "weight": ("pillar", "statue", "roof beam"),
    "terrain": ("ravine", "ruined causeway", "mountain pass", "flooded tunnel"),
    "detail": ("A loose blue thread catches on your sleeve.", "Someone nearby hums a familiar tune.",
               "A small moth circles in the light.", "A feather drifts down nearby.",
               "A faint scent of lavender hangs in the air.", "Dust settles on your shoulder.",
               "A tiny beetle crawls across a nearby surface.", "A speck of yellow paint marks your boot.",
                "A strand of hair brushes your cheek.", "A button on your coat catches the light."),
}
SCENE_DEVELOPMENTS = {
    "Body": (
        ("The footing is slick and uncertain.", "Someone nearby is at risk if the situation worsens.",
         "A heavy load shifts without warning.", "The available space grows tighter.",
         "A sudden gust makes movement harder.", "Another traveller is already struggling.",
         "The route ahead begins to break apart.", "A loud crash threatens to draw attention."),
        ("A sturdy plank lies within reach.", "A bystander offers to help carry something.",
         "A length of rope can be borrowed.", "A handcart stands nearby.",
         "An open side passage offers another way through.", "A fixed railing provides a handhold.",
         "A crate could serve as a step or barrier.", "A nearby worker knows the layout.")),
    "Mind": (
        ("A second account contradicts the first.", "A crucial mark has been rubbed away.",
         "The evidence is being moved out of sight.", "The available light is fading.",
         "A new detail calls the initial explanation into question.", "Someone has altered a recent record.",
         "Two apparent clues point in opposite directions.", "Time is running short before the next shift."),
        ("An observer remembers how things looked earlier.", "A rough sketch of the area is available.",
         "A discarded note names a possible source.", "A spare instrument can be tested.",
         "A second set of records is stored nearby.", "An older witness offers to compare memories.",
         "A damaged component can still be examined.", "A marked map shows an alternate route.")),
    "Face": (
        ("One listener begins to question the story.", "A public argument draws more attention.",
         "Someone threatens to leave the discussion.", "An unexpected rival claims to know the truth.",
         "A rumour about the dispute spreads through the room.", "A decision is due sooner than expected.",
         "The people involved disagree about who has authority.", "A witness grows reluctant to speak."),
        ("A neutral observer offers to hear both sides.", "A written agreement is available for inspection.",
         "Someone nearby knows a person both sides trust.", "A quieter place to talk is open nearby.",
         "A messenger can carry a private reply.", "An old favour can be called in.",
         "A supporter volunteers to speak first.", "A clerk can verify the order of events.")),
    "Weird": (
        ("The strange effect begins to spread.", "Its pulse suddenly grows stronger.",
         "An object nearby behaves impossibly.", "A witness reports seeing the effect elsewhere.",
         "The phenomenon changes with the light.", "Someone close to it becomes disoriented.",
         "Its rhythm becomes irregular.", "The air around it takes on an unfamiliar scent."),
        ("A repeated pattern can be seen in the effect.", "An unaffected object remains nearby.",
         "A careful observer has recorded its timing.", "A boundary stone seems to interrupt it.",
         "A witness remembers when it first appeared.", "A sheltered spot lies just beyond its reach.",
         "A loose fragment reacts when brought closer.", "An old diagram depicts something similar.")),
}


class Character(dict):
    """JSON-compatible character with a human-readable sheet."""

    def __str__(self):
        stats = self["stats"]
        lines = [self["id"].replace("-", " ").title(), "", "PICK ONE BASE STAT OPTION:"]
        lines += [f"  {name}: {stats[name]}" for name in STATS]
        if self["weird"]:
            lines.append(f"  Weird: {self['weird']}")
        for item in self["gear"]:
            effect = f"; {item['effect']}" if "effect" in item else ""
            lines.append(f"  {item['id']} / {item['name']}: {item['tier']} ({item['kind']}{effect})")
        lines += ["", "PICK UP TO FIVE OF THESE TAGS THAT CLEARLY APPLY TO THE SAME ACTION:"]
        for column in COLUMNS:
            lines.append(f"  {column} (Rank {self['ranks'][column]}):")
            tags = [tag for tag in self["tags"] if tag["source"] == column]
            if not tags:
                lines.append("    (none)")
            for tag in tags:
                item = next((gear for gear in self["gear"] if gear["id"] == tag.get("item_id")), None)
                suffix = f" ({item['name']})" if item else ""
                lines.append(f"    {tag['id']}{suffix}")
        return "\n".join(lines)


def character(rng, number, ranks=None):
    if ranks is None:
        ranks = dict(zip(COLUMNS, rng.sample((1, 2, 3, 4), 4)))
    if set(ranks) != set(COLUMNS) or any(rank not in (1, 2, 3, 4) for rank in ranks.values()):
        raise ValueError("each column must have a rank from 1 to 4")
    stat_rng, body_rng, skill_rng, magic_rng, stuff_rng = (
        random.Random(rng.getrandbits(64)) for _ in range(5))
    feat_rngs = {column: random.Random(rng.getrandbits(64)) for column in COLUMNS}
    body, stuff, skills, magic = (ranks[c] for c in COLUMNS)
    points = SKILL_POINTS[skills]
    valid_spreads = [spread for spread in itertools.product(range(1, 6), repeat=2)
                     if sum(value - 1 + (value == 5) for value in spread) == points]
    mind, face = stat_rng.choice(valid_spreads)
    stats = {"Body": BODY_STAT[body], "Mind": mind, "Face": face}

    tags = ([{"id": f"body:{name}", "source": "Body", "name": name}
             for name in body_rng.sample(BODY_TAGS, len(BODY_TAGS))[:BODY_TAG_COUNTS[body]]]
            + [{"id": f"skill:{name}", "source": "Skills", "name": name}
               for name in skill_rng.sample(SKILLS, len(SKILLS))[:SKILL_COUNTS[skills]]])
    if magic > 1:
        picked = magic_rng.sample((*TECHNIQUES, *FORMS, *SPECIFICS), MAGIC_COUNTS[magic])
        tags += [{"id": f"magic:{name}", "source": "Magic", "name": name} for name in picked]

    gear = []
    budget = STUFF_POINTS[stuff]
    # Guarantee an owned Tier-4 item for the free Tier-5 capstone.
    tiers = [4] if stuff == 4 else []
    budget -= sum(tiers)
    while budget >= 2:
        tier = stuff_rng.choice([t for t in (2, 3, 4) if t <= min(budget, stuff)])
        tiers.append(tier)
        budget -= tier
    for index, tier in enumerate(tiers):
        kinds = tuple(kind for kind, names in GEAR_NAMES.items() if tier in names)
        names_by_kind = {kind: [name for name in GEAR_NAMES[kind][tier]
                                if all(name != owned["name"] for owned in gear)]
                         for kind in kinds}
        kind = stuff_rng.choice([kind for kind, names in names_by_kind.items() if names])
        name = stuff_rng.choice(names_by_kind[kind])
        item = {"id": f"gear-{len(gear) + 1}", "kind": kind, "name": name,
                "tier": 5 if stuff == 4 and index == 0 else tier}
        if kind == "Gadget":
            item["effect"] = GADGET_EFFECTS[name]
        gear.append(item)
    for _ in range(STUFF_TAG_COUNTS[stuff]):
        candidates = [(item, name) for item in gear
                      for name in (GADGET_TAGS[item["name"]] if item["kind"] == "Gadget"
                                   else GEAR_TAGS[item["kind"]])
                      if not any(t["item_id"] == item["id"] and t["name"] == name for t in tags
                                 if t["source"] == "Stuff")]
        item, name = stuff_rng.choice(candidates)
        tags.append({"id": f"stuff:{item['id']}:{name}", "source": "Stuff",
                     "item_id": item["id"], "name": name})

    feats = []
    for column in COLUMNS:
        for _ in range(max(0, ranks[column] - 2)):
            choices = [f for f in FEATS if (column != "Skills" or f != "Walk Through Walls")
                       and all(existing["name"] != f for existing in feats)]
            name = feat_rngs[column].choice(choices)
            feats.append({"id": f"{column}:{name}", "source": column, "name": name})
    return Character({"id": f"character-{number}", "ranks": ranks, "stats": stats,
                      "weird": magic - 1, "gear": gear, "tags": tags, "feats": feats,
                      "unspent_stuff_points": budget})


def controlled_characters(rng, families):
    """One shared rank-2 baseline plus ranks 1/3/4 per pillar, per family."""
    actors = []
    for family in range(1, families + 1):
        family_seed = rng.getrandbits(64)
        choices = [(None, 2)] + [(column, rank) for column in COLUMNS for rank in (1, 3, 4)]
        for column, rank in choices:
            ranks = {name: rank if name == column else 2 for name in COLUMNS}
            actor = character(random.Random(family_seed), len(actors) + 1, ranks)
            actor.update(family=family, varied_column=column, varied_rank=rank)
            actors.append(actor)
    return actors


def situation(rng, number, targets, stat=None, excluded=(), seen_premises=()):
    options = [(index, entry) for index, entry in enumerate(SCENES) if stat is None or entry[0] == stat]
    if not options:
        raise ValueError("unknown situation stat")
    available = [option for option in options if option[0] not in excluded]
    for _ in range(10000):
        index, (theme, template) = rng.choice(available or options)
        choices = {key: rng.choice(values) for key, values in SCENE_CHOICES.items()}
        pressure, opening = (rng.choice(options) for options in SCENE_DEVELOPMENTS[theme])
        premise = template.format(**choices) + " " + pressure + " " + opening
        if premise not in seen_premises:
            break
    else:
        raise ValueError("not enough distinct situations for requested sample")
    return {"id": f"scene-{number}", "template_id": index, "theme": theme,
            "target": rng.choice(targets), "premise": premise,
            "text": premise + " " + choices["detail"]}


def probabilities(pool, target):
    """Exact probabilities of each mutually exclusive result (4+ is a hit)."""
    if pool < 0 or target < 1:
        raise ValueError("pool must be nonnegative and target must be positive")
    partial = math.comb(pool, target) / 2**pool if target <= pool else 0.0
    failure = sum(math.comb(pool, i) for i in range(min(pool, target - 1) + 1)) / 2**pool
    critical = sum(math.comb(pool, i) * (1 / 6)**i * (5 / 6)**(pool - i)
                   for i in range(target + 1, pool + 1))
    return {"failure": failure, "partial": partial,
            "full": 1 - failure - partial - critical, "critical": critical}


def roll(rng, pool, target):
    dice = [rng.randint(1, 6) for _ in range(pool)]
    hits = sum(d >= 4 for d in dice)
    sixes = dice.count(6)
    result = ("critical" if sixes > target else "failure" if hits < target
              else "partial" if hits == target else "full")
    return {"dice": dice, "result": result}


def assess(actor, proposal):
    """Validate model-selected evidence; never trust it to calculate dice."""
    if type(proposal) is not dict or set(proposal) != {"action_plan", "base_stat", "tags"}:
        raise ValueError("proposal must contain only action_plan, base_stat, and tags")
    if not isinstance(proposal["action_plan"], str) or not proposal["action_plan"].strip():
        raise ValueError("proposal must contain an action_plan")
    ids = proposal.get("tags")
    if type(ids) is not list or any(type(i) is not str for i in ids):
        raise ValueError("tags must be a list of distinct owned tag IDs")
    raw_option = proposal.get("base_stat")
    if not isinstance(raw_option, str):
        raise ValueError("base_stat must name a stat or owned item")
    name = raw_option.strip().casefold()
    stat = next((stat for stat in actor["stats"] if stat.casefold() == name), None)
    items = [gear for gear in actor["gear"]
             if name in (gear["id"].casefold(), gear["name"].casefold())]
    if len(items) > 1:
        raise ValueError("ambiguous item name; use its gear ID")
    item = items[0] if items else None
    if stat is not None:
        option = stat
        base = actor["stats"][stat]
    elif name == "weird" and actor["weird"] > 0:
        option = "Weird"
        base = actor["weird"]
    elif item is not None:
        option = item["id"]
        base = item["tier"]
    else:
        raise ValueError("base_stat must be a listed character stat or owned item")
    selected = []
    for tag_id in ids:
        name = tag_id.strip().casefold()
        matches = [tag["id"] for tag in actor["tags"]
                   if name in (tag["id"].casefold(), tag["name"].casefold())]
        if len(matches) != 1:
            raise ValueError("tag not owned or ambiguous; use its full ID")
        selected.append(matches[0])
    if len(selected) != len(set(selected)):
        raise ValueError("tags must be a list of distinct owned tag IDs")
    ids = selected
    capped = ids[5:]
    ids = ids[:5]
    return {"pool": base + len(ids), "base": base, "base_stat": option, "tags": ids,
            "item_id": item["id"] if item else None, "capped_tag_ids": capped}
