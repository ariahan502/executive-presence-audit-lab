drop view if exists content_label_comparison;

create view content_label_comparison as
select
    ca.asset_id,
    ca.asset_type,
    ca.page_url,
    ca.title,
    ca.content_theme,
    ca.message_framing as manual_message_framing,
    cle.derived_message_framing as text_derived_message_framing,
    clm.message_framing as model_assisted_message_framing,
    ca.audience_segment as manual_audience_segment,
    cle.derived_audience_segment as text_derived_audience_segment,
    clm.audience_segment as model_assisted_audience_segment,
    ca.cta_style as manual_cta_style,
    cle.derived_cta_style as text_derived_cta_style,
    clm.cta_style as model_assisted_cta_style,
    cle.message_framing_confidence,
    cle.audience_confidence,
    cle.cta_style_confidence,
    clm.model_provider,
    clm.model_name,
    clm.prompt_version,
    clm.notes as model_assisted_notes,
    case when ca.message_framing = cle.derived_message_framing then 1 else 0 end as manual_vs_text_framing_match,
    case when ca.message_framing = clm.message_framing then 1 else 0 end as manual_vs_model_framing_match,
    case when cle.derived_message_framing = clm.message_framing then 1 else 0 end as text_vs_model_framing_match,
    case when ca.audience_segment = cle.derived_audience_segment then 1 else 0 end as manual_vs_text_audience_match,
    case when ca.audience_segment = clm.audience_segment then 1 else 0 end as manual_vs_model_audience_match,
    case when cle.derived_audience_segment = clm.audience_segment then 1 else 0 end as text_vs_model_audience_match,
    case when ca.cta_style = cle.derived_cta_style then 1 else 0 end as manual_vs_text_cta_match,
    case when ca.cta_style = clm.cta_style then 1 else 0 end as manual_vs_model_cta_match,
    case when cle.derived_cta_style = clm.cta_style then 1 else 0 end as text_vs_model_cta_match,
    case
        when ca.message_framing = cle.derived_message_framing
         and ca.message_framing = clm.message_framing then 1
        else 0
    end as unanimous_framing_match,
    case
        when ca.audience_segment = cle.derived_audience_segment
         and ca.audience_segment = clm.audience_segment then 1
        else 0
    end as unanimous_audience_match,
    case
        when ca.cta_style = cle.derived_cta_style
         and ca.cta_style = clm.cta_style then 1
        else 0
    end as unanimous_cta_match,
    coalesce(cp.sessions, 0) as synthetic_sessions,
    coalesce(cp.consultation_lead_rate, 0.0) as synthetic_consultation_lead_rate
from content_assets ca
left join content_label_enrichment cle
    on cle.asset_id = ca.asset_id
left join content_label_model_assisted clm
    on clm.asset_id = ca.asset_id
left join content_performance cp
    on cp.asset_id = ca.asset_id
   and cp.traffic_type = 'synthetic'
order by ca.asset_type, ca.page_url;
