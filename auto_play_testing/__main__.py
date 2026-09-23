"""Run from the repo root: python -m auto_play_testing chart|run."""

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import csv
import itertools
import json
import os
from pathlib import Path
import random
import urllib.error
import urllib.request

from .core import SCENES, assess, character, controlled_characters, probabilities, roll, situation


MAX_OUTPUT_TOKENS = 700


def chart(output, max_pool, max_target):
    """Produce dependency-free SVG heatmaps and an exact probability CSV."""
    output.mkdir(parents=True, exist_ok=True)
    cells = []
    for target in range(1, max_target + 1):
        for pool in range(max_pool + 1):
            odds = probabilities(pool, target)
            cells.append({"pool": pool, "target": target, **odds,
                          "partial_or_better": 1 - odds["failure"],
                          "full_or_better": odds["full"] + odds["critical"]})
    with (output / "dice_odds.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cells[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(cells)

    width = 120 + 2 * (max_pool + 1) * 55 + 75
    height = 145 + max_target * 46
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#101c28"/>',
             '<style>text{font: 13px sans-serif;fill:#e6f2f3} .title{font-size:20px;font-weight:bold} '
             '.cell{font-size:11px;font-weight:bold}</style>',
             '<text class="title" x="30" y="35">Dice pool vs target: exact chance</text>',
             '<text x="30" y="57">Each d6 hits on 4+. Tie = partial; beat = full.</text>']
    for side, (key, title) in enumerate((("partial_or_better", "Partial or better"),
                                          ("full_or_better", "Full or critical"))):
        left = 65 + side * ((max_pool + 1) * 55 + 55)
        parts.append(f'<text x="{left}" y="84">{title}</text>')
        for pool in range(max_pool + 1):
            parts.append(f'<text x="{left + pool * 55 + 25}" y="104" text-anchor="middle">{pool}</text>')
        for target in range(1, max_target + 1):
            y = 115 + (target - 1) * 46
            parts.append(f'<text x="{left - 20}" y="{y + 25}" text-anchor="middle">{target}</text>')
            for pool in range(max_pool + 1):
                p = cells[(target - 1) * (max_pool + 1) + pool][key]
                # Dark slate (0%) through saturated turquoise (100%).
                colour = f'rgb({int(29 + 33*p)},{int(49 + 133*p)},{int(66 + 125*p)})'
                x = left + pool * 55
                parts += [f'<rect x="{x}" y="{y}" width="52" height="42" rx="4" fill="{colour}"/>',
                          f'<text class="cell" x="{x + 26}" y="{y + 26}" text-anchor="middle">{p:.0%}</text>']
    parts += [f'<text x="30" y="{height - 13}">Rows: GM target  |  Columns: dice in pool  |  Criticals are included in full.</text>',
              '</svg>']
    (output / "dice_odds.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def action_prompt(actor, scene):
    return (
        "You are this Traveller. Choose what you want to do in this situation; "
        "describe one meaningful action you initiate and build a dice roll for it. "
        "Pick exactly one listed base option (a Body, Mind, Face, Weird stat "
        "or an item); use the number printed beside it. For an item, either its gear ID "
        "or its name is accepted. Pick up to five listed tag IDs that you think "
        "help your action, from any "
        "combination of Body, Stuff, Skills, and Magic. Each selected tag adds one die. "
        "You decide which base and tags fit; no particular tag is required. "
        "Return JSON with exactly action_plan (a short string), base_stat (one listed "
        "stat name, gear ID, or item name), and tags (a list of listed tag IDs).\n\n"
        + str(actor) + "\n\n"
        + json.dumps({"scene": {"id": scene["id"], "text": scene["text"],
                                 "target": scene["target"]}}, ensure_ascii=True)
    )


def model_pricing(model):
    with urllib.request.urlopen(f"https://openrouter.ai/api/v1/models/{model}/endpoints", timeout=30) as response:
        endpoints = json.load(response)["data"]["endpoints"]
    if not endpoints:
        raise ValueError(f"no pricing endpoints for {model}")
    return (max(float(e["pricing"]["prompt"]) for e in endpoints),
            max(float(e["pricing"]["completion"]) for e in endpoints))


def ask_openrouter(api_key, model, prompt):
    data = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"}, "temperature": 0,
                       "max_tokens": MAX_OUTPUT_TOKENS}).encode()
    request = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=data,
                                     headers={"Authorization": f"Bearer {api_key}",
                                              "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    usage = result["usage"]
    if not isinstance(usage.get("cost"), (int, float)):
        raise ValueError("OpenRouter did not report cost; cannot enforce budget")
    return result["choices"][0]["message"]["content"], usage


def summary(rows, output):
    """Aggregate both observed rolls and exact expected rates per condition."""
    groups = {}
    for row in rows:
        for dimension, value in (("all", "all"), ("body_rank", row["ranks"]["Body"]),
                                 ("body_stat", row["stats"]["Body"]),
                                 ("skills_rank", row["ranks"]["Skills"]),
                                 ("magic_rank", row["ranks"]["Magic"]),
                                 ("stuff_rank", row["ranks"]["Stuff"]),
                                 ("scene_theme", row["scene_theme"]), ("target", row["target"])):
            key = (row["mode"], dimension, value)
            group = groups.setdefault(key, {"trials": 0, "feasible": 0, "pool_sum": 0,
                                            **{f"observed_{k}": 0 for k in ("failure", "partial", "full", "critical")},
                                            **{f"expected_{k}": 0.0 for k in ("failure", "partial", "full", "critical")}})
            group["trials"] += 1
            group["feasible"] += int(row["possible"])
            group["pool_sum"] += row["pool"]
            group[f'observed_{row["result"]}'] += 1
            for result, chance in row["odds"].items():
                group[f"expected_{result}"] += chance
    fields = ("mode", "dimension", "value", "trials", "feasible_rate", "mean_pool",
              "observed_failure", "observed_partial", "observed_full", "observed_critical",
              "expected_failure", "expected_partial", "expected_full", "expected_critical")
    with (output / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for (mode, dimension, value), group in sorted(groups.items(), key=lambda x: str(x[0])):
            n = group["trials"]
            writer.writerow({"mode": mode, "dimension": dimension, "value": value, "trials": n,
                             "feasible_rate": group["feasible"] / n, "mean_pool": group["pool_sum"] / n,
                             **{k: v / n for k, v in group.items() if k.startswith(("observed_", "expected_"))}})


def outcomes_chart(rows, output):
    """Body-rank plot; stacked heights are exact expected outcome rates."""
    groups = {}
    for row in rows:
        group = groups.setdefault(row["ranks"]["Body"], [])
        group.append(row["odds"])
    colours = {"failure": "#e27b73", "partial": "#eec681", "full": "#5dc3bc", "critical": "#749cea"}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 420">',
             '<rect width="100%" height="100%" fill="#101c28"/>',
             '<style>text{font:14px sans-serif;fill:#e6f2f3}.title{font-size:21px;font-weight:bold}</style>',
             '<text class="title" x="35" y="38">Expected outcomes by Body rank</text>',
              '<text x="35" y="62">Same scenes for every character; current rules.</text>']
    for index, rank in enumerate(range(1, 5)):
        samples = groups.get(rank, [])
        if not samples:
            continue
        x = 112 + index * 180
        y = 320.0
        for result, colour in colours.items():
            fraction = sum(sample[result] for sample in samples) / len(samples)
            size = 220 * fraction
            y -= size
            parts.append(f'<rect x="{x}" y="{y:.2f}" width="50" height="{size:.2f}" fill="{colour}"/>')
        parts.append(f'<text x="{137 + index * 180}" y="365" text-anchor="middle">Body rank {rank}</text>')
    for index, (name, colour) in enumerate(colours.items()):
        x = 80 + index * 180
        parts += [f'<rect x="{x}" y="388" width="14" height="14" fill="{colour}"/>',
                  f'<text x="{x + 20}" y="401">{name.title()}</text>']
    parts.append('</svg>')
    (output / "body_rank_outcomes.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def run(args):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("export OPENROUTER_API_KEY before running paid AI trials")
    input_price, output_price = model_pricing(args.model)
    rng = random.Random(args.seed)
    controlled = getattr(args, "command", "run") == "run-controlled"
    if controlled:
        actors = controlled_characters(rng, args.families)
        by_variant = {(actor["family"], actor["varied_column"], actor["varied_rank"]): actor
                      for actor in actors}
        scene_themes = ("Body", "Mind", "Face", "Weird")
        used = {theme: set() for theme in scene_themes}
        seen_premises = set()
        templates_per_theme = {theme: sum(entry[0] == theme for entry in SCENES)
                               for theme in scene_themes}
        assignments = [(family, column, rank) for family in range(1, args.families + 1)
                       for column in ("Body", "Stuff", "Skills", "Magic") for rank in (1, 3, 4)]
        scenes = []
        for i in range(args.situations):
            theme = scene_themes[i % 4]
            if len(used[theme]) == templates_per_theme[theme]:
                used[theme].clear()
            scene = situation(rng, i + 1, args.targets, theme, used[theme], seen_premises)
            used[theme].add(scene["template_id"])
            seen_premises.add(scene["premise"])
            if i % len(assignments) == 0:
                rng.shuffle(assignments)
            scene["family"], scene["varied_column"], scene["varied_rank"] = assignments[i % len(assignments)]
            scenes.append(scene)
        scheduled = ((scene, actor) for scene in scenes for actor in (
            by_variant[scene["family"], None, 2],
            by_variant[scene["family"], scene["varied_column"], scene["varied_rank"]]))
    else:
        actors = [character(rng, i + 1) for i in range(args.characters)]
        scenes = [situation(rng, i + 1, args.targets) for i in range(args.situations)]
        scheduled = itertools.product(scenes, actors)
    requested_calls = len(scenes) * (2 if controlled else len(actors))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "setup.json").write_text(json.dumps({"seed": args.seed, "model": args.model,
        "design": "three-at-two" if controlled else "abcd", "targets": args.targets,
        "requested_calls": requested_calls, "characters": actors, "situations": scenes}, indent=2) + "\n", encoding="utf-8")
    rows = []
    spent = 0.0
    known_cost = 0.0
    calls = 0
    invalid = 0
    request_errors = 0
    tasks = iter(enumerate(scheduled))
    next_task = next(tasks, None)
    # Persist each response immediately: a provider error does not erase earlier paid calls.
    with (args.output / "trials.jsonl").open("w", encoding="utf-8") as f, (
        args.output / "rejected.jsonl"
    ).open("w", encoding="utf-8") as rejected, (
        args.output / "request_errors.jsonl"
    ).open("w", encoding="utf-8") as errors, ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = {}
        reserved = 0.0
        while next_task is not None or pending:
            while next_task is not None and len(pending) < args.workers:
                index, (scene, actor) = next_task
                prompt = action_prompt(actor, scene)
                # Reserve worst-case input bytes and the full output allowance
                # for every outstanding request, not just completed calls.
                reserve = len(prompt.encode("utf-8")) * input_price + MAX_OUTPUT_TOKENS * output_price
                if spent + reserved + reserve > args.max_cost:
                    if not pending:
                        next_task = None
                    break
                future = executor.submit(ask_openrouter, api_key, args.model, prompt)
                pending[future] = (index, scene, actor, reserve)
                reserved += reserve
                next_task = next(tasks, None)
            if not pending:
                break
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                index, scene, actor, reserve = pending.pop(future)
                reserved -= reserve
                try:
                    content, usage = future.result()
                except (TimeoutError, ConnectionError, urllib.error.URLError, json.JSONDecodeError) as exc:
                    if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                        raise
                    # A timed-out request might have been billed. Charge its whole
                    # reservation against the remaining budget; do not score it.
                    spent += reserve
                    calls += 1
                    request_errors += 1
                    errors.write(json.dumps({"character_id": actor["id"], "scene_id": scene["id"],
                                             "error": str(exc), "reserved_cost": reserve}) + "\n")
                    errors.flush()
                    continue
                spent += usage["cost"]
                known_cost += usage["cost"]
                calls += 1
                try:
                    proposal = json.loads(content)
                except (TypeError, json.JSONDecodeError) as exc:
                    invalid += 1
                    rejected.write(json.dumps({"character_id": actor["id"], "scene_id": scene["id"],
                                               "error": f"invalid JSON: {exc}",
                                               "raw_response": content, "usage": usage}) + "\n")
                    rejected.flush()
                    continue
                try:
                    assessed = assess(actor, proposal)
                except ValueError as exc:
                    invalid += 1
                    rejected.write(json.dumps({"character_id": actor["id"], "scene_id": scene["id"],
                                               "error": str(exc), "proposal": proposal,
                                               "usage": usage}) + "\n")
                    rejected.flush()
                    continue
                if controlled:
                    row = {"character_id": actor["id"], "scene_id": scene["id"],
                           "family": actor["family"], "varied_column": actor["varied_column"],
                           "varied_rank": actor["varied_rank"], "ranks": actor["ranks"],
                           "stats": actor["stats"], "scene_theme": scene["theme"],
                           "target": scene["target"], "possible": True,
                           "proposal": proposal, "usage": usage, "tag_count": len(assessed["tags"]),
                           **assessed}
                    f.write(json.dumps(row) + "\n")
                    f.flush()
                    rows.append(row)
                    continue
                odds = probabilities(assessed["pool"], scene["target"])
                thrown = roll(random.Random(args.seed + index), assessed["pool"], scene["target"])
                row = {"character_id": actor["id"], "scene_id": scene["id"],
                       "ranks": actor["ranks"], "stats": actor["stats"],
                       "scene_theme": scene["theme"], "target": scene["target"],
                       "mode": "current", "possible": True, "proposal": proposal, "usage": usage,
                       **assessed, **thrown, "odds": odds}
                f.write(json.dumps(row) + "\n")
                f.flush()
                rows.append(row)
    (args.output / "report.json").write_text(json.dumps({"model": args.model, "requested_calls":
        requested_calls, "calls": calls, "valid": len(rows), "rejected": invalid,
        "request_errors": request_errors, "cost": known_cost, "cost_upper_bound": spent,
        "max_cost": args.max_cost}, indent=2) + "\n", encoding="utf-8")
    if not controlled:
        summary(rows, args.output)
        outcomes_chart(rows, args.output)
        chart(args.output, 10, max(args.targets))
    print(f"{calls} attempts: {len(rows)} validated, {invalid} rejected, {request_errors} transport errors; "
          f"${known_cost:.4f} recorded (at most ${spent:.4f}). See {args.output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    odds = sub.add_parser("chart", help="write exact probability SVG and CSV, no API needed")
    odds.add_argument("--output", type=Path, default=Path("auto_play_testing"))
    odds.add_argument("--max-pool", type=int, default=10)
    odds.add_argument("--max-target", type=int, default=5)
    trials = sub.add_parser("run", help="run ABCD characters with one model call per scene")
    controlled = sub.add_parser("run-controlled", help="hold three ranks at 2 and vary the fourth")
    for command, default_output, default_situations in (
        (trials, "auto_play_testing/results", 10),
        (controlled, "auto_play_testing/results/controlled", 1000),
    ):
        command.add_argument("--output", type=Path, default=Path(default_output))
        command.add_argument("--model", required=True, help="OpenRouter model ID")
        command.add_argument("--seed", type=int, default=42)
        command.add_argument("--situations", type=int, default=default_situations)
        command.add_argument("--targets", type=int, nargs="+", default=[1, 2, 3, 4])
        command.add_argument("--max-cost", type=float, default=5.0)
        command.add_argument("--workers", type=int, default=8)
    trials.add_argument("--characters", type=int, default=10)
    controlled.add_argument("--families", type=int, default=6)
    args = parser.parse_args()
    if args.command == "chart":
        if args.max_pool < 0 or args.max_target < 1:
            parser.error("max-pool must be >= 0 and max-target must be >= 1")
        chart(args.output, args.max_pool, args.max_target)
    else:
        if (args.situations < 1 or args.workers < 1
                or args.max_cost <= 0 or any(t < 1 for t in args.targets)):
            parser.error("situations, targets, workers and max-cost must all be positive")
        if args.command == "run" and args.characters < 1:
            parser.error("characters must be positive")
        if args.command == "run-controlled" and (args.families < 1 or args.situations % 4):
            parser.error("families must be positive and situations must be a multiple of four")
        run(args)


if __name__ == "__main__":
    main()
