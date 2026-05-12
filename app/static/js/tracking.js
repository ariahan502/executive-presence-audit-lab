(function () {
  const body = document.body;
  const trackingEndpoint = body.dataset.trackingEndpoint;
  const trafficType = "live";
  const storageKeys = {
    anonymousId: "epal_anonymous_id",
    sessionId: "epal_session_id",
    sessionStartedAt: "epal_session_started_at",
    pathHistory: "epal_path_history",
    utmSource: "epal_utm_source",
    utmMedium: "epal_utm_medium",
    utmCampaign: "epal_utm_campaign",
    referrer: "epal_referrer",
  };

  function randomId(prefix) {
    return prefix + "_" + Math.random().toString(36).slice(2, 10);
  }

  function getOrCreateAnonymousId() {
    let value = localStorage.getItem(storageKeys.anonymousId);
    if (!value) {
      value = randomId("anon");
      localStorage.setItem(storageKeys.anonymousId, value);
    }
    return value;
  }

  function getOrCreateSessionId() {
    const existing = sessionStorage.getItem(storageKeys.sessionId);
    if (existing) {
      return existing;
    }
    const value = randomId("sess");
    sessionStorage.setItem(storageKeys.sessionId, value);
    sessionStorage.setItem(storageKeys.sessionStartedAt, new Date().toISOString());
    return value;
  }

  function persistAcquisition() {
    const params = new URLSearchParams(window.location.search);
    const acquisitionMap = {
      utm_source: storageKeys.utmSource,
      utm_medium: storageKeys.utmMedium,
      utm_campaign: storageKeys.utmCampaign,
    };

    Object.entries(acquisitionMap).forEach(([paramKey, storageKey]) => {
      const value = params.get(paramKey);
      if (value) {
        localStorage.setItem(storageKey, value);
      }
    });
    if (document.referrer) {
      localStorage.setItem(storageKeys.referrer, document.referrer);
    }
  }

  function rememberPath() {
    const path = window.location.pathname;
    const current = JSON.parse(sessionStorage.getItem(storageKeys.pathHistory) || "[]");
    if (current[current.length - 1] !== path) {
      current.push(path);
      sessionStorage.setItem(storageKeys.pathHistory, JSON.stringify(current.slice(-8)));
    }
  }

  function fillHiddenInputs() {
    const anonymousId = getOrCreateAnonymousId();
    const sessionId = getOrCreateSessionId();
    const pathHistory = JSON.parse(sessionStorage.getItem(storageKeys.pathHistory) || "[]");
    const pathSummary = pathHistory.join(" > ");

    document.querySelectorAll("input[name='anonymous_id']").forEach((el) => {
      el.value = anonymousId;
    });
    document.querySelectorAll("input[name='session_id']").forEach((el) => {
      el.value = sessionId;
    });
    document.querySelectorAll("input[name='content_path_summary']").forEach((el) => {
      el.value = pathSummary;
    });
    document.querySelectorAll("input[name='traffic_type']").forEach((el) => {
      el.value = trafficType;
    });

    const utmSource = localStorage.getItem(storageKeys.utmSource) || "";
    const utmMedium = localStorage.getItem(storageKeys.utmMedium) || "";
    const utmCampaign = localStorage.getItem(storageKeys.utmCampaign) || "";
    const referrer = localStorage.getItem(storageKeys.referrer) || document.referrer || "";

    document.querySelectorAll("input[name='utm_source']").forEach((el) => {
      el.value = utmSource;
    });
    document.querySelectorAll("input[name='utm_medium']").forEach((el) => {
      el.value = utmMedium;
    });
    document.querySelectorAll("input[name='utm_campaign']").forEach((el) => {
      el.value = utmCampaign;
    });
    document.querySelectorAll("input[name='referrer']").forEach((el) => {
      el.value = referrer;
    });
  }

  function buildEventPayload(overrides) {
    const pathHistory = JSON.parse(sessionStorage.getItem(storageKeys.pathHistory) || "[]");
    return {
      anonymous_id: getOrCreateAnonymousId(),
      session_id: getOrCreateSessionId(),
      page_url: window.location.pathname,
      page_title: body.dataset.pageTitle || document.title,
      content_theme: body.dataset.contentTheme || "",
      message_framing: body.dataset.messageFraming || "",
      funnel_stage_intent: body.dataset.funnelStageIntent || "",
      article_slug: window.location.pathname.startsWith("/articles/")
        ? window.location.pathname.split("/").pop()
        : "",
      path_history: pathHistory.join(" > "),
      landing_page: pathHistory[0] || window.location.pathname,
      utm_source: localStorage.getItem(storageKeys.utmSource) || "",
      utm_medium: localStorage.getItem(storageKeys.utmMedium) || "",
      utm_campaign: localStorage.getItem(storageKeys.utmCampaign) || "",
      referrer: localStorage.getItem(storageKeys.referrer) || document.referrer || "",
      traffic_type: trafficType,
      ...overrides,
    };
  }

  function sendEvent(payload) {
    if (!trackingEndpoint) {
      return Promise.resolve();
    }
    return fetch(trackingEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      keepalive: true,
    }).catch(function () {
      return null;
    });
  }

  function trackPageView() {
    const isArticle = window.location.pathname.startsWith("/articles/");
    sendEvent(buildEventPayload({ event_name: isArticle ? "article_view" : "page_view" }));
  }

  function attachCtaTracking() {
    document.querySelectorAll("[data-event-name='cta_click']").forEach((el) => {
      el.addEventListener("click", function () {
        sendEvent(
          buildEventPayload({
            event_name: "cta_click",
            cta_label: el.dataset.ctaLabel || "",
          })
        );
      });
    });
  }

  function attachFormTracking() {
    document.querySelectorAll(".track-form").forEach((form) => {
      let started = false;
      form.addEventListener("focusin", function () {
        if (started) {
          return;
        }
        started = true;
        form.dataset.formStarted = "true";
        sendEvent(
          buildEventPayload({
            event_name: form.dataset.formName === "consultation"
              ? "consultation_form_start"
              : "newsletter_form_start",
            form_name: form.dataset.formName || "",
          })
        );
      });
    });
  }

  persistAcquisition();
  getOrCreateAnonymousId();
  getOrCreateSessionId();
  rememberPath();
  fillHiddenInputs();
  trackPageView();
  attachCtaTracking();
  attachFormTracking();
})();
