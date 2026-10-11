# Privacy

You can read and navigate the handbook without allowing analytics. Optional analytics is currently disabled in this source edition; enabling it requires separately verified public Google settings.

## What delivers the pages?

Vercel hosts and delivers this static website. Page delivery necessarily involves network information such as your IP address and browser requests, independently of the optional analytics choice. Hosting and delivery logs are distinct from Google Analytics.

## What happens if you allow analytics?

When configured, Google Tag Manager loads the handbook's analytics container only after your explicit allowance, on the exact production hostname. Google Analytics measures handbook reading through that container. There is no separate analytics loader, advertising tag or tracking iframe in this site. Global Privacy Control overrides an allowance, and analytics does not load on preview sites or localhost.

Analytics may use pseudonymous cookie identifiers and browser, device and network information. Pseudonymous is not anonymous: these identifiers may distinguish a browser over time. We do not send form values or application user IDs. Before the container loads, the site supplies the production origin and page path without query strings or fragments, and only the referring site's origin, not its path, query or fragment. The Google tag must separately be configured to use those sanitized values before its first pageview; local seeding alone does not prove what Google receives.

## How is your choice saved?

Your allow or decline choice and its decision time are stored in this browser's local storage for 180 days, approximately six months. Invalid, expired or future-dated choices are treated as undecided. If storage is unavailable, your choice applies only to the current page; a reload requires a fresh allowance. Without JavaScript, optional analytics does not load and the handbook remains readable.

## How do you withdraw?

Open Analytics preferences in the footer and choose Decline analytics. The site saves a decline when storage permits, removes accessible first-party analytics cookies, and reloads if a container was already loaded so it is unloaded. Browser restrictions, cookie paths, domains and inaccessible cookies can limit deletion. If storage is blocked, withdrawal cannot be remembered across reloads, but the next load starts without an allowance. You can also clear site data in your browser.

Withdrawal stops future collection by this site; it cannot retract requests already sent. Deleting cookies does not erase existing aggregated reports.

## What retention and advertising settings are planned?

The intended Google Analytics settings are two-month user/event retention and 180-day analytics cookie expiry. These are planned settings requiring separate account and published-container verification, not claims that they are already active. Enhanced measurement, advertising features and Google Signals must remain disabled. This source change neither configures those accounts nor verifies received pageviews.

## Questions and limits

The handbook is maintained by Desmond Landry. You can raise a privacy question through the [handbook repository](https://github.com/desland01/agent-engineering-handbook). This notice describes the implementation and its limits; it is not a legal certification or a claim that every privacy obligation has been assessed.
