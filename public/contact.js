const enquiryForm = document.getElementById('enquiry');
document.querySelectorAll('[data-enquiry]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    enquiryForm.showModal();
  });
});
document.getElementById('close-enquiry').onclick = () => enquiryForm.close();


// Google Analytics and Google Ads (WhatsApp click measurement). Nothing from Google loads until the visitor
// accepts; declining keeps everything off. The page <head> sets every consent type to denied first.
(() => {
  const adsId = 'AW-18545533050';
  const containerId = 'GTM-T49KV83L'; // Google Analytics 4 is set up in this container
  const conversionId = 'AW-18545533050/ATUyCJnQ7LgdEPrAmYtF';
  const consentKey = 'hd-events-ads-consent';
  let choice = null;
  try { choice = localStorage.getItem(consentKey); } catch (_) {}

  const setConsent = allowed => {
    choice = allowed ? 'granted' : 'denied';
    try { localStorage.setItem(consentKey, choice); } catch (_) {}
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        ad_storage: choice, ad_user_data: choice, ad_personalization: choice,
        analytics_storage: choice
      });
    }
    if (allowed) loadTag();
    document.getElementById('hd-ads-consent')?.remove();
  };
  let loaded = false;
  const loadTag = () => {
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      ad_storage: 'denied', ad_user_data: 'denied',
      ad_personalization: 'denied', analytics_storage: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('config', adsId);
    window.gtag('consent', 'update', {
      ad_storage: 'granted', ad_user_data: 'granted',
      ad_personalization: 'granted', analytics_storage: 'granted'
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(adsId);
    document.head.appendChild(script);
    window.dataLayer.push({'gtm.start': Date.now(), event: 'gtm.js'});
    const gtm = document.createElement('script');
    gtm.async = true;
    gtm.src = 'https://www.googletagmanager.com/gtm.js?id=' + containerId;
    document.head.appendChild(gtm);
  };
  if (choice === 'granted') loadTag();

  // Measure all WhatsApp links, including the floating button and mobile links.
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link || !/^https:\/\/(?:wa\.me|api\.whatsapp\.com)\//i.test(link.href)) return;
    if (choice !== 'granted' || typeof window.gtag !== 'function') return;
    window.gtag('event', 'conversion', { send_to: conversionId });
  }, true);

  if (choice !== 'granted' && choice !== 'denied') {
    const notice = document.createElement('div');
    notice.id = 'hd-ads-consent';
    notice.setAttribute('role', 'region');
    notice.setAttribute('aria-label', 'Cookies');
    notice.style.cssText = 'position:fixed;bottom:12px;left:12px;right:12px;z-index:99999;background:#17212a;color:white;padding:16px;border:1px solid #82909d;border-radius:10px;max-width:470px;box-shadow:0 3px 18px #0006;font:14px/1.5 Arial,sans-serif';
    notice.innerHTML = '<p style="margin:0 0 10px">Can we use analytics and advertising cookies to see how people use our website and measure enquiries? You can decline and still use the site.</p><button type="button" data-consent="deny" style="padding:8px 12px;margin-right:8px;cursor:pointer">Decline</button><button type="button" data-consent="accept" style="padding:8px 12px;cursor:pointer">Accept</button>';
    notice.addEventListener('click', event => {
      const button = event.target.closest('[data-consent]');
      if (button) setConsent(button.dataset.consent === 'accept');
    });
    document.body.appendChild(notice);
  }
  // Visitors can reopen cookie consent and withdraw it at any time.
  const footer = document.querySelector('footer');
  if (footer) {
    const settings = document.createElement('button');
    settings.type = 'button';
    settings.textContent = 'Cookie settings';
    settings.setAttribute('aria-label', 'Change cookie preferences');
    settings.style.cssText = 'background:transparent;color:inherit;border:1px solid currentColor;border-radius:5px;padding:6px 10px;margin:10px 0;cursor:pointer;font:inherit';
    settings.addEventListener('click', () => {
      try { localStorage.removeItem(consentKey); } catch (_) {}
      window.location.reload();
    });
    footer.appendChild(settings);
  }
})();
