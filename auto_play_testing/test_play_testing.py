from collections import Counter
import json
import importlib.util
from pathlib import Path
import random
import tempfile
import threading
import unittest
from unittest.mock import patch

from auto_play_testing.__main__ import action_prompt, ask_openrouter, chart, run
from auto_play_testing.controlled_report import (fit_rank_trend, load_controlled, make_controlled_report,
                                                 sheet_profile, usage_counts)
from auto_play_testing.report import character_interval
from auto_play_testing.core import (
    BODY_STAT, BODY_TAG_COUNTS, COLUMNS, FEATS, GADGET_EFFECTS, GADGET_TAGS, GEAR_NAMES, GEAR_TAGS,
    MAGIC_COUNTS, SKILL_COUNTS,
    SKILL_POINTS, STUFF_POINTS, STUFF_TAG_COUNTS, assess, character, controlled_characters, probabilities,
    roll, situation,
)


class CharacterTests(unittest.TestCase):
    def test_character_sheet_is_readable_and_json_compatible(self):
        for seed in range(24):
            actor = character(random.Random(seed), seed + 1)
            sheet = str(actor)
            lines = sheet.splitlines()
            self.assertEqual(lines[0], f"Character {seed + 1}")
            self.assertIn("PICK ONE BASE STAT OPTION:", sheet)
            self.assertIn("PICK UP TO FIVE OF THESE TAGS", sheet)
            for stat in ("Body", "Mind", "Face"):
                self.assertIn(f"  {stat}: {actor['stats'][stat]}", sheet)
            self.assertEqual("  Weird:" in sheet, actor["weird"] > 0)
            for column in COLUMNS:
                self.assertIn(f"{column} (Rank {actor['ranks'][column]})", sheet)
            for item in actor["gear"]:
                effect = f"; {item['effect']}" if "effect" in item else ""
                self.assertIn(f"{item['id']} / {item['name']}: {item['tier']} "
                              f"({item['kind']}{effect})", sheet)
            for tag in actor["tags"]:
                self.assertIn(tag["id"], sheet)
            self.assertNotIn("FEATS", sheet)
            for feat in actor["feats"]:
                self.assertNotIn(feat["id"], sheet)
            self.assertEqual(json.loads(json.dumps(actor)), dict(actor))

    def test_random_builds_respect_budgets_and_menus(self):
        rng = random.Random(77)
        kinds = set()
        for i in range(500):
            actor = character(rng, i)
            ranks, stats = actor["ranks"], actor["stats"]
            self.assertEqual(sorted(ranks.values()), [1, 2, 3, 4])
            self.assertEqual(set(stats), {"Body", "Mind", "Face"})
            self.assertTrue(all(1 <= v <= 5 for v in stats.values()))
            self.assertEqual(stats["Body"], BODY_STAT[ranks["Body"]])
            self.assertEqual(sum(stats[s] - 1 + (stats[s] == 5) for s in ("Mind", "Face")),
                             SKILL_POINTS[ranks["Skills"]])
            self.assertLessEqual(sum(v == 5 for v in stats.values()), 1)
            for source, expected in (("Body", BODY_TAG_COUNTS[ranks["Body"]]),
                                     ("Skills", SKILL_COUNTS[ranks["Skills"]]),
                                     ("Magic", MAGIC_COUNTS[ranks["Magic"]]),
                                     ("Stuff", STUFF_TAG_COUNTS[ranks["Stuff"]])):
                self.assertEqual(sum(t["source"] == source for t in actor["tags"]), expected)
            self.assertEqual(len({t["id"] for t in actor["tags"]}), len(actor["tags"]))
            self.assertEqual(actor["weird"], ranks["Magic"] - 1)
            self.assertEqual(sum(min(g["tier"], 4) for g in actor["gear"])
                             + actor["unspent_stuff_points"], STUFF_POINTS[ranks["Stuff"]])
            self.assertTrue(all(2 <= g["tier"] <= ranks["Stuff"] or
                                ranks["Stuff"] == 4 and g["tier"] == 5 for g in actor["gear"]))
            self.assertEqual(sum(g["tier"] == 5 for g in actor["gear"]), int(ranks["Stuff"] == 4))
            kinds.update(g["kind"] for g in actor["gear"])
            self.assertEqual(len({g["name"] for g in actor["gear"]}), len(actor["gear"]))
            self.assertEqual(bool(actor["gear"]), ranks["Stuff"] > 1)
            for item in actor["gear"]:
                self.assertIn(item["name"], GEAR_NAMES[item["kind"]][min(item["tier"], 4)])
                self.assertEqual(item.get("effect"), GADGET_EFFECTS.get(item["name"]))
            for tag in actor["tags"]:
                if tag["source"] == "Stuff":
                    item = next(g for g in actor["gear"] if g["id"] == tag["item_id"])
                    self.assertIn(tag["name"], GADGET_TAGS[item["name"]] if item["kind"] == "Gadget"
                                  else GEAR_TAGS[item["kind"]])
            self.assertEqual(len(actor["feats"]), 3)  # one rank 3 and two rank 4
            self.assertTrue(all(f["name"] in FEATS for f in actor["feats"]))
        self.assertEqual(kinds, set(GEAR_NAMES))

    def test_every_stuff_category_can_receive_its_published_tags(self):
        tagged_kinds = set()
        for seed in range(500):
            actor = character(random.Random(seed), seed, dict.fromkeys(COLUMNS, 4))
            tagged_kinds.update(next(item["kind"] for item in actor["gear"] if item["id"] == tag["item_id"])
                                for tag in actor["tags"] if tag["source"] == "Stuff")
        self.assertEqual(tagged_kinds, set(GEAR_NAMES))

    def test_scenes_are_reproducible_and_use_configured_targets(self):
        one = [situation(random.Random(123 + i), i, [2, 4]) for i in range(100)]
        two = [situation(random.Random(123 + i), i, [2, 4]) for i in range(100)]
        self.assertEqual(one, two)
        self.assertEqual({s["theme"] for s in one}, {"Body", "Mind", "Face", "Weird"})
        self.assertEqual({s["target"] for s in one}, {2, 4})
        for scene in one:
            self.assertGreaterEqual(scene["text"].count("."), 3)
            self.assertNotRegex(scene["text"], r"\b(?:Convince|Free|Identify|Teleport|Protect|Secure|Contain)\b")
            self.assertNotIn("Your objective is", scene["text"])
            self.assertNotIn("fallen pillar was sabotaged", scene["text"])
            self.assertNotIn("heavy watchtower", scene["text"])

    def test_controlled_families_change_only_one_pillar(self):
        actors = controlled_characters(random.Random(93), 5)
        self.assertEqual(len(actors), 65)  # One shared baseline + 3 variants per pillar.
        for family in range(1, 6):
            group = [a for a in actors if a["family"] == family]
            baseline = next(a for a in group if a["varied_column"] is None)
            self.assertEqual(baseline["ranks"], dict.fromkeys(COLUMNS, 2))
            for actor in group:
                column = actor["varied_column"]
                self.assertEqual(actor["ranks"], {c: actor["varied_rank"] if c == column else 2
                                                  for c in COLUMNS})
                if column not in ("Body", "Skills"):
                    self.assertEqual(actor["stats"], baseline["stats"])
                if column != "Stuff":
                    self.assertEqual(actor["gear"], baseline["gear"])
                for source in COLUMNS:
                    if source != column:
                        self.assertEqual([t for t in actor["tags"] if t["source"] == source],
                                         [t for t in baseline["tags"] if t["source"] == source])
                if column != "Magic":
                    self.assertEqual(actor["weird"], baseline["weird"])
        self.assertEqual(actors, controlled_characters(random.Random(93), 5))

    def test_controlled_scene_theme_cycle_can_be_balanced(self):
        rng = random.Random(9)
        themes = ("Body", "Mind", "Face", "Weird")
        used = {theme: set() for theme in themes}
        scenes = []
        for i, theme in enumerate(themes * 4):
            scene = situation(rng, i + 1, [2], theme, used[theme])
            self.assertNotIn(scene["template_id"], used[theme])
            used[theme].add(scene["template_id"])
            scenes.append(scene)
        self.assertEqual([s["theme"] for s in scenes], list(themes * 4))
        self.assertTrue(all(len(used[theme]) == 4 for theme in themes))


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.actor = {"stats": {"Body": 2, "Mind": 3, "Face": 1}, "weird": 2,
                       "gear": [{"id": "gear-1", "name": "War-Chariot", "tier": 5}],
                      "feats": [{"id": "Stuff:Blink"}],
                      "tags": [{"id": "body:Strong", "source": "Body", "name": "Strong"},
                               {"id": "skill:Athletics", "source": "Skills", "name": "Athletics"},
                               {"id": "stuff:gear-1:Fast", "source": "Stuff", "name": "Fast", "item_id": "gear-1"},
                               {"id": "magic:Control", "source": "Magic", "name": "Control"},
                               {"id": "magic:Water", "source": "Magic", "name": "Water"}]}
        self.proposal = {"action_plan": "Push using the vehicle", "base_stat": "gear-1",
                          "tags": ["body:Strong", "skill:Athletics"]}

    def test_mixed_tags_and_item_base(self):
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 7)
        self.assertEqual(self.proposal["tags"], ["body:Strong", "skill:Athletics"])
        self.proposal["tags"] = ["body:Strong", "skill:Athletics", "stuff:gear-1:Fast",
                                 "magic:Control", "magic:Water"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 10)
        self.proposal["base_stat"] = "Body"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 7)
        self.proposal["tags"] = []
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 2)
        self.proposal["base_stat"] = "Mind"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 3)

    def test_reject_unlisted_options_but_accept_single_magic_tag(self):
        self.proposal["tags"] = ["body:Made up"]
        with self.assertRaisesRegex(ValueError, "not owned"):
            assess(self.actor, self.proposal)
        self.proposal["tags"] = []
        self.proposal["base_stat"] = "Magic"
        with self.assertRaisesRegex(ValueError, "listed"):
            assess(self.actor, self.proposal)
        self.proposal["base_stat"] = "Body"
        self.proposal["tags"] = ["magic:Control"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 3)
        self.proposal["tags"] = ["magic:Water"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 3)
        self.proposal["base_stat"] = "Weird"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 3)
        self.proposal["tags"] = []
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 2)

    def test_weird_and_item_bases_are_independent_listed_options(self):
        self.proposal["tags"] = ["magic:Control", "magic:Water"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 7)
        self.proposal["base_stat"] = "Weird"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 4)
        self.actor["weird"] = 0
        with self.assertRaisesRegex(ValueError, "listed"):
            assess(self.actor, self.proposal)

    def test_item_id_and_name_select_same_canonical_base(self):
        by_id = assess(self.actor, self.proposal)
        self.proposal["base_stat"] = "  war-chariot  "
        by_name = assess(self.actor, self.proposal)
        self.assertEqual(by_id, by_name)
        self.assertEqual(by_name["base_stat"], "gear-1")
        self.assertEqual(self.proposal["base_stat"], "  war-chariot  ")
        self.proposal["base_stat"] = "BODY"
        self.assertEqual(assess(self.actor, self.proposal)["base_stat"], "Body")

    def test_unambiguous_owned_tag_names_are_accepted_but_duplicate_names_are_not(self):
        self.proposal["tags"] = [" Strong ", "athletics", "MAGIC:WATER"]
        self.assertEqual(assess(self.actor, self.proposal)["tags"],
                         ["body:Strong", "skill:Athletics", "magic:Water"])
        self.proposal["tags"] = ["Strong", "body:Strong"]
        with self.assertRaisesRegex(ValueError, "distinct"):
            assess(self.actor, self.proposal)
        self.actor["tags"].append({"id": "stuff:gear-1:Strong", "source": "Stuff",
                                   "name": "Strong", "item_id": "gear-1"})
        self.proposal["tags"] = ["Strong"]
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            assess(self.actor, self.proposal)
        self.proposal["tags"] = ["stuff:gear-1:Strong"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 6)

    def test_duplicate_item_names_need_id_to_disambiguate(self):
        self.actor["gear"].append({"id": "gear-2", "name": "War-Chariot", "tier": 3})
        self.proposal["base_stat"] = "War-Chariot"
        with self.assertRaisesRegex(ValueError, "ambiguous item name"):
            assess(self.actor, self.proposal)
        self.proposal["base_stat"] = "gear-2"
        self.assertEqual(assess(self.actor, self.proposal)["base"], 3)

    def test_exact_outcomes(self):
        odds = probabilities(3, 2)
        self.assertAlmostEqual(odds["failure"], .5)
        self.assertAlmostEqual(odds["partial"], .375)
        self.assertAlmostEqual(odds["critical"], 1 / 216)
        self.assertAlmostEqual(sum(odds.values()), 1)
        self.assertEqual(probabilities(0, 2)["failure"], 1)
        self.assertEqual(roll(random.Random(1), 0, 2)["result"], "failure")

    def test_base_stat_must_be_a_listed_option(self):
        self.proposal.update(action_plan="No plausible approach", base_stat=None, tags=[])
        with self.assertRaisesRegex(ValueError, "base_stat"):
            assess(self.actor, self.proposal)
        self.proposal["tags"] = ["skill:Athletics"]
        with self.assertRaisesRegex(ValueError, "base_stat"):
            assess(self.actor, self.proposal)

    def test_cap_applied_in_selection_order_without_pair_preference(self):
        self.actor["tags"].extend({"id": f"skill:Extra{i}", "name": f"Extra{i}", "source": "Skills"}
                                  for i in range(5))
        self.proposal["tags"] = [f"skill:Extra{i}" for i in range(5)] + ["magic:Control", "magic:Water"]
        scored = assess(self.actor, self.proposal)
        self.assertEqual(scored["pool"], 10)
        self.assertEqual(scored["tags"], [f"skill:Extra{i}" for i in range(5)])
        self.assertEqual(scored["capped_tag_ids"], ["magic:Control", "magic:Water"])
        self.proposal["base_stat"] = "Weird"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 7)

    def test_owned_item_tags_can_mix_without_matching_item_base(self):
        self.actor["gear"].append({"id": "gear-2", "name": "Gunship", "tier": 3})
        self.actor["tags"].append({"id": "stuff:gear-2:Armed", "source": "Stuff",
                                   "name": "Armed", "item_id": "gear-2"})
        self.proposal["tags"] = ["stuff:gear-2:Armed"]
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 6)
        self.proposal["base_stat"] = "Body"
        self.assertEqual(assess(self.actor, self.proposal)["pool"], 3)

    def test_item_tier_is_a_base_and_feat_is_not_a_tag(self):
        self.actor["stats"]["Body"] = 4
        self.actor["gear"][0]["tier"] = 2
        self.assertEqual(assess(self.actor, self.proposal)["base"], 2)
        self.proposal["base_stat"] = "Body"
        self.assertEqual(assess(self.actor, self.proposal)["base"], 4)
        self.proposal["tags"] = ["Stuff:Blink"]
        with self.assertRaisesRegex(ValueError, "tag not owned"):
            assess(self.actor, self.proposal)


