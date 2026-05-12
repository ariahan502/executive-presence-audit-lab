# Event Schema v1

## Planned Events

- `page_view`
- `article_view`
- `cta_click`
- `newsletter_form_start`
- `newsletter_submit`
- `consultation_form_start`
- `consultation_submit`

## Shared Fields

- `event_time`
- `event_name`
- `anonymous_id`
- `session_id`
- `page_url`
- `page_title`
- `content_theme`
- `message_framing`
- `funnel_stage_intent`
- `cta_label`
- `form_name`
- `article_slug`
- `path_history`
- `landing_page`
- `utm_source`
- `utm_medium`
- `utm_campaign`
- `referrer`

## Notes

The current implementation stores raw browser events in the `raw_events` table through the `/events` endpoint and logs submit events server-side during form POST handling.

Browser-captured events:
- `page_view`
- `article_view`
- `cta_click`
- `newsletter_form_start`
- `consultation_form_start`

Server-captured submit events:
- `newsletter_submit`
- `consultation_submit`
