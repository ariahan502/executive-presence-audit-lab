from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from random import Random
import re
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app

@dataclass(frozen=True)
class PageContext:
    page_url: str
    page_title: str
    content_theme: str
    message_framing: str
    funnel_stage_intent: str
    landing_page: str
    article_slug: str = ""
    path_history: str = ""


PAGE_CONTEXTS = {
    "home": PageContext("/", "Executive Presence Audit Lab", "general_hub", "authority", "awareness", "/"),
    "audit": PageContext("/executive-presence-audit", "Executive Presence Audit", "executive_presence", "authority", "conversion", "/executive-presence-audit"),
    "finance": PageContext("/for-women-in-finance", "Executive Presence for Women in Finance", "women_in_finance", "industry_specific", "consideration", "/for-women-in-finance"),
    "client": PageContext("/for-client-facing-leaders", "For Client-Facing Leaders", "client_facing_credibility", "practical", "consideration", "/for-client-facing-leaders"),
    "newsletter": PageContext("/newsletter", "Newsletter Signup", "newsletter_capture", "practical", "consideration", "/newsletter"),
    "consultation": PageContext("/consultation-request", "Request a Consultation", "consultation", "conversion", "conversion", "/consultation-request"),
    "article_finance": PageContext("/articles/women-in-finance", "What Women in Finance Often Get Wrong About Leadership Presence", "women_in_finance", "industry_specific", "awareness", "/articles/women-in-finance", "women-in-finance", "/articles/women-in-finance"),
    "article_promotion": PageContext("/articles/promotion-signals", "How Executive Presence Shapes Promotion Signals", "executive_presence", "authority", "awareness", "/articles/promotion-signals", "promotion-signals", "/articles/promotion-signals"),
    "article_client": PageContext("/articles/visual-credibility", "Why Client-Facing Professionals Need Visual Credibility", "client_facing_credibility", "practical", "awareness", "/articles/visual-credibility", "visual-credibility", "/articles/visual-credibility"),
}


UTM_OPTIONS = [
    ("", "", ""),
    ("google", "cpc", "finance_search"),
    ("linkedin", "social", "leadership_social"),
    ("newsletter", "email", "nurture_series"),
    ("partner", "referral", "trusted_intros"),
    ("linkedin", "paid_social", "exec_presence_paid"),
]


