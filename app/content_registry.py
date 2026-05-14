from dataclasses import dataclass


@dataclass(frozen=True)
class ContentAsset:
    asset_id: str
    asset_type: str
    page_url: str
    title: str
    content_theme: str
    message_framing: str
    funnel_stage_intent: str
    audience_segment: str
    primary_cta: str
    cta_style: str
    body_summary: str
    slug: str = ""


CONTENT_ASSETS = [
    ContentAsset(
        asset_id="page_home",
        asset_type="landing_page",
        page_url="/",
        title="Executive Presence Audit Lab",
        content_theme="general_hub",
        message_framing="authority",
        funnel_stage_intent="awareness",
        audience_segment="cross_audience",
        primary_cta="get_audit",
        cta_style="direct_conversion",
        body_summary="General hub introducing executive presence, leadership credibility, and advisory funnel pathways.",
    ),
    ContentAsset(
        asset_id="page_audit",
        asset_type="landing_page",
        page_url="/executive-presence-audit",
        title="Executive Presence Audit",
        content_theme="executive_presence",
        message_framing="authority",
        funnel_stage_intent="conversion",
        audience_segment="cross_audience",
        primary_cta="request_consultation",
        cta_style="direct_conversion",
        body_summary="Core conversion page positioning the audit as a structured review of authority, credibility, and leadership readiness.",
    ),
    ContentAsset(
        asset_id="page_finance",
        asset_type="landing_page",
        page_url="/for-women-in-finance",
        title="Executive Presence for Women in Finance",
        content_theme="women_in_finance",
        message_framing="industry_specific",
        funnel_stage_intent="consideration",
        audience_segment="women_in_finance",
        primary_cta="finance_to_audit",
        cta_style="direct_conversion",
        body_summary="Industry-specific page for finance professionals focused on visibility, authority, and promotion readiness.",
    ),
    ContentAsset(
        asset_id="page_client_facing",
        asset_type="landing_page",
        page_url="/for-client-facing-leaders",
        title="For Client-Facing Leaders",
        content_theme="client_facing_credibility",
        message_framing="practical",
        funnel_stage_intent="consideration",
        audience_segment="client_facing_leaders",
        primary_cta="client_facing_to_consultation",
        cta_style="direct_conversion",
        body_summary="Practical page for consultants, advisors, and sellers focused on visible credibility and trust-building.",
    ),
    ContentAsset(
        asset_id="page_newsletter",
        asset_type="conversion_page",
        page_url="/newsletter",
        title="Newsletter Signup",
        content_theme="newsletter_capture",
        message_framing="practical",
        funnel_stage_intent="consideration",
        audience_segment="cross_audience",
        primary_cta="join_newsletter",
        cta_style="nurture_capture",
        body_summary="Lower-commitment capture page for ongoing executive presence content and nurture sequencing.",
    ),
    ContentAsset(
        asset_id="page_consultation",
        asset_type="conversion_page",
        page_url="/consultation-request",
        title="Request a Consultation",
        content_theme="consultation",
        message_framing="conversion",
        funnel_stage_intent="conversion",
        audience_segment="cross_audience",
        primary_cta="submit_request",
        cta_style="high_intent_form",
        body_summary="Primary conversion page for qualified consultation demand and higher-intent inbound interest.",
    ),
    ContentAsset(
        asset_id="article_promotion_signals",
        asset_type="article",
        page_url="/articles/promotion-signals",
        title="How Executive Presence Shapes Promotion Signals",
        content_theme="executive_presence",
        message_framing="authority",
        funnel_stage_intent="awareness",
        audience_segment="promotion_readiness",
        primary_cta="article_to_next_step",
        cta_style="bridge_to_conversion",
        body_summary="Authority-framed article about executive presence as a promotion-readiness signal in visible leadership contexts.",
        slug="promotion-signals",
    ),
    ContentAsset(
        asset_id="article_visual_credibility",
        asset_type="article",
        page_url="/articles/visual-credibility",
        title="Why Client-Facing Professionals Need Visual Credibility",
        content_theme="client_facing_credibility",
        message_framing="practical",
        funnel_stage_intent="awareness",
        audience_segment="client_facing_leaders",
        primary_cta="article_to_next_step",
        cta_style="bridge_to_conversion",
        body_summary="Practical article connecting visible professional credibility to trust and influence in external-facing roles.",
        slug="visual-credibility",
    ),
    ContentAsset(
        asset_id="article_women_in_finance",
        asset_type="article",
        page_url="/articles/women-in-finance",
        title="What Women in Finance Often Get Wrong About Leadership Presence",
        content_theme="women_in_finance",
        message_framing="industry_specific",
        funnel_stage_intent="awareness",
        audience_segment="women_in_finance",
        primary_cta="article_to_next_step",
        cta_style="bridge_to_conversion",
        body_summary="Industry-specific article about authority signaling, leadership presence, and fit in finance environments.",
        slug="women-in-finance",
    ),
]


CONTENT_BY_URL = {asset.page_url: asset for asset in CONTENT_ASSETS}
CONTENT_BY_SLUG = {asset.slug: asset for asset in CONTENT_ASSETS if asset.slug}
