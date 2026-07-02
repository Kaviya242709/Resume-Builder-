import re

STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "shall",
    "can",
    "not",
    "no",
    "its",
    "it",
    "this",
    "that",
    "these",
    "those",
    "you",
    "your",
    "we",
    "our",
    "they",
    "their",
    "as",
    "if",
    "so",
    "than",
    "then",
    "when",
    "where",
    "who",
    "what",
    "how",
    "which",
    "any",
    "all",
    "each",
    "both",
    "more",
    "most",
    "also",
    "just",
    "only",
    "about",
    "after",
    "before",
    "between",
    "into",
    "through",
    "during",
    "across",
    "within",
    "without",
    "against",
    "over",
    "under",
    "above",
    "below",
    "up",
    "down",
    "out",
    "off",
    "again",
    "further",
    "once",
    "here",
    "there",
    "why",
    "while",
    "although",
    "because",
    "since",
    "until",
    "unless",
    "whether",
    "work",
    "working",
    "experience",
    "skills",
    "ability",
    "strong",
    "good",
    "great",
    "new",
    "team",
    "role",
    "company",
    "business",
    "looking",
    "seeking",
    "candidate",
    "years",
    "year",
    "least",
    "must",
    "including",
    "using",
    "used",
    "use",
    "build",
    "built",
    "develop",
    "developed",
    "manage",
    "managed",
    "provide",
    "provided",
    "support",
    "supported",
    "able",
    "proven",
    "real",
    "things",
    "person",
    "people",
    "ensure",
    "where",
    "what",
    "from",
    "they",
    "their",
    # ── additional low-signal boilerplate words often picked up from JD formatting ──
    "required",
    "minimum",
    "qualifications",
    "plus",
    "mandatory",
    "familiarity",
    "basic",
    "solid",
    "bachelor",
    "degree",
    "computer",
    "related",
    "field",
    "e.g",
    "eg",
    "advantageous",
}

MULTI_WORD_KEYWORDS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "computer vision",
    "data science",
    "data engineering",
    "data analysis",
    "power bi",
    "power automate",
    "power apps",
    "azure devops",
    "azure ai",
    "azure ml",
    "azure machine learning",
    "microsoft azure",
    "github actions",
    "ci/cd",
    "agile/scrum",
    "prompt engineering",
    "large language model",
    "generative ai",
    "reinforcement learning",
    "feature engineering",
    "software testing",
    "test automation",
    "api integration",
    "no-code",
    "low-code",
    "stakeholder management",
    "scikit-learn",
    "hugging face",
    "openai api",
    "langchain",
    "langgraph",
    "chromadb",
    "mcp server",
    "rag pipeline",
    "n8n",
    "make.com",
    "power platform",
    "penetration testing",
    "threat modelling",
    "incident response",
    "security operations",
    "risk assessment",
    "financial modelling",
    "business analysis",
    "project management",
    "product management",
    "ux design",
    "user research",
    "a/b testing",
    "test lifecycle",
    "defect lifecycle",
    "problem-solving",
]


def extract_jd_keywords(jd_text: str) -> list:
    text_lower = jd_text.lower()
    found = []

    for kw in MULTI_WORD_KEYWORDS:
        if kw in text_lower:
            found.append(kw)

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9\+\#\/\-\.]{2,}\b", jd_text)
    seen = set(kw.lower() for kw in found)
    for word in words:
        w = word.lower()
        if w in STOPWORDS or len(w) < 3:
            continue
        already_covered = any(w in kw for kw in seen)
        if already_covered or w in seen:
            continue
        seen.add(w)
        found.append(word)

    seen_final = set()
    result = []
    for k in found:
        kl = k.lower()
        if kl not in seen_final:
            seen_final.add(kl)
            result.append(k)
    return result


def check_cv_for_keyword(keyword: str, cv_text: str) -> bool:
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return bool(pattern.search(cv_text))


def _fallback_resources(keyword: str) -> list:
    q = keyword.replace(" ", "+")
    return [
        f"📺 YouTube: https://www.youtube.com/results?search_query={q}+tutorial+beginners",
        f"📚 Google: https://www.google.com/search?q=learn+{q}+free+course",
        f"📖 Search: https://www.google.com/search?q={q}+documentation",
    ]


