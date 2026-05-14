drop view if exists content_performance;

create view content_performance as
select
    sf.traffic_type,
    ca.asset_id,
    ca.asset_type,
    ca.page_url,
    ca.title,
    ca.content_theme,
    ca.message_framing,
    ca.audience_segment,
    ca.cta_style,
    count(*) as sessions,
    sum(case when sf.article_views > 0 then 1 else 0 end) as sessions_with_article_view,
    sum(case when sf.cta_clicks > 0 then 1 else 0 end) as sessions_with_cta_click,
    sum(case when sf.became_newsletter_signup > 0 then 1 else 0 end) as sessions_with_newsletter_signup,
    sum(case when sf.became_consultation_lead > 0 then 1 else 0 end) as sessions_with_consultation_lead,
    round(1.0 * sum(case when sf.cta_clicks > 0 then 1 else 0 end) / nullif(count(*), 0), 4) as cta_click_rate,
    round(1.0 * sum(case when sf.became_newsletter_signup > 0 then 1 else 0 end) / nullif(count(*), 0), 4) as newsletter_signup_rate,
    round(1.0 * sum(case when sf.became_consultation_lead > 0 then 1 else 0 end) / nullif(count(*), 0), 4) as consultation_lead_rate
from session_facts sf
join content_assets ca on ca.page_url = sf.landing_page
group by
    sf.traffic_type,
    ca.asset_id,
    ca.asset_type,
    ca.page_url,
    ca.title,
    ca.content_theme,
    ca.message_framing,
    ca.audience_segment,
    ca.cta_style;