class TrafficSeeder:
    def __init__(self, rng: Random):
        self.rng = rng
        self.app = create_app()
        self.client = self.app.test_client()
        self.session_counter = self._existing_counter("raw_events", "session_id", r"sess_seed_(\d+)", default=1000)
        self.person_counter = self._existing_counter("raw_events", "anonymous_id", r"anon_seed_(\d+)", default=1000)

    def _existing_counter(self, table_name: str, column_name: str, pattern: str, *, default: int) -> int:
        regex = re.compile(pattern)
        db_path = BASE_DIR / "instance" / "app.db"
        conn = sqlite3.connect(db_path)
        try:
            max_value = default
            query = f"select {column_name} from {table_name} where {column_name} like ?"
            for (raw_value,) in conn.execute(query, ("%seed_%",)):
                if not raw_value:
                    continue
                match = regex.search(str(raw_value))
                if match:
                    max_value = max(max_value, int(match.group(1)))
            return max_value
        finally:
            conn.close()

    def next_ids(self):
        self.session_counter += 1
        self.person_counter += 1
        return f"anon_seed_{self.person_counter}", f"sess_seed_{self.session_counter}"

    def pick_utm(self):
        return self.rng.choice(UTM_OPTIONS)

    def maybe_referrer(self):
        return self.rng.choice(
            [
                "https://example.com",
                "https://www.google.com/",
                "https://www.linkedin.com/",
                "https://mail.google.com/",
            ]
        )

    def post_event(self, event_name: str, context: PageContext, anonymous_id: str, session_id: str, *, cta_label: str = "", form_name: str = "", path_history: str | None = None, utm_source: str = "", utm_medium: str = "", utm_campaign: str = "", referrer: str = "https://example.com"):
        payload = {
            "event_name": event_name,
            "anonymous_id": anonymous_id,
            "session_id": session_id,
            "page_url": context.page_url,
            "page_title": context.page_title,
            "content_theme": context.content_theme,
            "message_framing": context.message_framing,
            "funnel_stage_intent": context.funnel_stage_intent,
            "cta_label": cta_label,
            "form_name": form_name,
            "article_slug": context.article_slug,
            "path_history": path_history if path_history is not None else context.path_history,
            "landing_page": context.landing_page,
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "referrer": referrer,
            "traffic_type": "synthetic",
        }
        response = self.client.post("/events", json=payload)
        assert response.status_code == 202, response.get_data(as_text=True)

    def submit_newsletter(self, context: PageContext, anonymous_id: str, session_id: str, *, email: str, job_title: str, industry: str, path_history: str, utm_source: str, utm_medium: str, utm_campaign: str, referrer: str = "https://example.com"):
        response = self.client.post(
            "/newsletter-signup",
            data={
                "email": email,
                "job_title": job_title,
                "industry": industry,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "landing_page": context.page_url,
                "page_title": context.page_title,
                "content_theme": context.content_theme,
                "message_framing": context.message_framing,
                "funnel_stage_intent": context.funnel_stage_intent,
                "form_name": "newsletter",
                "article_slug": context.article_slug,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "referrer": referrer,
                "traffic_type": "synthetic",
            },
        )
        assert response.status_code == 302, response.status_code

    def submit_consultation(self, context: PageContext, anonymous_id: str, session_id: str, *, name: str, email: str, job_title: str, industry: str, company_size: str, primary_goal: str, urgent_challenge: str, path_history: str, utm_source: str, utm_medium: str, utm_campaign: str, referrer: str = "https://example.com"):
        response = self.client.post(
            "/consultation-request",
            data={
                "name": name,
                "email": email,
                "job_title": job_title,
                "industry": industry,
                "company_size": company_size,
                "primary_goal": primary_goal,
                "urgent_challenge": urgent_challenge,
                "anonymous_id": anonymous_id,
                "session_id": session_id,
                "landing_page": context.page_url,
                "content_path_summary": path_history,
                "page_title": context.page_title,
                "content_theme": context.content_theme,
                "message_framing": context.message_framing,
                "funnel_stage_intent": context.funnel_stage_intent,
                "form_name": "consultation",
                "article_slug": context.article_slug,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "referrer": referrer,
                "traffic_type": "synthetic",
            },
        )
        assert response.status_code == 302, response.status_code

    def run_newsletter_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        article = self.rng.choice([PAGE_CONTEXTS["article_promotion"], PAGE_CONTEXTS["article_client"], PAGE_CONTEXTS["article_finance"]])
        newsletter = PAGE_CONTEXTS["newsletter"]
        path_history = f"{article.page_url} > {newsletter.page_url}"
        referrer = self.maybe_referrer()
        self.post_event("article_view", article, anonymous_id, session_id, path_history=article.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", article, anonymous_id, session_id, cta_label="article_to_newsletter", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("newsletter_form_start", newsletter, anonymous_id, session_id, form_name="newsletter", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.submit_newsletter(newsletter, anonymous_id, session_id, email=f"newsletter{session_id}@example.com", job_title=self.rng.choice(["Manager", "Senior Manager", "Consultant"]), industry=self.rng.choice(["Finance", "Consulting", "Tech"]), path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_finance_consultation_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.rng.choice(
            [("google", "cpc", "finance_search"), ("linkedin", "paid_social", "exec_presence_paid")]
        )
        finance = PAGE_CONTEXTS["finance"]
        consultation = PAGE_CONTEXTS["consultation"]
        path_history = f"{finance.page_url} > {consultation.page_url}"
        referrer = self.maybe_referrer()
        self.post_event("page_view", finance, anonymous_id, session_id, path_history=finance.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", finance, anonymous_id, session_id, cta_label="finance_to_audit", path_history=finance.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.submit_consultation(consultation, anonymous_id, session_id, name=f"Finance Lead {session_id}", email=f"finance{session_id}@example.com", job_title=self.rng.choice(["Director", "VP", "Head of Strategy"]), industry="Finance", company_size=self.rng.choice(["201-1000", "1000+"]), primary_goal=self.rng.choice(["Executive readiness", "Promotion visibility", "Leadership presence"]), urgent_challenge=self.rng.choice(["Sharpen leadership signaling with senior stakeholders", "Improve executive credibility in a high-visibility finance environment"]), path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_client_consultation_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.rng.choice(
            [("linkedin", "social", "client_credibility_push"), ("partner", "referral", "trusted_intros")]
        )
        article = PAGE_CONTEXTS["article_client"]
        client_page = PAGE_CONTEXTS["client"]
        consultation = PAGE_CONTEXTS["consultation"]
        article_path = article.page_url
        full_path = f"{article.page_url} > {client_page.page_url} > {consultation.page_url}"
        referrer = self.maybe_referrer()
        self.post_event("article_view", article, anonymous_id, session_id, path_history=article_path, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", article, anonymous_id, session_id, cta_label="article_to_next_step", path_history=f"{article.page_url} > {client_page.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("page_view", client_page, anonymous_id, session_id, path_history=f"{article.page_url} > {client_page.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", client_page, anonymous_id, session_id, cta_label="client_facing_to_consultation", path_history=full_path, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=full_path, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.submit_consultation(consultation, anonymous_id, session_id, name=f"Client Lead {session_id}", email=f"client{session_id}@example.com", job_title=self.rng.choice(["Client Partner", "Manager", "Founder"]), industry=self.rng.choice(["Consulting", "Advisory", "Tech"]), company_size=self.rng.choice(["51-200", "201-1000"]), primary_goal=self.rng.choice(["Client-facing credibility", "Executive communication", "Leadership presence"]), urgent_challenge=self.rng.choice(["Build stronger credibility in high-stakes client settings", "Translate expertise into more authoritative client presence"]), path_history=full_path, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_consultation_abandon_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        origin = self.rng.choice([PAGE_CONTEXTS["finance"], PAGE_CONTEXTS["client"], PAGE_CONTEXTS["audit"]])
        consultation = PAGE_CONTEXTS["consultation"]
        path_history = f"{origin.page_url} > {consultation.page_url}"
        referrer = self.maybe_referrer()
        self.post_event("page_view", origin, anonymous_id, session_id, path_history=origin.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", origin, anonymous_id, session_id, cta_label="view_consultation_form", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_mixed_exploration_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        start = self.rng.choice([PAGE_CONTEXTS["home"], PAGE_CONTEXTS["article_promotion"], PAGE_CONTEXTS["article_finance"]])
        mid = self.rng.choice([PAGE_CONTEXTS["audit"], PAGE_CONTEXTS["finance"], PAGE_CONTEXTS["client"]])
        end = self.rng.choice([PAGE_CONTEXTS["newsletter"], PAGE_CONTEXTS["consultation"]])
        referrer = self.maybe_referrer()
        path_one = start.page_url
        path_two = f"{start.page_url} > {mid.page_url}"
        path_three = f"{start.page_url} > {mid.page_url} > {end.page_url}"
        self.post_event("article_view" if start.article_slug else "page_view", start, anonymous_id, session_id, path_history=path_one, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", start, anonymous_id, session_id, cta_label="explore_path", path_history=path_two, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("page_view", mid, anonymous_id, session_id, path_history=path_two, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        if end is PAGE_CONTEXTS["newsletter"]:
            self.post_event("newsletter_form_start", end, anonymous_id, session_id, form_name="newsletter", path_history=path_three, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        else:
            self.post_event("consultation_form_start", end, anonymous_id, session_id, form_name="consultation", path_history=path_three, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_newsletter_then_consultation_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        article = self.rng.choice([PAGE_CONTEXTS["article_promotion"], PAGE_CONTEXTS["article_finance"]])
        newsletter = PAGE_CONTEXTS["newsletter"]
        audit = PAGE_CONTEXTS["audit"]
        consultation = PAGE_CONTEXTS["consultation"]
        referrer = self.maybe_referrer()
        path_history = f"{article.page_url} > {newsletter.page_url} > {audit.page_url} > {consultation.page_url}"
        self.post_event("article_view", article, anonymous_id, session_id, path_history=article.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", article, anonymous_id, session_id, cta_label="article_to_newsletter", path_history=f"{article.page_url} > {newsletter.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("newsletter_form_start", newsletter, anonymous_id, session_id, form_name="newsletter", path_history=f"{article.page_url} > {newsletter.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.submit_newsletter(newsletter, anonymous_id, session_id, email=f"hybrid{session_id}@example.com", job_title=self.rng.choice(["Senior Manager", "Director", "Consultant"]), industry=self.rng.choice(["Finance", "Consulting", "Tech"]), path_history=f"{article.page_url} > {newsletter.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("page_view", audit, anonymous_id, session_id, path_history=f"{article.page_url} > {newsletter.page_url} > {audit.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        if self.rng.random() < 0.5:
            self.submit_consultation(consultation, anonymous_id, session_id, name=f"Hybrid Lead {session_id}", email=f"hybrid_consult{session_id}@example.com", job_title=self.rng.choice(["Director", "Head of Strategy"]), industry=self.rng.choice(["Finance", "Consulting"]), company_size=self.rng.choice(["51-200", "201-1000", "1000+"]), primary_goal=self.rng.choice(["Leadership presence", "Promotion visibility", "Executive readiness"]), urgent_challenge=self.rng.choice(["Need a clearer executive signal before a promotion cycle", "Want stronger presence in senior client and stakeholder settings"]), path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_low_signal_consultation_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        origin = self.rng.choice([PAGE_CONTEXTS["audit"], PAGE_CONTEXTS["finance"]])
        consultation = PAGE_CONTEXTS["consultation"]
        referrer = self.maybe_referrer()
        path_history = f"{origin.page_url} > {consultation.page_url}"
        self.post_event("page_view", origin, anonymous_id, session_id, path_history=origin.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        if self.rng.random() < 0.5:
            self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.submit_consultation(consultation, anonymous_id, session_id, name=f"Low Signal Lead {session_id}", email=f"low_signal{session_id}@example.com", job_title=self.rng.choice(["Manager", "Director"]), industry=self.rng.choice(["Finance", "Consulting", "Tech"]), company_size=self.rng.choice(["51-200", "201-1000"]), primary_goal=self.rng.choice(["Promotion visibility", "Executive readiness"]), urgent_challenge=self.rng.choice(["Need help quickly sharpening executive presence", "Want a sharper leadership signal before upcoming reviews"]), path_history=path_history, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_high_engagement_no_submit_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        article = self.rng.choice([PAGE_CONTEXTS["article_client"], PAGE_CONTEXTS["article_finance"], PAGE_CONTEXTS["article_promotion"]])
        mid = self.rng.choice([PAGE_CONTEXTS["client"], PAGE_CONTEXTS["finance"], PAGE_CONTEXTS["audit"]])
        consultation = PAGE_CONTEXTS["consultation"]
        referrer = self.maybe_referrer()
        path_two = f"{article.page_url} > {mid.page_url}"
        path_three = f"{article.page_url} > {mid.page_url} > {consultation.page_url}"
        self.post_event("article_view", article, anonymous_id, session_id, path_history=article.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", article, anonymous_id, session_id, cta_label="explore_more", path_history=path_two, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("page_view", mid, anonymous_id, session_id, path_history=path_two, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("cta_click", mid, anonymous_id, session_id, cta_label="open_consultation", path_history=path_three, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        self.post_event("consultation_form_start", consultation, anonymous_id, session_id, form_name="consultation", path_history=path_three, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        if self.rng.random() < 0.5:
            newsletter = PAGE_CONTEXTS["newsletter"]
            self.post_event("newsletter_form_start", newsletter, anonymous_id, session_id, form_name="newsletter", path_history=f"{path_three} > {newsletter.page_url}", utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def run_browse_only_journey(self):
        anonymous_id, session_id = self.next_ids()
        utm_source, utm_medium, utm_campaign = self.pick_utm()
        page = self.rng.choice([PAGE_CONTEXTS["home"], PAGE_CONTEXTS["audit"], PAGE_CONTEXTS["finance"], PAGE_CONTEXTS["client"]])
        referrer = self.maybe_referrer()
        self.post_event("page_view", page, anonymous_id, session_id, path_history=page.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)
        if self.rng.random() < 0.5:
            self.post_event("cta_click", page, anonymous_id, session_id, cta_label="explore_only", path_history=page.page_url, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, referrer=referrer)

    def seed(self, sessions: int):
        journey_methods = [
            (self.run_finance_consultation_journey, 0.2),
            (self.run_client_consultation_journey, 0.18),
            (self.run_newsletter_journey, 0.18),
            (self.run_newsletter_then_consultation_journey, 0.14),
            (self.run_low_signal_consultation_journey, 0.08),
            (self.run_high_engagement_no_submit_journey, 0.1),
            (self.run_consultation_abandon_journey, 0.12),
            (self.run_mixed_exploration_journey, 0.08),
            (self.run_browse_only_journey, 0.02),
        ]
        total_weight = sum(weight for _, weight in journey_methods)
        for _ in range(sessions):
            roll = self.rng.random() * total_weight
            cursor = 0.0
            for method, weight in journey_methods:
                cursor += weight
                if roll <= cursor:
                    method()
                    break


def parse_args():
    parser = argparse.ArgumentParser(description="Seed synthetic funnel traffic into the local SQLite database.")
    parser.add_argument("--sessions", type=int, default=24, help="Number of synthetic sessions to create.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible traffic generation.")
    return parser.parse_args()


def main():
    args = parse_args()
    rng = Random(args.seed)
    seeder = TrafficSeeder(rng)
    seeder.seed(args.sessions)
    print(f"Seeded {args.sessions} synthetic sessions with seed={args.seed}.")


if __name__ == "__main__":
    main()
