#!/usr/bin/env python3
import csv
import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_TSV = ROOT / "irish_driving_test_2026_safe_anki.tsv"
OUTPUT_TSV = ROOT / "irish_driving_test_2026_web_visual_anki.tsv"
OUTPUT_SOURCES = ROOT / "web_image_sources.csv"
MEDIA_DIR = ROOT / "web_anki_media"
ANKI_MEDIA_DIR = Path.home() / "Library/Application Support/Anki2/User 1/collection.media"
USER_AGENT = "CodexDrivingDeckBuilder/1.0 (local study use)"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80]


def fetch_json(url: str):
    time.sleep(0.9 if "wikimedia.org" in url else 0.25)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def download(url: str, path: Path):
    time.sleep(1.5 if "wikimedia.org" in url else 0.35)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp, open(path, "wb") as f:
        f.write(resp.read())


def search_commons(query: str):
    url = (
        "https://commons.wikimedia.org/w/api.php?action=query"
        "&generator=search&gsrnamespace=6"
        f"&gsrsearch={urllib.parse.quote(query)}"
        "&prop=imageinfo&iiprop=url&iiurlwidth=900&format=json"
    )
    try:
        data = fetch_json(url)
    except Exception:
        return None

    pages = list(data.get("query", {}).get("pages", {}).values())
    if not pages:
        return None

    def score(page):
        title = page.get("title", "").lower()
        score = 0
        if "ie road sign" in title:
            score += 10
        if "svg" in title:
            score += 5
        if "ireland" in title or "irish" in title:
            score += 4
        if "pdf" in title or "djvu" in title:
            score -= 20
        if "road" in title:
            score += 2
        if "sign" in title:
            score += 2
        if "geograph" in title:
            score += 1
        return score

    pages.sort(key=score, reverse=True)
    best = pages[0]
    info = (best.get("imageinfo") or [{}])[0]
    return {
        "engine": "commons",
        "query": query,
        "title": best.get("title", ""),
        "image_url": info.get("thumburl") or info.get("url"),
        "source_url": info.get("descriptionurl") or "",
        "creator": "",
        "license": "",
    }


def search_openverse(query: str):
    url = (
        "https://api.openverse.org/v1/images"
        f"?q={urllib.parse.quote(query)}&page_size=10"
    )
    try:
        data = fetch_json(url)
    except Exception:
        return None

    results = data.get("results", [])
    if not results:
        return None

    allowed_licenses = {"cc0", "pdm", "by", "by-sa", "by-nc", "by-nc-sa", "by-nd", "by-nc-nd"}

    def score(item):
        title = (item.get("title") or "").lower()
        score = 0
        if item.get("license") in allowed_licenses:
            score += 2
        if any(bad in title for bad in ("pdf", "djvu", "book", "register", "regulation")):
            score -= 10
        for word in query.lower().split():
            if len(word) > 2 and word in title:
                score += 1
        if item.get("thumbnail"):
            score += 2
        return score

    results.sort(key=score, reverse=True)
    best = results[0]
    return {
        "engine": "openverse",
        "query": query,
        "title": best.get("title") or "",
        "image_url": best.get("thumbnail") or best.get("url") or "",
        "source_url": best.get("foreign_landing_url") or best.get("url") or "",
        "creator": best.get("creator") or "",
        "license": best.get("license") or "",
    }


