drop view if exists lead_intent_features;

create view lead_intent_features as
select
    sf.session_id,
    sf.anonymous_id,
    sf.traffic_type,
    sf.landing_page,
    sf.first_content_theme,
    sf.first_message_framing,
    sf.first_utm_source,
    sf.first_utm_medium,
    sf.first_utm_campaign,
    ca.audience_segment,
    ca.cta_style,
    sf.total_events,
    sf.page_views,
    sf.article_views,
    sf.cta_clicks,
    sf.newsletter_form_starts,
    sf.newsletter_submits,
    sf.consultation_form_starts,
    sf.consultation_submits,
    sf.newsletter_signup_count,
    sf.consultation_lead_count,
    length(coalesce(sf.path_history, '')) as path_history_length,
    (
        length(coalesce(sf.path_history, '')) - length(replace(coalesce(sf.path_history, ''), '>', ''))
    ) + case when coalesce(sf.path_history, '') = '' then 0 else 1 end as path_step_count,
    case when sf.article_views > 0 then 1 else 0 end as used_article_content,
    case when sf.cta_clicks > 0 then 1 else 0 end as clicked_cta,
    case when sf.consultation_form_starts > 0 then 1 else 0 end as started_high_intent_form,
    case when sf.became_consultation_lead > 0 then 1 else 0 end as target_consultation_lead
from session_facts sf
left join content_assets ca on ca.page_url = sf.landing_page;