class OutputTests(unittest.TestCase):
    def test_prompt_shows_options_and_leaves_base_and_tag_choice_to_model(self):
        actor = character(random.Random(7), 1)
        scene = situation(random.Random(9), 1, [2])
        prompt = action_prompt(actor, scene)
        for phrase in ("PICK ONE BASE STAT OPTION", "PICK UP TO FIVE", "You decide which base and tags fit",
                       "combination of Body, Stuff, Skills, and Magic", "either its gear ID",
                       "Choose what you want to do in this situation",
                       "action_plan", "base_stat", "tags"):
            self.assertIn(phrase, prompt)
        self.assertNotIn("GM has fixed", prompt)
        self.assertNotIn("tag_meanings", prompt)
        self.assertNotIn("FEATS", prompt)
        self.assertEqual(set(json.loads(prompt.split("\n\n")[-1])["scene"]), {"id", "text", "target"})
        for feat in actor["feats"]:
            self.assertNotIn(feat["id"], prompt)
        for item in actor["gear"]:
            self.assertIn(f"{item['id']} / {item['name']}: {item['tier']}", prompt)

    def test_openrouter_json_and_usage_are_parsed(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return json.dumps({"choices": [{"message": {"content":
                    '{"action_plan":"Try","base_stat":"Body","tags":[]}'}}],
                                   "usage": {"cost": 0.0001}}).encode()

        with patch("auto_play_testing.__main__.urllib.request.urlopen", return_value=Response()) as client:
            proposal, usage = ask_openrouter("test-key", "test-model", "test prompt")
        self.assertEqual(json.loads(proposal)["base_stat"], "Body")
        self.assertEqual(usage["cost"], 0.0001)
        request = client.call_args.args[0]
        self.assertEqual(json.loads(request.data)["max_tokens"], 700)

    def test_chart_and_offline_end_to_end_run(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            chart(output, 5, 3)
            self.assertIn("Partial or better", (output / "dice_odds.svg").read_text())
            self.assertEqual(len((output / "dice_odds.csv").read_text().splitlines()), 19)

            def fake_ai(key, model, prompt):
                return json.dumps({"action_plan": "Try directly", "base_stat": "Body", "tags": []}), {"cost": 0.0001}

            args = type("Args", (), {"seed": 7, "characters": 3, "situations": 4,
                                     "targets": [2], "output": output, "model": "fake", "max_cost": 5.0,
                                     "workers": 4})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", side_effect=fake_ai
            ) as client, patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            self.assertEqual(client.call_count, 12)
            records = [json.loads(line) for line in (output / "trials.jsonl").read_text().splitlines()]
            self.assertEqual(len(records), 12)
            self.assertEqual({r["mode"] for r in records}, {"current"})
            self.assertTrue((output / "body_rank_outcomes.svg").exists())
            self.assertIn("body_rank", (output / "summary.csv").read_text())

    def test_two_builds_get_full_width_uncertainty(self):
        rows = [{"character_id": "a", "odds": {"failure": .2}},
                {"character_id": "b", "odds": {"failure": .3}}]
        if importlib.util.find_spec("scipy"):
            point, low, high, n = character_interval(rows, lambda r: 1 - r["odds"]["failure"])
            self.assertEqual((low, high, n), (0, 1, 2))
            self.assertAlmostEqual(point, .75)

    def test_cost_cap_stops_before_any_paid_call(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"seed": 7, "characters": 1, "situations": 1,
                                     "targets": [2], "output": Path(directory), "model": "fake",
                                     "max_cost": 0.000001, "workers": 4})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter"
            ) as client, patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            client.assert_not_called()
            self.assertEqual(json.loads((Path(directory) / "report.json").read_text())["calls"], 0)

    def test_invalid_response_is_recorded_not_counted_as_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"seed": 7, "characters": 1, "situations": 1,
                                     "targets": [2], "output": Path(directory), "model": "fake",
                                     "max_cost": 5, "workers": 2})()
            def fake_ai(key, model, prompt):
                return json.dumps({"action_plan": "Invent magic", "base_stat": "Magic",
                                   "tags": []}), {"cost": 0.001}
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", side_effect=fake_ai
            ), patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            report = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual((report["calls"], report["valid"], report["rejected"]), (1, 0, 1))
            self.assertEqual(len((Path(directory) / "rejected.jsonl").read_text().splitlines()), 1)

    def test_truncated_json_is_recorded_as_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"seed": 7, "characters": 1, "situations": 1,
                                     "targets": [2], "output": Path(directory), "model": "fake",
                                     "max_cost": 5, "workers": 2})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", return_value=('''{"possible": true, ''', {"cost": 0.001})
            ), patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            report = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual((report["calls"], report["valid"], report["rejected"]), (1, 0, 1))
            self.assertIn("invalid JSON", (Path(directory) / "rejected.jsonl").read_text())

    def test_workers_make_simultaneous_requests_and_rolls_are_repeatable(self):
        def perform(output):
            barrier = threading.Barrier(2, timeout=5)
            def fake_ai(key, model, prompt):
                barrier.wait()
                proposal = {"action_plan": "Attempt", "base_stat": "Body", "tags": []}
                return json.dumps(proposal), {"cost": 0.001}
            args = type("Args", (), {"seed": 7, "characters": 2, "situations": 1,
                                     "targets": [2], "output": output, "model": "fake",
                                     "max_cost": 5, "workers": 2})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", side_effect=fake_ai
            ), patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            return {r["character_id"]: r["dice"] for r in (
                json.loads(line) for line in (output / "trials.jsonl").read_text().splitlines())}

        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            self.assertEqual(perform(Path(first)), perform(Path(second)))

    def test_budget_reserves_every_in_flight_call(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"seed": 7, "characters": 2, "situations": 2,
                                     "targets": [2], "output": Path(directory), "model": "fake",
                                     "max_cost": 1, "workers": 8})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter",
                 return_value=(json.dumps({"action_plan": "Try", "base_stat": "Body", "tags": []}), {"cost": 0.8})
            ) as client, patch("auto_play_testing.__main__.model_pricing", return_value=(0, 0.001)):
                run(args)
            client.assert_called_once()
            report = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual(report["calls"], 1)
            self.assertLessEqual(report["cost"], args.max_cost)

    def test_controlled_run_scores_one_current_rule_pool_per_call(self):
        with tempfile.TemporaryDirectory() as directory:
            def fake_ai(key, model, prompt):
                payload = json.loads(prompt.split("\n\n")[-1])
                scene = payload["scene"]
                if scene["id"] == "scene-4" and "  Weird:" in prompt:
                    magic_tag = next((line.strip() for line in prompt.splitlines()
                                      if line.startswith("    magic:")), None)
                    proposal = {"action_plan": "Bend reality", "base_stat": "Weird", "tags": [magic_tag]}
                else:
                    tags = [next((line.strip() for line in prompt.splitlines()
                                  if line.startswith(f"    {source}:")), None)
                            for source in ("body", "skill")]
                    item_line = next((line for line in prompt.splitlines()
                                      if line.startswith("  gear-1 / ")), None)
                    base = (item_line.split(" / ", 1)[1].split(": ", 1)[0]
                            if scene["id"] == "scene-1" and item_line else "Body")
                    proposal = {"action_plan": "Attempt directly", "base_stat": base,
                                 "tags": [t for t in tags if t is not None]}
                return json.dumps(proposal), {"cost": 0.0001}

            args = type("Args", (), {"command": "run-controlled", "seed": 7, "families": 1,
                                     "situations": 12, "targets": [2], "output": Path(directory),
                                     "model": "fake", "max_cost": 5, "workers": 4})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", side_effect=fake_ai
            ) as client, patch("auto_play_testing.__main__.model_pricing", return_value=(0.0000001, 0.0000004)):
                run(args)
            records = [json.loads(line) for line in (Path(directory) / "trials.jsonl").read_text().splitlines()]
            self.assertEqual(client.call_count, 24)
            self.assertEqual(len(records), 24)
            self.assertTrue(any(row["scene_theme"] == "Weird" and row["tag_count"] == 1
                                and row["possible"] for row in records))
            self.assertTrue(any(row["proposal"]["base_stat"] != row["base_stat"]
                                and row["base_stat"] == "gear-1" for row in records))
            self.assertEqual(json.loads((Path(directory) / "setup.json").read_text())["design"], "three-at-two")
            for row in records:
                self.assertEqual(row["pool"], row["base"] + row["tag_count"])
                self.assertEqual(row["tag_count"], len(row["tags"]))
                self.assertNotIn("one_source", row)
                self.assertNotIn("mixed", row)
            self.assertAlmostEqual(sum(r["usage"]["cost"] for r in records),
                                   json.loads((Path(directory) / "report.json").read_text())["cost"])
            self.assertEqual(len(load_controlled(Path(directory))[1]), 24)
            if importlib.util.find_spec("matplotlib") and importlib.util.find_spec("scipy"):
                pdf = make_controlled_report(Path(directory), Path(directory) / "controlled.pdf", sheet_families=4)
                self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))

    def test_controlled_runner_uses_distinct_templates_within_each_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"command": "run-controlled", "seed": 2042, "families": 1,
                                     "situations": 16, "targets": [2], "output": Path(directory),
                                     "model": "fake", "max_cost": 5, "workers": 4})()
            proposal = json.dumps({"action_plan": "Try", "base_stat": "Body", "tags": []})
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", return_value=(proposal, {"cost": .0001})
            ), patch("auto_play_testing.__main__.model_pricing", return_value=(.0000001, .0000004)):
                run(args)
            setup = json.loads((Path(directory) / "setup.json").read_text())
            for theme in ("Body", "Mind", "Face", "Weird"):
                scenes = [scene for scene in setup["situations"] if scene["theme"] == theme]
                self.assertEqual(len(scenes), 4)
                self.assertEqual(len({scene["template_id"] for scene in scenes}), 4)
            self.assertEqual(json.loads((Path(directory) / "report.json").read_text())["valid"], 32)

    def test_thousand_controlled_scenarios_are_unique_and_balanced_without_paid_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"command": "run-controlled", "seed": 2042, "families": 1,
                                     "situations": 1000, "targets": [1, 2, 3, 4], "output": Path(directory),
                                     "model": "fake", "max_cost": .000001, "workers": 4})()
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter"
            ) as client, patch("auto_play_testing.__main__.model_pricing", return_value=(.0000001, .0000004)):
                run(args)
            client.assert_not_called()
            scenes = json.loads((Path(directory) / "setup.json").read_text())["situations"]
            self.assertEqual(len(scenes), 1000)
            self.assertEqual(len({scene["text"] for scene in scenes}), 1000)
            self.assertEqual(len({scene["premise"] for scene in scenes}), 1000)
            self.assertEqual(json.loads((Path(directory) / "report.json").read_text())["requested_calls"], 2000)
            self.assertEqual(set(Counter((s["family"], s["varied_column"], s["varied_rank"])
                                         for s in scenes).values()), {83, 84})
            for theme in ("Body", "Mind", "Face", "Weird"):
                themed = [scene for scene in scenes if scene["theme"] == theme]
                self.assertEqual(len(themed), 250)
                self.assertEqual(set(Counter(scene["template_id"] for scene in themed).values()), {25})

    def test_usage_counts_distinguish_tag_dice_from_actions_and_item_bases(self):
        setup = {"characters": [{"id": "a", "tags": [
            {"id": "b", "source": "Body"}, {"id": "s", "source": "Skills"},
            {"id": "i", "source": "Stuff"}, {"id": "m1", "source": "Magic"},
            {"id": "m2", "source": "Magic"}]}]}
        rows = [{"character_id": "a", "scene_theme": "Body", "possible": True,
                 "base_stat": "gear-1", "item_id": "gear-1", "tags": ["b", "s", "i", "m1", "m2"]},
                {"character_id": "a", "scene_theme": "Face", "possible": True,
                 "base_stat": "Face", "item_id": None, "tags": ["s"]}]
        counts = usage_counts(setup, rows)
        self.assertEqual(counts["feasible"], 2)
        self.assertEqual(counts["bases"], {"Item": 1, "Face": 1})
        self.assertEqual(counts["tag_dice"], {"Body": 1, "Stuff": 1, "Skills": 2, "Magic": 2})
        self.assertEqual(counts["tag_actions"], {"Body": 1, "Stuff": 1, "Skills": 2, "Magic": 1})
        self.assertEqual(counts["by_stat"]["Body"], {"feasible": 1, "item": 1})

    def test_sheet_profile_counts_all_owned_tags_and_available_base_ratings(self):
        actor = {"stats": {"Body": 2, "Mind": 3, "Face": 4}, "weird": 0,
                 "gear": [{"tier": 2}, {"tier": 5}],
                 "tags": [{"source": "Magic"}, {"source": "Magic"}, {"source": "Stuff"}]}
        profile = sheet_profile(actor)
        self.assertEqual(profile["tags"], {"Magic": 2, "Stuff": 1})
        self.assertEqual((profile["rating_sum"], profile["option_count"]), (16, 5))
        actor["weird"] = 2
        self.assertEqual((sheet_profile(actor)["rating_sum"], sheet_profile(actor)["option_count"]), (18, 6))

    def test_rank_trend_uses_one_mean_per_rank_not_number_of_responses(self):
        slope, intercept = fit_rank_trend({1: 2, 2: 3, 3: 4, 4: 5})
        self.assertAlmostEqual(slope, 1)
        self.assertAlmostEqual(intercept, 1)
        slope, intercept = fit_rank_trend({1: 5, 2: 4, 3: 4, 4: 2})
        self.assertAlmostEqual(slope, -.9)
        self.assertAlmostEqual(intercept, 6)

    def test_timeout_is_recorded_without_losing_other_responses(self):
        with tempfile.TemporaryDirectory() as directory:
            args = type("Args", (), {"seed": 7, "characters": 1, "situations": 1,
                                     "targets": [2], "output": Path(directory), "model": "fake",
                                     "max_cost": 5, "workers": 2})()
            def fake_ai(key, model, prompt):
                if "Character 1\n" in prompt:
                    raise TimeoutError("provider stalled")
                return json.dumps({"action_plan": "Try", "base_stat": "Body", "tags": []}), {"cost": .001}
            args.characters = 2
            with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test"}), patch(
                "auto_play_testing.__main__.ask_openrouter", side_effect=fake_ai
            ), patch("auto_play_testing.__main__.model_pricing", return_value=(.0000001, .0000004)):
                run(args)
            report = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual((report["calls"], report["valid"], report["request_errors"]), (2, 1, 1))
            self.assertGreater(report["cost_upper_bound"], report["cost"])
            self.assertIn("provider stalled", (Path(directory) / "request_errors.jsonl").read_text())


if __name__ == "__main__":
    unittest.main()