def get_resources_via_ai_batch(keywords: list, jd_context: str, brain) -> dict:
    """Ask the AI for learning resources for ALL missing keywords in a single call.
    This replaces the old one-call-per-keyword approach to avoid burning
    through API rate/quota limits. Returns {keyword: [line1, line2, line3]}."""
    if not keywords:
        return {}

    kw_list_str = "\n".join(f"- {kw}" for kw in keywords)
    prompt = f"""
A job candidate is missing these skills for this role:
{jd_context[:500]}

Missing skills:
{kw_list_str}

For EACH skill listed above, give exactly 3 real learning resources.
Return the result in EXACTLY this format, one block per skill, in the same order as listed:

### <skill name>
📚 Course: <title> — <url>
📺 YouTube: <search title or channel> — <url>
📖 Docs/Reference: <title> — <url>

Use ONLY real, working URLs. No made-up links.
No intro text, no explanation outside the blocks. Output ONLY the blocks.
"""
    result = brain.think(prompt)
    resources_map = {}

    if result:
        blocks = result.split("### ")
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            if not lines:
                continue
            kw_name = lines[0].strip()
            body_lines = lines[1:4]
            match = next((k for k in keywords if k.lower() == kw_name.lower()), None)
            if match and body_lines:
                resources_map[match] = body_lines

    # Fill in fallback (generic search links) for anything the AI missed/skipped
    for kw in keywords:
        if kw not in resources_map or not resources_map[kw]:
            resources_map[kw] = _fallback_resources(kw)

    return resources_map


def run_keyword_match(jd_text: str, cv_text: str, final_latex: str, brain) -> str:
    print("\n" + "─" * 52)
    print("   KEYWORD MATCH REPORT")
    print("─" * 52)

    keywords = extract_jd_keywords(jd_text)
    if not keywords:
        print("  No keywords extracted from JD.")
        print("─" * 52)
        return final_latex

    found_kws = []
    missing_kws = []

    for kw in keywords:
        if check_cv_for_keyword(kw, cv_text):
            found_kws.append(kw)
        else:
            missing_kws.append(kw)

    for kw in found_kws:
        print(f"  {kw}")
    for kw in missing_kws:
        print(f"  ❌  {kw}")

    total = len(keywords)
    matched = len(found_kws)
    score = int((matched / total) * 100) if total > 0 else 0

    print("─" * 52)
    print(f"  Match Score: {score}%  ({matched}/{total} keywords matched)")
    print(f"  Reason: {len(missing_kws)} keywords from the JD are missing in your CV.")
    print("─" * 52)

    if not missing_kws:
        print("\n  Your CV covers all JD keywords!")
        return final_latex

    print("\n  Missing keywords — add only what you KNOW:")
    for i, kw in enumerate(missing_kws, 1):
        print(f"   [{i}] {kw}")

    print()
    print("  Warning!, Only add keywords you can explain in an interview.")
    print()

    raw = input("Enter numbers you know (e.g. 1,3) or press Enter to skip: ").strip()

    if not raw:
        print(
            "\n  No keywords added. Fetching learning resources for all missing keywords...\n"
        )
        _show_resources_for_all(missing_kws, jd_text, brain)
        return final_latex

    selected_indices = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(missing_kws):
                selected_indices.append(idx)

    selected = [missing_kws[i] for i in selected_indices]
    not_selected = [kw for i, kw in enumerate(missing_kws) if i not in selected_indices]

    if not selected:
        print("\n  No valid selections.")
        _show_resources_for_all(missing_kws, jd_text, brain)
        return final_latex

    confirmed = []
    skipped = []
    print()

    for kw in selected:
        answer = (
            input(f"  '{kw}' : Is this for your interview? (yes/no): ").strip().lower()
        )
        if answer in ("yes", "y"):
            confirmed.append(kw)
            print(f"'{kw}' will be added to your CV.\n")
        else:
            skipped.append(kw)

    # Batch-fetch resources for all skipped + not-selected keywords in ONE call
    needs_resources = skipped + not_selected
    if needs_resources:
        print(f"Fetching resources for {len(needs_resources)} keyword(s)...\n")
        resources_map = get_resources_via_ai_batch(needs_resources, jd_text, brain)

        if skipped:
            for kw in skipped:
                print(f"  → {kw}")
                for r in resources_map.get(kw, []):
                    print(f"      {r}")
                print()

        if not_selected:
            print("Resources for other missing keywords:\n")
            for kw in not_selected:
                print(f"  → {kw}")
                for r in resources_map.get(kw, []):
                    print(f"      {r}")
                print()

    if not confirmed:
        print("  Nothing added to CV.")
        return final_latex

    # Inject confirmed keywords into skills table in final_latex
    keywords_str = ", ".join(confirmed)
    inject_line = f"\\resumeSectionType{{Additional Skills}}{{:}}{{{keywords_str}}}"
    final_latex = final_latex.replace(
        "\\end{tabularx}", inject_line + "\n\\end{tabularx}", 1
    )

    print(f"\n Added to Skills: {keywords_str}")
    print("─" * 52)

    return final_latex


def _show_resources_for_all(missing_kws: list, jd_text: str, brain):
    print(" Learning resources for missing keywords:\n")
    resources_map = get_resources_via_ai_batch(missing_kws, jd_text, brain)
    for kw in missing_kws:
        print(f"  → {kw}")
        for r in resources_map.get(kw, []):
            print(f"      {r}")
        print()
