drop view if exists content_label_diagnostics;

create view content_label_diagnostics as
select
    ca.asset_id,
    ca.asset_type,
    ca.page_url,
    ca.title,
    ca.content_theme,
    ca.message_framing as manual_message_framing,
    cle.derived_message_framing,
    ca.audience_segment as manual_audience_segment,
    cle.derived_audience_segment,
    ca.cta_style as manual_cta_style,
    cle.derived_cta_style,
    cle.message_framing_confidence,
    cle.audience_confidence,
    cle.cta_style_confidence,
    cle.authority_score,
    cle.practical_score,
    cle.industry_specific_score,
    cle.conversion_score,
    cle.direct_conversion_score,
    cle.bridge_to_conversion_score,
    cle.nurture_capture_score,
    cle.high_intent_form_score,
    cle.women_in_finance_score,
    cle.client_facing_leaders_score,
    cle.promotion_readiness_score,
    cle.cross_audience_score,
    cle.framing_match_flag,
    cle.audience_match_flag,
    cle.cta_match_flag,
    coalesce(cp.traffic_type, 'synthetic') as traffic_type,
    coalesce(cp.sessions, 0) as sessions,
    coalesce(cp.sessions_with_cta_click, 0) as sessions_with_cta_click,
    coalesce(cp.sessions_with_newsletter_signup, 0) as newsletter_signups,
    coalesce(cp.sessions_with_consultation_lead, 0) as consultation_leads,
    coalesce(cp.consultation_lead_rate, 0.0) as consultation_lead_rate
from content_assets ca
left join content_label_enrichment cle
    on cle.asset_id = ca.asset_id
left join content_performance cp
    on cp.asset_id = ca.asset_id
   and cp.traffic_type = 'synthetic'
order by ca.asset_type, ca.page_url;
