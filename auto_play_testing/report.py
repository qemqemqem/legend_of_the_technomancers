"""Produce a PDF analysis of a saved play-test run (no API calls).

Requires matplotlib and scipy; the simulation itself remains standard-library only.
Run: python3 -m auto_play_testing.report auto_play_testing/results/large-2026-v2 \
     --output auto_play_testing/playtest_report.pdf
"""

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import statistics
import textwrap


INK = "#172a38"
PAPER = "#f7f4ed"
TEAL = "#177e84"
ORANGE = "#ca6542"
MUTED = "#5c6c75"
GRID = "#d8dedc"
MODES = (("one-source", TEAL), ("mixed", ORANGE))


def load_run(directory):
    setup = json.loads((directory / "setup.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (directory / "trials.jsonl").read_text(encoding="utf-8").splitlines()]
    rejects = [json.loads(line) for line in (directory / "rejected.jsonl").read_text(encoding="utf-8").splitlines()]
    all_responses = rows + rejects
    keys = [(r["scene_id"], r["character_id"], r["mode"]) for r in all_responses]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate character/scene/mode responses")
    counts = Counter(r["scene_id"] for r in all_responses)
    complete = [scene["id"] for scene in setup["situations"]
                if counts[scene["id"]] == 2 * len(setup["characters"])]
    if not complete:
        raise ValueError("no scenes with every character and both modes sampled")
    return setup, rows, rejects, complete


def character_interval(rows, value):
    """Equal-weight character means; 95% t interval conditional on these scenes."""
    from scipy.stats import t

    by_character = defaultdict(list)
    for row in rows:
        by_character[row["character_id"]].append(value(row))
    means = [statistics.mean(values) for values in by_character.values()]
    if not means:
        return None
    point = statistics.mean(means)
    n = len(means)
    if n < 3:
        return point, 0.0, 1.0, n  # Too few independent builds for a useful CI.
    half = t.ppf(0.975, n - 1) * statistics.stdev(means) / math.sqrt(n)
    return point, max(0.0, point - half), min(1.0, point + half), n


def pair_interval(pairs):
    """Per-character matched mixed-minus-one-source differences in success chance."""
    from scipy.stats import t

    by_character = defaultdict(list)
    for one, mixed in pairs:
        by_character[one["character_id"]].append(one["odds"]["failure"] - mixed["odds"]["failure"])
    means = [statistics.mean(values) for values in by_character.values()]
    if not means:
        return None
    n = len(means)
    point = statistics.mean(means)
    if n < 3:
        return point, -1.0, 1.0, n
    half = t.ppf(0.975, n - 1) * statistics.stdev(means) / math.sqrt(n)
    return point, max(-1.0, point - half), min(1.0, point + half), n


def make_report(directory, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import FancyBboxPatch

    setup, all_rows, all_rejects, complete = load_run(directory)
    rows = [r for r in all_rows if r["scene_id"] in complete]
    rejects = [r for r in all_rejects if r["scene_id"] in complete]
    index = {(r["scene_id"], r["character_id"], r["mode"]): r for r in rows}
    pairs = [(r, index[(r["scene_id"], r["character_id"], "mixed")])
             for r in rows if r["mode"] == "one-source"
             and (r["scene_id"], r["character_id"], "mixed") in index]
    delta = pair_interval(pairs)
    total_cost = sum(r["usage"]["cost"] for r in all_rows + all_rejects)
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.edgecolor": GRID, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED,
                         "text.color": INK, "figure.facecolor": PAPER,
                         "savefig.facecolor": PAPER})

    def page(title, subtitle, number):
        fig = plt.figure(figsize=(11.7, 8.3), facecolor=PAPER)
        fig.text(.065, .955, "LEGEND OF THE TECHNOMANCERS / FIELD REPORT 01",
                 fontsize=9, weight="bold", color=TEAL)
        fig.text(.065, .892, title, fontsize=27, weight="bold", color=INK)
        fig.text(.065, .855, subtitle, fontsize=11, color=MUTED)
        fig.add_artist(plt.Line2D([.065, .935], [.834, .834], transform=fig.transFigure,
                                  color=GRID, lw=1.5))
        fig.text(.065, .045, "EXPERIMENTAL / AI-SELECTED ACTIONS / NOT A BALANCE VERDICT",
                 fontsize=8, color=MUTED)
        fig.text(.935, .045, f"{number} / 4", ha="right", fontsize=9, color=MUTED)
        return fig

    def finish(pdf, fig):
        pdf.savefig(fig, dpi=160)
        plt.close(fig)

    with PdfPages(output, metadata={"Title": "Legend of the Technomancers - Play-test field report",
                                    "Author": "Auto Play Testing", "Subject": "Interrupted 2026 simulation analysis"}) as pdf:
        # Page 1: scope and paired finding.
        fig = page("What the first 467 calls say", "Seed 2026 | google/gemini-2.5-flash | interrupted before 1,000 calls", 1)
        cards = (("467", "paid calls saved"), (str(len(all_rows)), "valid actions"),
                 (str(len(all_rejects)), "mechanical rejections"), (f"${total_cost:.3f}", "recorded API spend"))
        for i, (value, label) in enumerate(cards):
            x = .065 + i * .224
            fig.add_artist(FancyBboxPatch((x, .707), .203, .105, transform=fig.transFigure,
                           boxstyle="round,pad=0.007,rounding_size=0.012", facecolor="white", edgecolor=GRID))
            fig.text(x + .015, .752, value, fontsize=23, weight="bold", color=INK)
            fig.text(x + .015, .725, label, fontsize=9, color=MUTED)
        fig.text(.068, .648, "FAIR COMPARISON SET", fontsize=11, weight="bold", color=TEAL)
        fig.text(.068, .610, f"{len(complete)} fully sampled scenes x {len(setup['characters'])} characters x 2 tag rules"
                 f" = {len(rows) + len(rejects)} calls.", fontsize=12)
        fig.text(.068, .575, f"{len(rows)} valid; {len(rejects)} rejected. The partly sampled next scene is excluded"
                 " from all comparisons below.", fontsize=11, color=MUTED)
        fig.text(.068, .510, "MIXING TAG SOURCES: A SMALL, UNCERTAIN GAIN", fontsize=11,
                 weight="bold", color=TEAL)
        ax = fig.add_axes((.095, .356, .57, .125), facecolor=PAPER)
        ax.axvline(0, color=INK, lw=1)
        ax.hlines(0, 100 * delta[1], 100 * delta[2], lw=5, color=TEAL)
        ax.plot(100 * delta[0], 0, "o", color=ORANGE, markersize=11, zorder=3)
        ax.set_xlim(-30, 30)
        ax.set_ylim(-.5, .5)
        ax.set_yticks([])
        ax.set_xlabel("Mixed minus one-source: partial-or-better chance (percentage points)")
        ax.grid(axis="x", color=GRID, lw=.7)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.text(.7, .424, f"{delta[0] * 100:+.1f} pp", fontsize=24, weight="bold", color=INK)
        fig.text(.7, .385, f"95% interval: {delta[1] * 100:+.1f} to {delta[2] * 100:+.1f} pp",
                 fontsize=10, color=MUTED)
        fig.text(.7, .356, f"{len(pairs)} valid paired scenes / {delta[3]} characters", fontsize=10, color=MUTED)
        fig.text(.068, .255, "HOW TO READ THIS", fontsize=11, weight="bold", color=TEAL)
        fig.text(.068, .207, textwrap.fill(
            "Success here means partial or better. Each valid dice pool is converted to its exact "
            "d6 success probability, avoiding noise from a single roll. Error bars measure variation "
            "between character builds across the nine fixed scenes, not uncertainty about new scenes.", 100),
            fontsize=10, va="top", linespacing=1.6)
        fig.text(.068, .119, "Caution: the AI can overclaim a tag even when its response passes mechanical validation.",
                 fontsize=10, weight="bold", color=ORANGE)
        finish(pdf, fig)

        # Page 2: rank allocation and independent-build intervals.
        fig = page("How build priorities performed", "Mean exact partial-or-better chance, by assigned column rank", 2)
        positions = ((.08, .55, .39, .24), (.55, .55, .39, .24),
                     (.08, .22, .39, .22), (.55, .22, .39, .22))
        for column, pos in zip(("Body", "Stuff", "Skills", "Magic"), positions):
            ax = fig.add_axes(pos, facecolor=PAPER)
            group_counts = Counter(a["ranks"][column] for a in setup["characters"])
            for mode, color in MODES:
                for rank in range(1, 5):
                    subset = [r for r in rows if r["mode"] == mode and r["ranks"][column] == rank]
                    interval = character_interval(subset, lambda r: 1 - r["odds"]["failure"])
                    if not interval:
                        continue
                    point, low, high, n = interval
                    x = rank + (-.085 if mode == "one-source" else .085)
                    ax.errorbar(x, point * 100, yerr=[[100 * (point - low)], [100 * (high - point)]],
                                fmt="o", markersize=5, capsize=3, color=color, elinewidth=1.4)
            ax.set(title=f"{column} priority", ylim=(0, 100), xlim=(.55, 4.45),
                   xticks=range(1, 5), xticklabels=[f"{i}\nn={group_counts[i]}" for i in range(1, 5)])
            ax.set_yticks((0, 25, 50, 75, 100))
            ax.set_yticklabels(("0%", "25%", "50%", "75%", "100%"))
            ax.grid(axis="y", color=GRID, lw=.7)
            ax.spines[["right", "top"]].set_visible(False)
            ax.tick_params(axis="x", length=0, pad=6)
        fig.text(.08, .140, "Teal: one-source     Orange: mixed", fontsize=10, weight="bold", color=INK)
        fig.text(.08, .114, "Bars: 95% t intervals across independent character means, conditional on these scenes.",
                 fontsize=9)
        fig.text(.08, .089, "n counts characters, not rolls. With fewer than 3 characters, the entire 0-100% range",
                 fontsize=9, color=MUTED)
        fig.text(.08, .067, "is shown rather than a misleading narrow interval. Ranks trade off under ABCD priorities.",
                 fontsize=9, color=MUTED)
        finish(pdf, fig)

        # Page 3: context and the principal missing-data mechanism.
        fig = page("The scene matters as much as the sheet", "What pushes back changes both the dice pool and feasibility", 3)
        kinds = ("Body", "Mind", "Face", "Weird")
        ax = fig.add_axes((.08, .47, .53, .3), facecolor=PAPER)
        for mode, color in MODES:
            for i, kind in enumerate(kinds):
                group = [r for r in rows if r["mode"] == mode and r["scene_stat"] == kind]
                interval = character_interval(group, lambda r: 1 - r["odds"]["failure"])
                if interval:
                    point, low, high, _ = interval
                    ax.errorbar(i + (-.09 if mode == "one-source" else .09), 100 * point,
                                yerr=[[100 * (point - low)], [100 * (high - point)]],
                                fmt="o", color=color, capsize=4, markersize=6)
        ax.set(ylim=(0, 100), xlim=(-.55, 3.55), ylabel="Partial or better (exact chance)",
               xticks=range(4), xticklabels=kinds)
        ax.grid(axis="y", color=GRID)
        ax.spines[["right", "top"]].set_visible(False)
        fig.text(.65, .743, "Why Weird drops away", fontsize=15, weight="bold", color=TEAL)
        fig.text(.65, .698, textwrap.fill("Historical data: this run mistakenly required a "
                 "Technique/Form pair, which is not a rule. Its Weird results and "
                 "rejection counts must not be treated as current play.", 39),
                 fontsize=11, va="top", linespacing=1.5)
        fig.text(.08, .410, "WHAT HAPPENED TO ALL 450 RESPONSES IN COMPLETE SCENES?", fontsize=11,
                 weight="bold", color=TEAL)
        ax2 = fig.add_axes((.11, .18, .77, .18), facecolor=PAPER)
        palette = (("Feasible action", TEAL), ("Model said impossible", "#d3a15b"),
                   ("Rejected response", ORANGE))
        for i, kind in enumerate(kinds):
            accepted = [r for r in rows if r["scene_stat"] == kind]
            rejected = [r for r in rejects if next(s["stat"] for s in setup["situations"]
                                                    if s["id"] == r["scene_id"]) == kind]
            total = len(accepted) + len(rejected)
            if not total:
                ax2.text(102, i, "n=0", va="center", fontsize=9, color=MUTED)
                continue
            values = (sum(r["possible"] for r in accepted), sum(not r["possible"] for r in accepted),
                      len(rejected))
            left = 0
            for count, (_, color) in zip(values, palette):
                ax2.barh(i, count / total * 100, left=left, color=color, height=.58)
                left += count / total * 100
            ax2.text(102, i, f"n={total}", va="center", fontsize=9, color=MUTED)
        ax2.set(xlim=(0, 114), yticks=range(4), yticklabels=kinds, xticks=(0, 25, 50, 75, 100))
        ax2.set_xticklabels(("0%", "25%", "50%", "75%", "100%"))
        ax2.invert_yaxis()
        ax2.spines[:].set_visible(False)
        ax2.grid(axis="x", color=GRID, zorder=0)
        for j, (name, color) in enumerate(palette):
            x = .12 + j * .26
            fig.add_artist(plt.Rectangle((x, .105), .016, .015, transform=fig.transFigure,
                                         color=color, clip_on=False))
            fig.text(x + .022, .105, name, fontsize=9, color=MUTED)
        finish(pdf, fig)

        # Page 4: paired dice, rejections and interpretation.
        fig = page("The rule change, under a microscope", "Matched scenes isolate the tag rule; model choices still differ", 4)
        differences = Counter(b["pool"] - a["pool"] for a, b in pairs)
        ax = fig.add_axes((.08, .54, .51, .22), facecolor=PAPER)
        xvalues = list(range(min(differences), max(differences) + 1))
        ax.bar(xvalues, [differences.get(x, 0) for x in xvalues], color=[
               ORANGE if x > 0 else TEAL if x < 0 else MUTED for x in xvalues], width=.78)
        ax.set(xlabel="Mixed pool minus one-source pool (dice)", ylabel="Matched character-scenes",
               xticks=xvalues)
        ax.spines[["right", "top"]].set_visible(False)
        ax.grid(axis="y", color=GRID)
        fig.text(.645, .728, f"{len(pairs)}", fontsize=27, weight="bold", color=INK)
        fig.text(.645, .693, "pairs with both responses valid", fontsize=11, color=MUTED)
        fig.text(.645, .634, f"{sum(b['pool'] > a['pool'] for a,b in pairs)} higher / "
                 f"{sum(b['pool'] == a['pool'] for a,b in pairs)} tied / "
                 f"{sum(b['pool'] < a['pool'] for a,b in pairs)} lower", fontsize=11)
        fig.text(.645, .587, "in mixed mode", fontsize=11, color=MUTED)
        stripped = sum(bool(r["stripped_tag_ids"]) for r in rows if r["mode"] == "one-source")
        fig.text(.645, .515, f"{stripped} one-source responses had tags stripped", fontsize=10)
        fig.text(.08, .428, "WHERE THE MODEL BROKE THE RULES", fontsize=11, weight="bold", color=TEAL)
        errors = Counter(r["error"] for r in rejects)
        for i, (error, count) in enumerate(errors.most_common()):
            label = error.replace("magic action needs a Technique and a Form", "Obsolete pair check")
            label = label.replace("reality-only action needs magic tags", "Weird without magic tags")
            label = label.replace("action must use the GM-set resistance stat", "Wrong resistance stat")
            label = label.replace("tag not owned", "Unowned tag")
            fig.text(.085, .387 - .045 * i, label, fontsize=10)
            fig.text(.57, .387 - .045 * i, str(count), fontsize=10, weight="bold", ha="right")
        fig.text(.645, .404, "INTERPRETATION LIMITS", fontsize=11, weight="bold", color=TEAL)
        limitations = (
            "Only 9 of 20 generated scenes were fully sampled; these target and stat mixes are not representative.",
            "One rank-4 Body group has 2 characters; all priority ranks are linked by ABCD allocation.",
            "Invalid calls are excluded, not treated as in-world failures. Fictional tag applicability is not verified.",
        )
        for i, line in enumerate(limitations):
            fig.text(.645, .37 - i * .084, textwrap.fill(line, 44), fontsize=9.5,
                     va="top", linespacing=1.4)
        fig.text(.08, .125, f"Source: {directory}/setup.json, trials.jsonl, rejected.jsonl.", fontsize=9, color=MUTED)
        fig.text(.08, .094, "The PDF reports the interrupted run, not a new simulation. No API calls were made.",
                 fontsize=9, color=MUTED)
        finish(pdf, fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="directory containing setup.json and JSONL results")
    parser.add_argument("--output", type=Path, default=Path("auto_play_testing/playtest_report.pdf"))
    args = parser.parse_args()
    print(make_report(args.run_dir, args.output))


if __name__ == "__main__":
    main()
