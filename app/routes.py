from dataclasses import dataclass

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for

from .content_registry import CONTENT_BY_SLUG, CONTENT_BY_URL


bp = Blueprint("main", __name__)


@dataclass(frozen=True)
class PageMeta:
    title: str
    content_theme: str
    message_framing: str
    funnel_stage_intent: str


ARTICLES = {
    "promotion-signals": {
        "meta": PageMeta(
            title="How Executive Presence Shapes Promotion Signals",
            content_theme="executive_presence",
            message_framing="authority",
            funnel_stage_intent="awareness",
        ),
        "sections": [
            {
                "heading": "Performance is not the only promotion signal",
                "body": "Strong output matters, but senior stakeholders also look for leadership readiness, communication confidence, and whether someone already feels promotion-caliber in visible settings.",
            },
            {
                "heading": "Presence influences how readiness is interpreted",
                "body": "Executive presence can affect whether a professional is seen as steady under pressure, persuasive with senior audiences, and credible when representing a team or function.",
            },
            {
                "heading": "Three common gaps",
                "body": "High-performing professionals often undersignal authority, rely on inconsistent visual cues, or default to tactical communication patterns that do not reinforce executive readiness.",
            },
        ],
        "cta_label": "See Whether an Executive Presence Audit Could Help",
        "cta_target": "main.audit",
    },
    "visual-credibility": {
        "meta": PageMeta(
            title="Why Client-Facing Professionals Need Visual Credibility",
            content_theme="client_facing_credibility",
            message_framing="practical",
            funnel_stage_intent="awareness",
        ),
        "sections": [
            {
                "heading": "Trust forms quickly in client-facing roles",
                "body": "In advisory, consulting, partnerships, and sales environments, professional credibility is often judged before a conversation is finished. Presence shapes how expertise lands.",
            },
            {
                "heading": "Visual signals support communication signals",
                "body": "Even when the underlying expertise is strong, misaligned cues can make communication feel less authoritative, less polished, or less consistent with the level of responsibility expected.",
            },
            {
                "heading": "What stronger credibility looks like",
                "body": "It is not about looking fashionable. It is about reinforcing steadiness, clarity, and trust through a more coherent leadership presentation.",
            },
        ],
        "cta_label": "Explore the Audit for Client-Facing Leaders",
        "cta_target": "main.client_facing",
    },
    "women-in-finance": {
        "meta": PageMeta(
            title="What Women in Finance Often Get Wrong About Leadership Presence",
            content_theme="women_in_finance",
            message_framing="industry_specific",
            funnel_stage_intent="awareness",
        ),
        "sections": [
            {
                "heading": "High-performance environments amplify signaling",
                "body": "In finance, visibility can be high, expectations can be conservative, and small perception gaps can meaningfully affect how authority is interpreted.",
            },
            {
                "heading": "Overcorrecting can create a new mismatch",
                "body": "Some professionals try to disappear into the norms of the environment, while others focus on polish without clarifying what their leadership presence is supposed to communicate.",
            },
            {
                "heading": "The goal is aligned authority",
                "body": "A stronger presence in finance should support credibility, steadiness, and leadership readiness without sacrificing clarity of identity or role alignment.",
            },
        ],
        "cta_label": "Explore Executive Presence for Women in Finance",
        "cta_target": "main.finance",
    },
}


def page_payload(meta: PageMeta):
    return {
        "page_title": meta.title,
        "page_meta": meta,
        "tracking_endpoint": url_for("main.capture_event"),
    }


