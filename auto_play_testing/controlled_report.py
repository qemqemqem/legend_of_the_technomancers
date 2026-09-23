"""Dice-pool report for an off-grid, three-columns-at-rank-2 play test.

Requires matplotlib and scipy. No OpenRouter calls are made.
Run: python3 -m auto_play_testing.controlled_report RUN_DIR \
     --output auto_play_testing/controlled_report.pdf
"""

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random
import statistics
import textwrap

from .core import Character, controlled_characters
from .report import GRID, INK, MUTED, ORANGE, PAPER, TEAL


def load_controlled(directory):
    setup = json.loads((directory / "setup.json").read_text(encoding="utf-8"))
    if setup.get("design") != "three-at-two":
        raise ValueError("report requires a run-controlled dataset")
    valid = [json.loads(line) for line in (directory / "trials.jsonl").read_text(encoding="utf-8").splitlines()]
    rejected = [json.loads(line) for line in (directory / "rejected.jsonl").read_text(encoding="utf-8").splitlines()]
    errors_file = directory / "request_errors.jsonl"
    errors = [json.loads(line) for line in errors_file.read_text(encoding="utf-8").splitlines()] if errors_file.exists() else []
    keys = [(row["scene_id"], row["character_id"]) for row in valid + rejected + errors]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate character/scene results")
    return setup, valid, rejected, errors


def group_rows(rows, column, rank):
    return [row for row in rows if row["varied_column"] == column and row["varied_rank"] == rank
            or rank == 2 and row["varied_column"] is None]


def family_interval(rows, value, lower=0, upper=10):
    """t interval over independent family means, not over correlated rolls."""
    from scipy.stats import t

    by_family = defaultdict(list)
    for row in rows:
        by_family[row["family"]].append(value(row))
    if not by_family:
        return None
    means = [statistics.mean(values) for values in by_family.values()]
    point = statistics.mean(means)
    n = len(means)
    if n < 3:
        return point, lower, upper, n
    half = t.ppf(.975, n - 1) * statistics.stdev(means) / math.sqrt(n)
    return point, max(lower, point - half), min(upper, point + half), n


def matched_changes(rows, column, rank):
    """Only compare family-scene cells with valid baseline AND variant."""
    baseline = {(row["family"], row["scene_id"]): row for row in rows
                if row["varied_column"] is None}
    return [(row, baseline[(row["family"], row["scene_id"])])
            for row in group_rows(rows, column, rank)
            if (row["family"], row["scene_id"]) in baseline]


def usage_counts(setup, rows):
    """Count applied dice and actions by source, excluding unfeasible actions."""
    actors = {actor["id"]: actor for actor in setup["characters"]}
    bases = Counter()
    tag_dice = Counter()
    tag_actions = Counter()
    by_stat = defaultdict(lambda: {"feasible": 0, "item": 0})
    for row in rows:
        base = "Item" if row["item_id"] else row["base_stat"]
        bases[base] += 1
        by_stat[row["scene_theme"]]["feasible"] += 1
        by_stat[row["scene_theme"]]["item"] += int(base == "Item")
        owned = {tag["id"]: tag["source"] for tag in actors[row["character_id"]]["tags"]}
        sources = [owned[tag_id] for tag_id in row["tags"]]
        tag_dice.update(sources)
        tag_actions.update(set(sources))
    return {"feasible": sum(bases.values()), "bases": bases, "tag_dice": tag_dice,
            "tag_actions": tag_actions, "by_stat": by_stat}


def sheet_profile(actor):
    """Owned tags and raw base ratings, independent of what the AI chose."""
    ratings = list(actor["stats"].values()) + [item["tier"] for item in actor["gear"]]
    if actor["weird"] > 0:
        ratings.append(actor["weird"])
    return {"tags": Counter(tag["source"] for tag in actor["tags"]),
            "rating_sum": sum(ratings), "option_count": len(ratings)}


def fit_rank_trend(means):
    """Fit an equally weighted straight line to rank-level means."""
    if len(means) < 2:
        raise ValueError("a trend needs at least two ranks")
    x_mean = statistics.mean(means)
    y_mean = statistics.mean(means.values())
    slope = sum((rank - x_mean) * (value - y_mean) for rank, value in means.items()) / sum(
        (rank - x_mean) ** 2 for rank in means)
    return slope, y_mean - slope * x_mean


