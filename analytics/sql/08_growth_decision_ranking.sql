drop view if exists growth_decision_ranking;

create view growth_decision_ranking as
with consultation_by_session as (
    select
        session_id,
        traffic_type,
        count(*) as consultation_leads,
        avg(lead_score) as avg_lead_score,
        sum(case when lead_tier = 'high' then 1 else 0 end) as high_tier_leads
    from lead_scoring
    group by session_id, traffic_type
),
rank_base as (
    select
        sf.traffic_type,
        coalesce(ca.content_theme, sf.first_content_theme, '(unknown)') as content_theme,
        coalesce(ca.message_framing, sf.first_message_framing, '(unknown)') as message_framing,
        coalesce(ca.audience_segment, '(unknown)') as audience_segment,
        coalesce(ca.cta_style, '(unknown)') as cta_style,
        count(*) as sessions,
        sum(case when sf.cta_clicks > 0 then 1 else 0 end) as sessions_with_cta_click,
        sum(case when sf.newsletter_signup_count > 0 then 1 else 0 end) as newsletter_sessions,
        sum(case when sf.consultation_lead_count > 0 then 1 else 0 end) as consultation_sessions,
        sum(coalesce(cbs.consultation_leads, 0)) as consultation_leads,
        sum(coalesce(cbs.high_tier_leads, 0)) as high_tier_leads,
        avg(case when cbs.consultation_leads > 0 then cbs.avg_lead_score end) as avg_lead_score
    from session_facts sf
    left join content_assets ca
        on ca.page_url = sf.landing_page
    left join consultation_by_session cbs
        on cbs.session_id = sf.session_id
       and cbs.traffic_type = sf.traffic_type
    group by
        sf.traffic_type,
        coalesce(ca.content_theme, sf.first_content_theme, '(unknown)'),
        coalesce(ca.message_framing, sf.first_message_framing, '(unknown)'),
        coalesce(ca.audience_segment, '(unknown)'),
        coalesce(ca.cta_style, '(unknown)')
    having count(*) >= 2
)
select
    traffic_type,
    content_theme,
    message_framing,
    audience_segment,
    cta_style,
    sessions,
    sessions_with_cta_click,
    newsletter_sessions,
    consultation_sessions,
    consultation_leads,
    high_tier_leads,
    round(1.0 * sessions_with_cta_click / sessions, 3) as cta_engagement_rate,
    round(1.0 * newsletter_sessions / sessions, 3) as newsletter_session_rate,
    round(1.0 * consultation_sessions / sessions, 3) as consultation_session_rate,
    round(1.0 * consultation_leads / sessions, 3) as consultation_lead_rate,
    round(1.0 * high_tier_leads / nullif(consultation_leads, 0), 3) as high_tier_share,
    round(coalesce(avg_lead_score, 0), 2) as avg_lead_score,
    round(
        (
            (1.0 * consultation_leads / sessions) * 50.0 +
            coalesce(avg_lead_score, 0) * 0.30 +
            (1.0 * sessions_with_cta_click / sessions) * 10.0 +
            (1.0 * newsletter_sessions / sessions) * 10.0
        ),
        2
    ) as decision_score,
    row_number() over (
        partition by traffic_type
        order by
            (
                (1.0 * consultation_leads / sessions) * 50.0 +
                coalesce(avg_lead_score, 0) * 0.30 +
                (1.0 * sessions_with_cta_click / sessions) * 10.0 +
                (1.0 * newsletter_sessions / sessions) * 10.0
            ) desc,
            sessions desc
    ) as segment_rank
from rank_base
order by traffic_type asc, segment_rank asc;
