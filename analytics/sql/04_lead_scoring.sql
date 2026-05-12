drop view if exists lead_scoring;

create view lead_scoring as
with consultation_enriched as (
    select
        cl.lead_id,
        cl.submitted_at,
        cl.name,
        cl.email,
        cl.job_title,
        cl.industry,
        cl.company_size,
        cl.primary_goal,
        cl.urgent_challenge,
        cl.anonymous_id,
        cl.session_id,
        cl.landing_page,
        cl.content_path_summary,
        cl.utm_source,
        cl.utm_medium,
        cl.utm_campaign,
        cl.referrer,
        coalesce(cl.traffic_type, 'live') as traffic_type,
        sf.page_views,
        sf.article_views,
        sf.cta_clicks,
        sf.first_content_theme,
        sf.first_message_framing,
        sf.first_utm_source,
        sf.path_history
    from consultation_leads cl
    left join session_facts sf on sf.session_id = cl.session_id
),
scored as (
    select
        *,
        case
            when lower(coalesce(industry, '')) like '%finance%' then 20
            when lower(coalesce(industry, '')) like '%consult%' then 15
            when lower(coalesce(industry, '')) like '%advis%' then 15
            when lower(coalesce(industry, '')) like '%tech%' then 10
            else 0
        end as industry_score,
        case
            when company_size = '1000+' then 15
            when company_size = '201-1000' then 12
            when company_size = '51-200' then 8
            when company_size = '1-50' then 5
            else 0
        end as company_size_score,
        case
            when lower(coalesce(job_title, '')) like '%director%' then 12
            when lower(coalesce(job_title, '')) like '%head%' then 12
            when lower(coalesce(job_title, '')) like '%vp%' then 12
            when lower(coalesce(job_title, '')) like '%vice president%' then 12
            when lower(coalesce(job_title, '')) like '%manager%' then 8
            when lower(coalesce(job_title, '')) like '%lead%' then 8
            when lower(coalesce(job_title, '')) like '%founder%' then 10
            else 4
        end as seniority_score,
        case
            when lower(coalesce(primary_goal, '')) like '%promotion%' then 15
            when lower(coalesce(primary_goal, '')) like '%executive%' then 15
            when lower(coalesce(primary_goal, '')) like '%leadership%' then 15
            when lower(coalesce(primary_goal, '')) like '%credib%' then 12
            when lower(coalesce(primary_goal, '')) like '%client%' then 12
            when trim(coalesce(primary_goal, '')) <> '' then 8
            else 0
        end as goal_score,
        case
            when length(trim(coalesce(urgent_challenge, ''))) >= 80 then 15
            when length(trim(coalesce(urgent_challenge, ''))) >= 20 then 10
            when length(trim(coalesce(urgent_challenge, ''))) > 0 then 5
            else 0
        end as urgency_score,
        case
            when coalesce(article_views, 0) > 0 and coalesce(cta_clicks, 0) > 0 then 10
            when coalesce(cta_clicks, 0) > 0 then 8
            when coalesce(page_views, 0) > 1 then 5
            else 0
        end as engagement_score,
        case
            when coalesce(content_path_summary, '') like '%/for-women-in-finance%' then 8
            when coalesce(content_path_summary, '') like '%/for-client-facing-leaders%' then 8
            when coalesce(first_content_theme, '') in ('women_in_finance', 'client_facing_credibility') then 6
            else 0
        end as audience_fit_score,
        case
            when trim(coalesce(utm_source, '')) <> '' then 5
            else 0
        end as acquisition_score
    from consultation_enriched
)
select
    lead_id,
    submitted_at,
    name,
    email,
    job_title,
    industry,
    company_size,
    primary_goal,
    urgent_challenge,
    anonymous_id,
    session_id,
    landing_page,
    content_path_summary,
    utm_source,
    utm_medium,
    utm_campaign,
    referrer,
    traffic_type,
    page_views,
    article_views,
    cta_clicks,
    first_content_theme,
    first_message_framing,
    path_history,
    industry_score,
    company_size_score,
    seniority_score,
    goal_score,
    urgency_score,
    engagement_score,
    audience_fit_score,
    acquisition_score,
    min(
        industry_score + company_size_score + seniority_score + goal_score +
        urgency_score + engagement_score + audience_fit_score + acquisition_score,
        100
    ) as lead_score,
    case
        when (
            industry_score + company_size_score + seniority_score + goal_score +
            urgency_score + engagement_score + audience_fit_score + acquisition_score
        ) >= 70 then 'high'
        when (
            industry_score + company_size_score + seniority_score + goal_score +
            urgency_score + engagement_score + audience_fit_score + acquisition_score
        ) >= 45 then 'medium'
        else 'low'
    end as lead_tier
from scored;