def make_controlled_report(directory, output, sheet_families=500):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    setup, rows, rejected, errors = load_controlled(directory)
    actors = setup["characters"]
    family_count = len({actor["family"] for actor in actors})
    if sheet_families < 1:
        raise ValueError("sheet_families must be positive")
    sheet_actors = controlled_characters(random.Random(setup["seed"] + 1), sheet_families)
    columns = ("Body", "Stuff", "Skills", "Magic")
    sheet_profiles = {(column, rank): [sheet_profile(actor) for actor in group_rows(sheet_actors, column, rank)]
                      for column in columns for rank in (1, 2, 3, 4)}
    sheet_bases = {(column, rank): sum(p["rating_sum"] for p in profiles) /
                   sum(p["option_count"] for p in profiles)
                   for (column, rank), profiles in sheet_profiles.items()}
    sheet_tags = {(column, rank): statistics.mean(sum(p["tags"].values()) for p in profiles)
                  for (column, rank), profiles in sheet_profiles.items()}
    requested = setup["requested_calls"]
    saved = len(rows) + len(rejected) + len(errors)
    known_cost = sum(r["usage"]["cost"] for r in rows + rejected)
    usage = usage_counts(setup, rows)
    feasible = usage["feasible"]
    if not rows or not feasible:
        raise ValueError("report requires validated feasible actions")
    validation = [(len(group_rows(rows, column, rank)),
                   sum(scene["varied_column"] == column and scene["varied_rank"] == rank
                       for scene in setup["situations"]), column, rank)
                   for column in columns for rank in (1, 3, 4)]
    least_valid, least_planned, least_column, least_rank = min(
        (entry for entry in validation if entry[1]), key=lambda result: result[0] / result[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED,
                         "axes.edgecolor": GRID, "figure.facecolor": PAPER,
                         "savefig.facecolor": PAPER})

    def page(number, title, subtitle):
        fig = plt.figure(figsize=(11.7, 8.3), facecolor=PAPER)
        fig.text(.065, .954, "LEGEND OF THE TECHNOMANCERS / CONTROLLED FIELD TEST", color=TEAL,
                 fontsize=9, weight="bold")
        fig.text(.065, .895, title, fontsize=25, weight="bold")
        fig.text(.065, .855, subtitle, fontsize=10.5, color=MUTED)
        fig.add_artist(plt.Line2D([.065, .935], [.835, .835], transform=fig.transFigure,
                                  color=GRID, lw=1.5))
        fig.text(.065, .04, "OFF-GRID EXPERIMENT / AI-SELECTED ACTIONS / NOT A BALANCE VERDICT",
                 fontsize=8, color=MUTED)
        fig.text(.935, .04, f"{number} / 10", ha="right", fontsize=9, color=MUTED)
        return fig

    def save(pdf, fig):
        pdf.savefig(fig)
        plt.close(fig)

    with PdfPages(output, metadata={"Title": "Legend of the Technomancers - Controlled dice-pool report",
                                    "Author": "Auto Play Testing"}) as pdf:
        fig = page(1, "What each pillar contributes", "Paired scenes: rank-2 baseline and one variant per scene")
        positions = ((.08, .55, .39, .24), (.55, .55, .39, .24),
                     (.08, .22, .39, .22), (.55, .22, .39, .22))
        for column, position in zip(columns, positions):
            ax = fig.add_axes(position, facecolor=PAPER)
            means = {}
            for rank in (1, 2, 3, 4):
                group = group_rows(rows, column, rank)
                if not group:
                    continue
                base = statistics.mean(row["base"] for row in group)
                tags = statistics.mean(row["tag_count"] for row in group)
                ax.bar(rank, base, width=.55, color="#8c9ca3")
                ax.bar(rank, tags, width=.55, bottom=base, color=TEAL)
                means[rank] = base + tags
                point, low, high, n = family_interval(group, lambda row: row["pool"])
                ax.errorbar(rank, point, yerr=[[point - low], [high - point]],
                            fmt="none", ecolor=INK, capsize=2.5, elinewidth=1.1)
            if len(means) >= 2:
                slope, intercept = fit_rank_trend(means)
                ax.plot((1, 4), (intercept + slope, intercept + 4 * slope),
                        ls="--", lw=1.7, color=ORANGE, zorder=5)
                ax.set_title(f"{column} rank | {slope:+.2f} dice/rank", fontsize=11)
            ax.set(ylim=(0, 10), xlim=(.55, 4.45),
                   xticks=(1, 2, 3, 4), yticks=(0, 2, 4, 6, 8, 10))
            ax.grid(axis="y", color=GRID, lw=.7)
            ax.set_axisbelow(True)
            ax.spines[["right", "top"]].set_visible(False)
            ax.tick_params(axis="x", pad=6, length=0)
        fig.text(.08, .143, "Slate: base dice    Teal: applied tag dice    Orange dash: rank trend    Whiskers: 95% family intervals",
                  fontsize=10, weight="bold")
        fig.text(.08, .116, f"{len(rows)} valid actions / {saved} saved attempts / {requested} planned; "
                 f"{len(rejected)} mechanical rejections, {len(errors) + requested - saved} missing or transport failures.",
                 fontsize=9)
        fig.text(.08, .09, "Rank means use different scene subsets; whiskers use 95% t intervals across families "
                  "(n<3: full-width bounds).", fontsize=9, color=MUTED)
        fig.text(.08, .067, f"Rank-2 baseline is shared. Fewest valid: {least_column}-{least_rank} "
                 f"({least_valid}/{least_planned}); rejected responses can bias slopes.", fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(2, "Turn just one dial", "Pool change from the same family's all-rank-2 baseline")
        fig.text(.08, .785, "Only family-scene pairs with both actions mechanically valid appear here.",
                  fontsize=10, color=MUTED)
        fig.text(.08, .753, "The model chooses its own objective and action for each character, even in the same scene.",
                 fontsize=9, color=MUTED)
        ax = fig.add_axes((.11, .32, .77, .40), facecolor=PAPER)
        colors = {"Body": TEAL, "Stuff": ORANGE, "Skills": "#7169a3", "Magic": "#b69143"}
        pair_counts = []
        for i, column in enumerate(columns):
            offset = (i - 1.5) * .11
            changes = {2: 0}
            for rank in (1, 3, 4):
                pairs = matched_changes(rows, column, rank)
                pair_counts.append(len(pairs))
                differences = [{"family": variant["family"], "change":
                                variant["pool"] - baseline["pool"]}
                               for variant, baseline in pairs]
                interval = family_interval(differences, lambda r: r["change"], -10, 10)
                if not interval:
                    continue
                point, low, high, n = interval
                changes[rank] = point
                x = rank + offset
                ax.errorbar(x, point, yerr=[[point - low], [high - point]],
                            fmt="o", color=colors[column], capsize=4, markersize=6, zorder=4)
            if len(changes) >= 2:
                slope, intercept = fit_rank_trend(changes)
                ax.plot([rank + offset for rank in (1, 4)],
                        [intercept + slope * rank for rank in (1, 4)],
                        ls="--", lw=1.6, color=colors[column],
                        label=f"{column} {slope:+.2f} dice/rank")
                ax.plot(2 + offset, 0, marker="o", ms=4, color=colors[column])
        ax.axhline(0, color=INK, lw=1)
        ax.set(xlim=(.53, 4.47), ylim=(-5, 6), xticks=(1, 2, 3, 4),
               xlabel="Varied column rank (the other three stay at 2)",
               ylabel="Dice versus matched rank-2 baseline")
        ax.grid(axis="y", color=GRID)
        ax.spines[["right", "top"]].set_visible(False)
        ax.legend(loc="upper left", frameon=False, ncol=2)
        fig.text(.09, .244, f"Each comparison has {min(pair_counts)}-{max(pair_counts)} matched scenes; "
                  f"95% intervals use independent family means (n={family_count}).", fontsize=10)
        fig.text(.09, .222, "Dashed lines fit rank-level matched differences (including the zero baseline).",
                 fontsize=9, color=MUTED)
        fig.text(.09, .199, textwrap.fill(
            "Body and Skills can also change the Body/Mind/Face stat budget. Stuff can supply the "
            "base through an item, including its rank-4 Tier-5 capstone. Magic changes tags and Weird. "
            "Those are the intended mechanisms of each dial, not separately randomized attributes.", 115),
            fontsize=9.5, va="top", linespacing=1.5)
        fig.text(.09, .09, "This design breaks the normal A/B/C/D priority constraint on purpose; "
                 "results describe this test, not legal starting builds.", fontsize=9.5, color=ORANGE)
        save(pdf, fig)

        fig = page(3, "Which base was chosen?", "One listed base per mechanically valid roll")
        kinds = ("Body", "Mind", "Face", "Weird", "Item")
        ax = fig.add_axes((.12, .40, .73, .37), facecolor=PAPER)
        counts = [usage["bases"][kind] for kind in kinds]
        bars = ax.barh(kinds, counts, color=[TEAL] * 4 + [ORANGE], height=.62)
        ax.bar_label(bars, labels=[f"{count}  ({count/feasible:.1%})" for count in counts], padding=6)
        ax.set(xlim=(0, max(counts) * 1.38 + 1), xlabel="Validated rolls")
        ax.invert_yaxis()
        ax.spines[["right", "top", "left"]].set_visible(False)
        ax.grid(axis="x", color=GRID)
        ax.set_axisbelow(True)
        fig.text(.09, .325, "ITEM BASES BY SCENE THEME (NOT A REQUIRED STAT)", fontsize=11,
                 color=TEAL, weight="bold")
        for i, kind in enumerate(("Body", "Mind", "Face", "Weird")):
            stat = usage["by_stat"][kind]
            pct = stat["item"] / stat["feasible"] if stat["feasible"] else 0
            fig.text(.09 + i * .22, .277, kind, fontsize=10, weight="bold")
            fig.text(.09 + i * .22, .245, f"{stat['item']} / {stat['feasible']}  ({pct:.1%})", fontsize=10)
        fig.text(.09, .17, f"Base denominator: {feasible} mechanically valid rolls out of {requested} planned.",
                 fontsize=9.5)
        fig.text(.09, .135, "Item means an owned gear ID was chosen; its printed tier supplied the base dice.",
                 fontsize=9.5, color=MUTED)
        fig.text(.09, .10, f"{len(rejected)} rejected; {len(errors)} transport errors; "
                 f"{requested - saved} unsent/missing. These are excluded from base frequencies.",
                 fontsize=9.5, color=MUTED)
        save(pdf, fig)

        fig = page(4, "Where tag dice came from", "Applied tags after the five-tag cap, across all four domains")
        ax = fig.add_axes((.13, .40, .73, .36), facecolor=PAPER)
        dice = [usage["tag_dice"][source] for source in columns]
        bars = ax.barh(columns, dice, color=[TEAL, ORANGE, "#7169a3", "#b69143"], height=.6)
        ax.bar_label(bars, labels=[f"{n} dice" for n in dice], padding=5)
        ax.set(xlim=(0, max(dice) * 1.3 + 1), xlabel="Applied tag dice")
        ax.invert_yaxis()
        ax.spines[["right", "top", "left"]].set_visible(False)
        ax.grid(axis="x", color=GRID)
        ax.set_axisbelow(True)
        fig.text(.09, .32, "ACTIONS USING AT LEAST ONE TAG FROM EACH DOMAIN", fontsize=11,
                 color=TEAL, weight="bold")
        for i, source in enumerate(columns):
            n = usage["tag_actions"][source]
            fig.text(.09 + i * .22, .27, source, fontsize=10, weight="bold")
            fig.text(.09 + i * .22, .24, f"{n} / {feasible}  ({n/feasible:.1%})", fontsize=10)
        fig.text(.09, .172, f"{sum(dice)} applied tag dice across {feasible} validated rolls; "
                 f"{sum(bool(r['capped_tag_ids']) for r in rows)} valid responses hit the five-tag cap.",
                 fontsize=9.5)
        fig.text(.09, .139, "An action can use multiple domains and multiple tags per domain; "
                 "action percentages need not sum to 100%.", fontsize=9.5, color=MUTED)
        fig.text(.09, .106, f"Recorded model cost: ${known_cost:.3f} across {len(rows) + len(rejected)} billed responses. "
                 f"Unknown billing for {len(errors)} transport errors.", fontsize=9)
        fig.text(.09, .078, "AI judges fictional applicability. Rejections and missing calls can bias "
                  "frequencies; each scene is tested with one baseline/variant pair.", fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(5, "What's on each sheet", "Owned tags and all available base ratings, by varied pillar rank")
        table_positions = ((.085, .515, .39, .245), (.54, .515, .39, .245),
                           (.085, .225, .39, .245), (.54, .225, .39, .245))
        for column, position in zip(columns, table_positions):
            ax = fig.add_axes(position, facecolor=PAPER)
            ax.axis("off")
            ax.set_title(f"{column} rank", loc="left", fontsize=14, color=TEAL, weight="bold")
            cells = []
            for rank in (1, 2, 3, 4):
                profiles = sheet_profiles[column, rank]
                cells.append([str(rank), f"{sheet_tags[column, rank]:.0f}",
                              f"{sheet_bases[column, rank]:.2f}",
                              f"{statistics.mean(p['option_count'] for p in profiles):.1f}"])
            table = ax.table(cellText=cells, colLabels=("Rank", "Tags", "Mean base", "Options"),
                             colWidths=(.17, .18, .39, .25), cellLoc="center", loc="center")
            table.auto_set_font_size(False)
            table.set_fontsize(10.5)
            table.scale(1, 1.8)
            for (row, _), cell in table.get_celld().items():
                cell.set_edgecolor(GRID)
                cell.set_facecolor(TEAL if row == 0 else PAPER if row % 2 == 0 else "#edf2f0")
                if row == 0:
                    cell.get_text().set_color("white")
                    cell.get_text().set_weight("bold")
        fig.text(.09, .161, f"Each variation has {sheet_families} offline-generated sheets, "
                 f"separate from the {family_count} AI-tested families.", fontsize=9.5)
        fig.text(.09, .129, "Tags = mean total owned per sheet; Options = mean count of available "
                 "bases per sheet.", fontsize=9.5, color=MUTED)
        fig.text(.09, .098, "Mean base pools every Body, Mind, Face, nonzero Weird and owned item tier "
                 "across those sheets.", fontsize=9.5, color=MUTED)
        fig.text(.09, .068, "Item tiers are standalone base options; no AI choices or rejected actions "
                 "enter these tables.", fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(6, "Who owns the tags?", "Mean tags on each character sheet, stacked by domain")
        for column, position in zip(columns, positions):
            ax = fig.add_axes(position, facecolor=PAPER)
            for rank in (1, 2, 3, 4):
                profiles = sheet_profiles[column, rank]
                bottom = 0
                for source in columns:
                    count = statistics.mean(p["tags"][source] for p in profiles)
                    ax.bar(rank, count, width=.55, bottom=bottom, color=colors[source])
                    bottom += count
                ax.text(rank, bottom + .35, f"{bottom:.0f}", ha="center", fontsize=9, color=INK)
            means = {rank: sheet_tags[column, rank] for rank in (1, 2, 3, 4)}
            slope, intercept = fit_rank_trend(means)
            ax.plot((1, 4), (intercept + slope, intercept + 4 * slope),
                    ls="--", lw=1.7, color=INK, zorder=5)
            ax.set_title(f"{column} rank | {slope:+.2f} tags/rank", fontsize=11)
            ax.set(ylim=(0, 24), xlim=(.55, 4.45),
                   xticks=(1, 2, 3, 4), yticks=(0, 5, 10, 15, 20))
            ax.grid(axis="y", color=GRID, lw=.7)
            ax.set_axisbelow(True)
            ax.spines[["right", "top"]].set_visible(False)
            ax.tick_params(axis="x", pad=6, length=0)
        for i, source in enumerate(columns):
            x = .085 + i * .21
            fig.add_artist(plt.Rectangle((x, .14), .016, .018, transform=fig.transFigure,
                                         color=colors[source], clip_on=False))
            fig.text(x + .022, .142, source, fontsize=10)
        fig.text(.09, .095, "Numbers above bars: owned tags per sheet; black dashed lines: fitted "
                 "rank trends, not tags selected for actions.", fontsize=9.5, color=MUTED)
        fig.text(.09, .068, f"All bars average {sheet_families} offline families; "
                 "each panel shares the same all-rank-2 baseline.", fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(7, "What bases are available?", "Mean of all printed base ratings on offline character sheets")
        ax = fig.add_axes((.12, .31, .77, .45), facecolor=PAPER)
        for column in columns:
            means = {rank: sheet_bases[column, rank] for rank in (1, 2, 3, 4)}
            slope, intercept = fit_rank_trend(means)
            ax.plot(means.keys(), means.values(), "o", color=colors[column], ms=6)
            ax.plot((1, 4), (intercept + slope, intercept + 4 * slope),
                    ls="--", lw=1.8, color=colors[column],
                    label=f"{column} {slope:+.2f} base dice/rank")
        ax.set(xlim=(.7, 4.3), xticks=(1, 2, 3, 4),
               xlabel="Varied column rank (the other three stay at 2)",
               ylabel="Mean available base rating")
        ax.grid(axis="y", color=GRID)
        ax.spines[["right", "top"]].set_visible(False)
        ax.legend(loc="upper left", frameon=False, ncol=2)
        fig.text(.09, .216, f"Each point pools Body, Mind, Face, nonzero Weird, and every item tier "
                 f"across {sheet_families} offline family sheets.", fontsize=9.5)
        fig.text(.09, .170, "Dashed lines are linear fits to four rank means. Their slopes summarize "
                 "this generated inventory, not an AI choice or a causal effect.", fontsize=9.5, color=MUTED)
        fig.text(.09, .104, "No scene, action, tag selection, or mechanical rejection enters these "
                  "base-rating averages.", fontsize=9.5, color=MUTED)
        save(pdf, fig)

        sample_rng = random.Random(setup["seed"] + 2)
        fig = page(8, "Meet the Travellers", "Random sample from the characters sent to the model")
        for index, actor in enumerate(sample_rng.sample(actors, min(2, len(actors)))):
            x = .075 + index * .46
            lines = str(Character(actor)).splitlines()
            fig.text(x, .795, " / ".join(f"{c} {actor['ranks'][c]}" for c in columns),
                     fontsize=9, weight="bold", color=TEAL)
            fig.text(x, .766, "\n".join(lines), va="top", fontsize=8.1,
                     linespacing=1.18, family="DejaVu Sans Mono")
        fig.text(.075, .072, "Random selection is reproducible from the run seed. Feats are not shown to the model.",
                 fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(9, "What happened?", "Random sample of the shared scenario texts, not prescribed actions")
        for index, scene in enumerate(sample_rng.sample(setup["situations"],
                                                         min(8, len(setup["situations"])))):
            x = .075 + (index % 2) * .46
            y = .785 - (index // 2) * .183
            fig.text(x, y, f"{scene['id']}  /  {scene['theme']} theme  /  target {scene['target']}",
                     fontsize=10, color=TEAL, weight="bold")
            fig.text(x, y - .030, textwrap.fill(scene["text"], 63),
                     va="top", fontsize=9.1, linespacing=1.25)
        fig.text(.075, .065, "Themes stratify the sample; the model sees only scene text and target.",
                 fontsize=9, color=MUTED)
        save(pdf, fig)

        fig = page(10, "How the rolls were built", "Random validated model actions: original plan, selected base and tag dice")
        actor_by_id = {actor["id"]: actor for actor in actors}
        for index, row in enumerate(sample_rng.sample(rows, min(4, len(rows)))):
            x = .075 + (index % 2) * .46
            y = .775 - (index // 2) * .35
            actor = actor_by_id[row["character_id"]]
            tags = {tag["id"]: tag for tag in actor["tags"]}
            item = next((item for item in actor["gear"] if item["id"] == row["item_id"]), None)
            base = f"{item['name']} ({item['id']})" if item else row["base_stat"]
            fig.text(x, y, f"{row['character_id']}  /  {row['scene_id']}",
                     fontsize=10, color=TEAL, weight="bold")
            fig.text(x, y - .035, textwrap.fill("Action: " + row["proposal"]["action_plan"], 63),
                     va="top", fontsize=9.1, linespacing=1.25)
            fig.text(x, y - .115, f"Base: {base} = {row['base']} dice", fontsize=9.2, weight="bold")
            chosen = [f"{tags[tag_id]['source']}: {tags[tag_id]['name']} (+1)" for tag_id in row["tags"]]
            fig.text(x, y - .144, "\n".join(chosen) if chosen else "No tags selected",
                     va="top", fontsize=9.1, linespacing=1.32)
            fig.text(x, y - .282, f"{row['base']} base + {len(chosen)} tag(s) = {row['pool']} dice",
                     fontsize=9.5, weight="bold", color=ORANGE)
        fig.text(.075, .065, "Shown after mechanical validation and the five-tag cap; applicability needs GM review.",
                 fontsize=9, color=MUTED)
        save(pdf, fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("auto_play_testing/controlled_report.pdf"))
    parser.add_argument("--sheet-families", type=int, default=500,
                        help="independent offline families for sheet metrics (default: 500)")
    args = parser.parse_args()
    print(make_controlled_report(args.run_dir, args.output, args.sheet_families))


if __name__ == "__main__":
    main()