def choose_source(question: str, answer: str, tags: str):
    q = question.lower()
    if "built-up area" in q:
        return [("commons", "IE road sign F-401-50")]
    if "7 february 2025" in q or "60 km/h" in answer:
        return [("commons", "IE road sign F-401-60")]
    if "regional roads" in q:
        return [("commons", "Ireland speed limit 80 km/h road sign")]
    if "national roads" in q:
        return [("commons", "Ireland speed limit 100 km/h road sign")]
    if "motorways" in q and "speed limit" in q:
        return [("commons", "Ireland speed limit 120 km/h road sign")]
    if "posted speed limit" in q:
        return [("commons", "Ireland speed limit signs")]
    if "roundabout" in q:
        return [("commons", "IE road sign 115")]
    if "crossroads" in q:
        return [("commons", "Ireland crossroads warning sign")]
    if "stop sign" in q and "school warden" not in q:
        return [("commons", "Ireland stop sign road sign")]
    if "yield sign" in q:
        return [("commons", "IE road sign RUS-026")]
    if "flashing amber traffic light" in q:
        return [("openverse", "amber traffic light"), ("commons", "Ireland flashing amber traffic light")]
    if "steady amber traffic light" in q:
        return [("openverse", "amber traffic light"), ("commons", "Ireland traffic light amber")]
    if "railway crossing" in q:
        return [("openverse", "railway crossing warning lights"), ("commons", "railway crossing lights road")]
    if "filter light" in q:
        return [("openverse", "green traffic filter arrow"), ("commons", "traffic signal arrow green")]
    if "yellow box junction" in q:
        return [("commons", "Ireland yellow box junction road marking")]
    if "broken white line in the centre" in q:
        return [("commons", "Ireland broken white line road marking")]
    if "continuous white line in the centre" in q:
        return [("commons", "Ireland continuous white line road marking")]
    if "double broken white lines" in q:
        return [("commons", "Ireland double broken white line road marking")]
    if "continuous and a broken white line" in q:
        return [("commons", "Ireland continuous broken white line road marking")]
    if "broken yellow line" in q:
        return [("commons", "Ireland broken yellow line road marking")]
    if "single continuous yellow line" in q:
        return [("commons", "Ireland yellow line no parking road marking")]
    if "double continuous yellow lines" in q:
        return [("commons", "Ireland double yellow line road marking")]
    if "zig-zag lines" in q:
        return [("openverse", "zebra crossing zig zag road"), ("commons", "zebra crossing zig zag road marking")]
    if "no entry" in q and "road markings" in q:
        return [("commons", "Ireland no entry road marking"), ("openverse", "no entry road marking")]
    if "warning signs" in q:
        return [("commons", "Irish warning road sign"), ("openverse", "warning road sign ireland")]
    if "regulatory signs" in q:
        return [("commons", "Irish regulatory road sign"), ("openverse", "regulatory road sign ireland")]
    if "motorway signs" in q:
        return [("commons", "Ireland motorway sign blue")]
    if "national road signs" in q:
        return [("commons", "Ireland national road sign green")]
    if "regional and local road signs" in q:
        return [("commons", "Ireland local road sign white")]
    if "dipped headlights" in q:
        return [("commons", "dipped headlights symbol"), ("openverse", "car dipped headlights dashboard symbol")]
    if "dazzled by headlights" in q:
        return [("openverse", "headlights glare night driving")]
    if "horn" in q:
        return [("openverse", "car horn symbol"), ("commons", "car horn symbol")]
    if "tyre tread" in q:
        return [("openverse", "tyre tread depth gauge"), ("commons", "tyre tread depth gauge")]
    if "2-second rule" in q:
        return [("openverse", "safe following distance cars road")]
    if "wet weather" in q or "braking distance" in q:
        return [("openverse", "dangerous driving in the rain tips")]
    if "aquaplaning" in q:
        return [("openverse", "wet day driving")]
    if "tailgating" in q:
        return [("openverse", "tailgating cars road")]
    if "coasting" in q:
        return [("openverse", "manual gear stick neutral car"), ("commons", "gear stick neutral car")]
    if "another driver is overtaking" in q:
        return [("openverse", "cars overtaking road"), ("commons", "overtaking traffic road")]
    if "overtake on the left" in q:
        return [("openverse", "slow moving traffic two lane road"), ("commons", "dual carriageway traffic lanes")]
    if "should not overtake" in q:
        return [("commons", "overtaking prohibited road sign"), ("openverse", "hill crest road no overtaking")]
    if "far from a junction" in q:
        return [("openverse", "car parked near junction"), ("commons", "parking at junction road")]
    if "pedestrian crossing" in q and "not park" in q:
        return [("commons", "zebra crossing road marking"), ("openverse", "pedestrian crossing zig zag road")]
    if "close to the kerb" in q:
        return [("openverse", "car parked by kerb"), ("commons", "parked car kerb")]
    if "hard shoulder" in q and "motorway" in q:
        return [("commons", "motorway hard shoulder"), ("openverse", "motorway hard shoulder road")]
    if "minimum age" in q:
        return [("commons", "Lplate.svg"), ("openverse", "learner driver car")]
    if "display on the vehicle" in q:
        return [("commons", "Lplate.svg")]
    if "must a learner driver be accompanied" in q:
        return [("openverse", "driving lesson instructor car"), ("commons", "Lplate.svg")]
    if "seatbelt" in q:
        return [("openverse", "seat belt buckle car")]
    if "penalty point" in q:
        return [("openverse", "warning traffic penalty points"), ("commons", "traffic warning sign")]
    if "purpose of the nct" in q:
        return [("openverse", "vehicle inspection garage"), ("commons", "vehicle inspection car")]
    if "which lane should you normally use on a motorway" in q:
        return [("commons", "motorway lanes traffic"), ("openverse", "motorway lane road")]
    if "school warden" in q:
        return [("commons", "IE road sign RUS-032"), ("openverse", "school crossing guard stop sign")]
    if "mobile phones" in q:
        return [("openverse", "hand held phone in car"), ("commons", "Hand held phone in car")]
    if "right turn in a one-way street" in q:
        return [("commons", "one way road sign turn right"), ("openverse", "one way street right turn")]
    if "u-turn" in q:
        return [("commons", "no u-turn road sign"), ("openverse", "no u turn road sign")]
    if "country roads" in q:
        return [("openverse", "country road bend farm tractor"), ("commons", "country road ireland")]
    if "multi-lane dual carriageway" in q:
        return [("commons", "dual carriageway lane 1 left lane"), ("openverse", "dual carriageway road")]
    if "with-flow and a contra-flow bus lane" in q:
        return [("commons", "Ireland bus lane road sign"), ("openverse", "bus lane road sign")]
    if "pelican crossing" in q:
        return [("openverse", "pelican crossing zebra crossing"), ("commons", "zebra crossing sign")]
    if "island in the middle of a pedestrian crossing" in q:
        return [("openverse", "pedestrian refuge island crossing"), ("commons", "pedestrian refuge island")]
    if "secondary controls" in q:
        return [("openverse", "car dashboard wiper controls"), ("commons", "car dashboard controls")]
    if "technical checks" in q:
        return [("openverse", "vehicle inspection car bonnet tyre"), ("commons", "car bonnet tyre check")]
    if "alcohol limit for learner" in q:
        return [("openverse", "drink driving warning sign"), ("commons", "do not drink and drive sign")]
    if "alcohol limit for most other drivers" in q:
        return [("openverse", "drink driving warning sign"), ("commons", "do not drink and drive sign")]
    if "before opening your car door" in q:
        return [("openverse", "dutch reach car door cyclist")]
    if "break down on a motorway" in q:
        return [("openverse", "broken down car motorway hard shoulder"), ("commons", "car broken down hard shoulder")]

    if "signs" in tags or "markings" in tags:
        return [("commons", question)]
    return [("openverse", question)]


