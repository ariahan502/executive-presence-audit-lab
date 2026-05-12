drop view if exists session_facts;

create view session_facts as
with event_sessions as (
    select
        session_id,
        min(event_time) as session_started_at,
        max(event_time) as session_ended_at,
        count(*) as total_events,
        sum(case when event_name = 'page_view' then 1 else 0 end) as page_views,
        sum(case when event_name = 'article_view' then 1 else 0 end) as article_views,
        sum(case when event_name = 'cta_click' then 1 else 0 end) as cta_clicks,
        sum(case when event_name = 'newsletter_form_start' then 1 else 0 end) as newsletter_form_starts,
        sum(case when event_name = 'newsletter_submit' then 1 else 0 end) as newsletter_submits,
        sum(case when event_name = 'consultation_form_start' then 1 else 0 end) as consultation_form_starts,
        sum(case when event_name = 'consultation_submit' then 1 else 0 end) as consultation_submits
    from raw_events
    where session_id is not null
      and trim(session_id) <> ''
    group by session_id
),
session_dimensions as (
    select
        es.session_id,
        (
            select re.anonymous_id
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as anonymous_id,
        (
            select re.traffic_type
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as traffic_type,
        (
            select re.landing_page
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as landing_page,
        (
            select re.page_url
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time desc, re.event_id desc
            limit 1
        ) as last_page_url,
        (
            select re.content_theme
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_content_theme,
        (
            select re.message_framing
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_message_framing,
        (
            select re.funnel_stage_intent
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_funnel_stage_intent,
        (
            select re.utm_source
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_utm_source,
        (
            select re.utm_medium
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_utm_medium,
        (
            select re.utm_campaign
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_utm_campaign,
        (
            select re.referrer
            from raw_events re
            where re.session_id = es.session_id
            order by re.event_time asc, re.event_id asc
            limit 1
        ) as first_referrer,
        (
            select re.path_history
            from raw_events re
            where re.session_id = es.session_id
              and coalesce(re.path_history, '') <> ''
            order by re.event_time desc, re.event_id desc
            limit 1
        ) as path_history
    from event_sessions es
),
newsletter_by_session as (
    select
        session_id,
        count(*) as newsletter_signup_count
    from newsletter_signups
    where session_id is not null
      and trim(session_id) <> ''
    group by session_id
),
consultation_by_session as (
    select
        session_id,
        count(*) as consultation_lead_count
    from consultation_leads
    where session_id is not null
      and trim(session_id) <> ''
    group by session_id
)
select
    es.session_id,
    sd.anonymous_id,
    coalesce(sd.traffic_type, 'live') as traffic_type,
    es.session_started_at,
    es.session_ended_at,
    sd.landing_page,
    sd.last_page_url,
    sd.first_content_theme,
    sd.first_message_framing,
    sd.first_funnel_stage_intent,
    sd.first_utm_source,
    sd.first_utm_medium,
    sd.first_utm_campaign,
    sd.first_referrer,
    sd.path_history,
    es.total_events,
    es.page_views,
    es.article_views,
    es.cta_clicks,
    es.newsletter_form_starts,
    es.newsletter_submits,
    es.consultation_form_starts,
    es.consultation_submits,
    coalesce(nbs.newsletter_signup_count, 0) as newsletter_signup_count,
    coalesce(cbs.consultation_lead_count, 0) as consultation_lead_count,
    case when es.newsletter_submits > 0 or coalesce(nbs.newsletter_signup_count, 0) > 0 then 1 else 0 end as became_newsletter_signup,
    case when es.consultation_submits > 0 or coalesce(cbs.consultation_lead_count, 0) > 0 then 1 else 0 end as became_consultation_lead
from event_sessions es
left join session_dimensions sd on sd.session_id = es.session_id
left join newsletter_by_session nbs on nbs.session_id = es.session_id
left join consultation_by_session cbs on cbs.session_id = es.session_id;