def log_event(event_name, **payload):
    db = current_app.get_db()
    db.execute(
        """
        insert into raw_events (
            event_name, anonymous_id, session_id, page_url, page_title,
            content_theme, message_framing, funnel_stage_intent, cta_label,
            form_name, article_slug, path_history, landing_page,
            utm_source, utm_medium, utm_campaign, referrer, traffic_type
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_name,
            payload.get("anonymous_id"),
            payload.get("session_id"),
            payload.get("page_url"),
            payload.get("page_title"),
            payload.get("content_theme"),
            payload.get("message_framing"),
            payload.get("funnel_stage_intent"),
            payload.get("cta_label"),
            payload.get("form_name"),
            payload.get("article_slug"),
            payload.get("path_history"),
            payload.get("landing_page"),
            payload.get("utm_source"),
            payload.get("utm_medium"),
            payload.get("utm_campaign"),
            payload.get("referrer"),
            payload.get("traffic_type", "live"),
        ),
    )
    db.commit()


def event_payload_from_form(form):
    return {
        "anonymous_id": form.get("anonymous_id"),
        "session_id": form.get("session_id"),
        "page_url": form.get("landing_page"),
        "page_title": form.get("page_title"),
        "content_theme": form.get("content_theme"),
        "message_framing": form.get("message_framing"),
        "funnel_stage_intent": form.get("funnel_stage_intent"),
        "form_name": form.get("form_name"),
        "article_slug": form.get("article_slug"),
        "path_history": form.get("content_path_summary"),
        "landing_page": form.get("landing_page"),
        "utm_source": form.get("utm_source"),
        "utm_medium": form.get("utm_medium"),
        "utm_campaign": form.get("utm_campaign"),
        "referrer": form.get("referrer"),
        "traffic_type": form.get("traffic_type", "live"),
    }


@bp.route("/")
def home():
    asset = CONTENT_BY_URL["/"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("home.html", **page_payload(meta))


@bp.route("/executive-presence-audit")
def audit():
    asset = CONTENT_BY_URL["/executive-presence-audit"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("audit.html", **page_payload(meta))


@bp.route("/for-women-in-finance")
def finance():
    asset = CONTENT_BY_URL["/for-women-in-finance"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("finance.html", **page_payload(meta))


@bp.route("/for-client-facing-leaders")
def client_facing():
    asset = CONTENT_BY_URL["/for-client-facing-leaders"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("client_facing.html", **page_payload(meta))


@bp.route("/newsletter")
def newsletter():
    asset = CONTENT_BY_URL["/newsletter"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("newsletter.html", **page_payload(meta))


@bp.route("/consultation-request")
def consultation_request():
    asset = CONTENT_BY_URL["/consultation-request"]
    meta = PageMeta(asset.title, asset.content_theme, asset.message_framing, asset.funnel_stage_intent)
    return render_template("consultation.html", **page_payload(meta))


@bp.route("/articles/<slug>")
def article(slug):
    registry_asset = CONTENT_BY_SLUG.get(slug)
    article_data = ARTICLES.get(slug)
    if article_data is None or registry_asset is None:
        return redirect(url_for("main.home"))
    return render_template(
        "article.html",
        article=article_data,
        slug=slug,
        **page_payload(article_data["meta"]),
    )


@bp.post("/events")
def capture_event():
    payload = request.get_json(silent=True) or {}
    event_name = payload.get("event_name")
    if not event_name:
        return jsonify({"ok": False, "error": "missing_event_name"}), 400

    log_event(
        event_name,
        anonymous_id=payload.get("anonymous_id"),
        session_id=payload.get("session_id"),
        page_url=payload.get("page_url"),
        page_title=payload.get("page_title"),
        content_theme=payload.get("content_theme"),
        message_framing=payload.get("message_framing"),
        funnel_stage_intent=payload.get("funnel_stage_intent"),
        cta_label=payload.get("cta_label"),
        form_name=payload.get("form_name"),
        article_slug=payload.get("article_slug"),
        path_history=payload.get("path_history"),
        landing_page=payload.get("landing_page"),
        utm_source=payload.get("utm_source"),
        utm_medium=payload.get("utm_medium"),
        utm_campaign=payload.get("utm_campaign"),
        referrer=payload.get("referrer"),
        traffic_type=payload.get("traffic_type", "live"),
    )
    return jsonify({"ok": True}), 202


@bp.post("/newsletter-signup")
def submit_newsletter():
    form = request.form
    db = current_app.get_db()
    db.execute(
        """
        insert into newsletter_signups (
            email, job_title, industry, anonymous_id, session_id, landing_page,
            utm_source, utm_medium, utm_campaign, referrer, traffic_type
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            form.get("email"),
            form.get("job_title"),
            form.get("industry"),
            form.get("anonymous_id"),
            form.get("session_id"),
            form.get("landing_page"),
            form.get("utm_source"),
            form.get("utm_medium"),
            form.get("utm_campaign"),
            form.get("referrer"),
            form.get("traffic_type", "live"),
        ),
    )
    log_event("newsletter_submit", **event_payload_from_form(form))
    db.commit()
    flash("Newsletter signup captured.")
    return redirect(url_for("main.newsletter"))


@bp.post("/consultation-request")
def submit_consultation():
    form = request.form
    db = current_app.get_db()
    db.execute(
        """
        insert into consultation_leads (
            name, email, job_title, industry, company_size, primary_goal,
            urgent_challenge, anonymous_id, session_id, landing_page,
            content_path_summary, utm_source, utm_medium, utm_campaign, referrer,
            traffic_type
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            form.get("name"),
            form.get("email"),
            form.get("job_title"),
            form.get("industry"),
            form.get("company_size"),
            form.get("primary_goal"),
            form.get("urgent_challenge"),
            form.get("anonymous_id"),
            form.get("session_id"),
            form.get("landing_page"),
            form.get("content_path_summary"),
            form.get("utm_source"),
            form.get("utm_medium"),
            form.get("utm_campaign"),
            form.get("referrer"),
            form.get("traffic_type", "live"),
        ),
    )
    log_event("consultation_submit", **event_payload_from_form(form))
    db.commit()
    flash("Consultation request submitted.")
    return redirect(url_for("main.consultation_request"))