def find_image(question: str, answer: str, tags: str):
    candidates = choose_source(question, answer, tags)
    for engine, query in candidates:
        if engine == "commons":
            result = search_commons(query)
        else:
            result = search_openverse(query)
        if result and result.get("image_url"):
            return result
    return {
        "engine": "none",
        "query": "",
        "title": "",
        "image_url": "",
        "source_url": "",
        "creator": "",
        "license": "",
    }


def main():
    MEDIA_DIR.mkdir(exist_ok=True)
    rows = []

    with open(INPUT_TSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for idx, row in enumerate(reader, start=1):
            if len(row) < 3:
                continue
            question, answer, tags = row[:3]
            result = find_image(question, answer, tags)
            ext = ".jpg"
            image_url = result.get("image_url") or ""
            if ".png" in image_url:
                ext = ".png"
            elif ".svg" in image_url:
                ext = ".svg"
            filename = f"webq_{idx:02d}_{slugify(question)}{ext}"
            local_path = MEDIA_DIR / filename
            if image_url:
                try:
                    if not local_path.exists():
                        download(image_url, local_path)
                    if ANKI_MEDIA_DIR.exists():
                        shutil.copy2(local_path, ANKI_MEDIA_DIR / filename)
                except Exception as exc:
                    print(f"warning: failed to download {question}: {exc}", file=sys.stderr)
            img_html = f'<br><img src="{filename}" style="max-width:420px;">' if image_url else ""
            rows.append(
                {
                    "question": question,
                    "answer": answer + img_html,
                    "tags": tags + " web_image",
                    "engine": result.get("engine", ""),
                    "query": result.get("query", ""),
                    "title": result.get("title", ""),
                    "image_url": image_url,
                    "source_url": result.get("source_url", ""),
                    "creator": result.get("creator", ""),
                    "license": result.get("license", ""),
                    "filename": filename,
                }
            )

    with open(OUTPUT_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        for row in rows:
            writer.writerow([row["question"], row["answer"], row["tags"]])

    with open(OUTPUT_SOURCES, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "question",
                "filename",
                "engine",
                "query",
                "title",
                "image_url",
                "source_url",
                "creator",
                "license",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["question"],
                    row["filename"],
                    row["engine"],
                    row["query"],
                    row["title"],
                    row["image_url"],
                    row["source_url"],
                    row["creator"],
                    row["license"],
                ]
            )


if __name__ == "__main__":
    main()
