drop view if exists path_performance;

create view path_performance as
select
    traffic_type,
    coalesce(path_history, '(no path recorded)') as path_history,
    count(*) as sessions,
    sum(case when article_views > 0 then 1 else 0 end) as sessions_with_article_view,
    sum(case when cta_clicks > 0 then 1 else 0 end) as sessions_with_cta_click,
    sum(case when became_newsletter_signup > 0 then 1 else 0 end) as sessions_with_newsletter_signup,
    sum(case when became_consultation_lead > 0 then 1 else 0 end) as sessions_with_consultation_lead,
    round(1.0 * sum(case when became_newsletter_signup > 0 then 1 else 0 end) / nullif(count(*), 0), 4) as newsletter_signup_rate,
    round(1.0 * sum(case when became_consultation_lead > 0 then 1 else 0 end) / nullif(count(*), 0), 4) as consultation_lead_rate
from session_facts
group by traffic_type, coalesce(path_history, '(no path recorded)')
order by traffic_type asc, sessions desc, consultation_lead_rate desc, newsletter_signup_rate desc;
