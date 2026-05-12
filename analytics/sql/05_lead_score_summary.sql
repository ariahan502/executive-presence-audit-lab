drop view if exists lead_score_summary;

create view lead_score_summary as
select
    traffic_type,
    lead_tier,
    coalesce(first_content_theme, '(unknown)') as first_content_theme,
    coalesce(utm_source, '(direct)') as utm_source,
    count(*) as leads,
    round(avg(lead_score), 2) as avg_lead_score,
    min(lead_score) as min_lead_score,
    max(lead_score) as max_lead_score
from lead_scoring
group by
    traffic_type,
    lead_tier,
    coalesce(first_content_theme, '(unknown)'),
    coalesce(utm_source, '(direct)')
order by traffic_type asc, avg_lead_score desc, leads desc;
