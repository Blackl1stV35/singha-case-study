# Exchange rates, Federal Reserve H.10 via FRED
- URLs: https://fred.stlouisfed.org/series/DEXTHUS (Thai baht per US dollar); https://fred.stlouisfed.org/series/DEXCHUS (Chinese yuan per US dollar)
- Date read: 2026-10-20 (WebFetch extraction; both series opened again on 2026-10-20 in the second pass)
- Source named: Board of Governors of the Federal Reserve System, release H.10
- Latest observation in each series: 2026-10-09. DEXTHUS 33.5500 (8 Oct 33.6900; 7 Oct 33.6600). DEXCHUS 6.6920 (8 Oct 6.7021; 7 Oct 6.7038).
- Tier: P (central bank series, republished by FRED)
- Used in the T9 re-price (revised): the 9 Oct observations, 33.5500 / 6.6920 = 5.0134 THB per CNY (the first version used 8 Oct, 5.0275, by oversight).
- Bank of Thailand: the BOT average counter rates for USD as of 15 Oct 2026 (sight buying 33.3535; transfer selling 33.7455; mid 33.5495) are saved in rework/raw/bot_fx_primary_2026-10-15.md and are used for USD. The BOT page gives USD only, so the CNY cross uses the Fed series. The Fed series is 11 days old at the read date.
