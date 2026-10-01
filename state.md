# State — Agentic Account (ending 4490)

**Source of truth.** One shared state file for both strategies. Rules for every future cycle:

1. **Append** a new entry to the cycle log below every cycle. Never overwrite or delete history.
2. **Pull live data every cycle** (portfolio, positions, quotes). Do not trust a prior cycle's narrative; a position can close between cycles.
3. Update the `DASHBOARD_DATA` JSON block (this is the only part edited in place; keep `equity_history` and `trades` append-only), then run `python3 build_dashboard.py` to regenerate `dashboard.html`. Do not hand-edit the dashboard.

Cycle entry template (copy for each cycle):

```
### Cycle YYYY-MM-DD HH:MM ET
- Stop check: <per position: price vs stop, cushion, action>
- Reconciliation: equity $X, buying power $X, positions match broker? Y/N
- Market/sector read (tape first, news second): <indices/sectors, one-line regime>
- Scan — mean-reversion: <universe size scanned, candidates, gate verdicts>
- Scan — momentum: <universe size scanned, candidates, gate verdicts>
- Skips logged: <ticker, time, failed criterion, price; follow-ups later>
- Decisions: <entries (thesis/stop/target/horizon/tag) / exits (P&L $, R, score, note)>
- Daily stats: trades today N (organic n / forced n), realized $X, unrealized $X, loss-limit headroom $X
```

## DASHBOARD_DATA

Edit values in place. `status`: `green` = flat/healthy, `amber` = position(s) open and watched, `red` = stop recently hit or circuit breaker tripped. Trade rows go in `trades` (newest last); positions needing no stop (legacy) are marked `"legacy": true`.

```json
{
  "as_of": "2026-10-01 12:35 ET (cycle 1)",
  "account": { "name": "Agentic Account", "last4": "4490", "type": "limited_margin" },
  "risk": { "position_size": 80, "max_positions": 3, "daily_loss_limit": 100, "breaker_pct": 10, "min_trades": 1, "max_trades": 10 },
  "status": "amber",
  "status_note": "3 adopted positions watched; stops clear; no buying power for new entries",
  "peak_equity": 421.51,
  "day": { "date": "2026-10-01", "start_equity": 421.51, "trades": 0, "forced": 0 },
  "equity_history": [
    { "t": "2026-10-01 setup", "equity": 421.51 },
    { "t": "2026-10-01 12:35 ET", "equity": 421.18 }
  ],
  "positions": [
    { "symbol": "KTOS", "strategy": "adopted", "qty": 4.890677, "entry": 42.53, "price": 42.89, "stop": 40.20, "target": 47.15 },
    { "symbol": "RKLB", "strategy": "adopted", "qty": 1.49887, "entry": 70.72, "price": 70.49, "stop": 66.80, "target": 78.55 },
    { "symbol": "OKLO", "strategy": "adopted", "qty": 2.914497, "entry": 36.37, "price": 36.27, "stop": 34.05, "target": 41.00 }
  ],
  "trades": [],
  "regime": {
    "read": "Mixed, mildly risk-off tape: SPY/QQQ slightly red, energy and small caps firm, healthcare and uranium weak. No broad dislocation; weakness is clustered in miners, UK/Japan banks and packaged food.",
    "chips": [
      { "name": "SPY", "chg": -0.16 }, { "name": "QQQ", "chg": -0.19 }, { "name": "IWM", "chg": 0.23 },
      { "name": "XLK", "chg": 0.37 }, { "name": "XLE", "chg": 1.50 }, { "name": "XLF", "chg": -0.37 },
      { "name": "XLV", "chg": -1.09 }, { "name": "XLU", "chg": 0.27 }, { "name": "ITA", "chg": 0.18 },
      { "name": "UFO", "chg": -0.27 }, { "name": "URA", "chg": -1.71 }
    ]
  }
}
```

`trades` row shape: `{"symbol":"", "strategy":"mean-reversion|momentum", "tier":"A|B|C|-", "entry":0, "exit":0, "pnl":0, "r":0, "score":0, "tag":"organic|forced", "closed":"YYYY-MM-DD HH:MM"}`.
`regime.chips` row shape: `{"name":"SPY", "chg":-0.4}` (percent change on the day).

## Baseline (setup, 2026-10-01)

- Account: Agentic Account (ending 4490), type limited_margin. Total value $421.51; cash / buying power $0.04.
- Pre-existing positions (legacy, not framework trades, unmanaged unless the user says otherwise): KTOS 4.890677 sh @ $42.53 avg, RKLB 1.49887 sh @ $70.72 avg, OKLO 2.914497 sh @ $36.37 avg (cost ≈ $208 / $106 / $106).
- Consequence: buying power is $0.04, so no $80 entry is possible until cash is available.
- **Update 2026-10-01 (user decision): the user told me to adopt these three positions into the strategy.** They are now framework positions ("adopted") and count toward the 3-slot cap. Order history shows they were bought earlier today (11:18-11:40 ET by an agent, before this framework) with sizes above $80 (KTOS about $210, RKLB and OKLO about $106 each), and a WULF position was sold at 11:39 ET. These are pre-framework trades, not scored or tagged, and not counted toward today's minimum.
- Risk parameters: $80 fixed size; 3 max positions; $100 daily loss limit; 10% circuit breaker from peak (peak $421.51, breaker at equity ≤ $379.36); min 1 / max 10 trades per day; no leverage/options/shorting/averaging down.

## Cycle log

### Cycle 2026-10-01 12:35 ET (cycle 1)
- **Stop check (first):** all clear. Stops are 1 daily ATR below the average cost, because the 4% default sits inside one day's ATR (KTOS 5.4%, RKLB 5.6%, OKLO 6.4%) and would churn. Targets are 2R.

  | Pos | Qty | Avg cost | Price | Stop | Cushion | Target | 1R at risk |
  |---|---|---|---|---|---|---|---|
  | KTOS | 4.890677 | 42.53 | 42.89 | 40.20 | 6.3% | 47.15 | $11.4 |
  | RKLB | 1.49887 | 70.72 | 70.49 | 66.80 | 5.2% | 78.55 | $5.9 |
  | OKLO | 2.914497 | 36.37 | 36.27 | 34.05 | 6.1% | 41.00 | $6.7 |

  Max horizon is 3 sessions. Adopted-trade thesis is inherited and not independently gate-checked, so any score on these will be capped on setup quality. Total stop risk is about $24 (5.7% of equity).
- **Reconciliation:** equity $421.18, cash and buying power $0.04, 3 positions match the broker, no open orders. Peak is $421.51 and the breaker is at $379.36 (not close). Daily loss is about -$0.33 against a $100 limit.
- **Market/sector read (tape first):** SPY -0.16%, QQQ -0.19%, IWM +0.23%. Sectors: XLE +1.50%, XLK +0.37%, XLU +0.27%, XLF -0.37%, XLV -1.09%. Themes: ITA +0.18%, UFO -0.27%, URA -1.71%. Read: no broad dislocation, mild rotation into energy and out of healthcare and nuclear/uranium. Relative strength vs sector: RKLB +1.2% vs UFO -0.3% (strong), KTOS +0.5% vs ITA +0.2% (in line), OKLO -2.0% vs URA -1.7% (in line with its group, no relative-strength-loss exit).
- **Scan, mean-reversion (full universe: stocks, cap ≥ $2B, 30-day avg volume ≥ 1M, down ≥ 2.5%):** 102 names. Window is Tier B (11:30-14:30). Tape-side clusters that look sector/macro-driven (the only plausible gate-1 passes): crypto miners (RIOT -6.7%, CLSK -5.8%, CIFR -5.5%, HUT -4.0%, MARA -3.5%), UK/Japan banks (NWG -5.0%, LYG -4.4%, HSBC -4.0%, ING -4.1%, MFG -4.1%, BCS -3.6%), packaged food (GIS, CAG, CPB, MKC, SJM, KHC each -2.5% to -3.2%), casinos (LVS -3.1%, WYNN -2.9%). Likely company-specific and an automatic gate-1 FAIL: NKTR -20.9%, LQDA -13.5%, GRND -8.8%, CARG -6.8%, APP -5.1%, TEM -5.0%. **Data anomaly:** CTVA shows -84% on a $12.11 price, which looks like a corporate-action artifact (spin-off), so it was excluded and logged in §6. **Verdict: no entry. Buying power is $0.04, so the $80 minimum is unmet.** Clusters were not taken through the full 4-point gate; they are logged as follow-ups below.
- **Scan, momentum (stocks, cap ≥ $2B, 30-day avg volume ≥ 1M, up ≥ 3%, relative volume ≥ 1.3):** 4 names: ACN +18.6%, COHR +11.0%, WIT +6.7%, INFY +5.9%. ACN/WIT/INFY are one IT-services group moving together, which fails gate 1 (no standout from peers). COHR has no confirmed catalyst yet and it's 12:30, so no held-pullback base. **Verdict: no entry; none pass.**
- **Skips logged (follow-ups to fill next cycle):** RIOT, CLSK, CIFR, HUT, MARA, NWG, HSBC, GIS, CAG, LVS (mean-reversion candidates, price noted at 12:30); ACN, COHR (momentum). Follow-up: price at close and next-day vs 12:30, to check whether a gate-1 pass would have worked.
- **Decisions:** no entries or exits. No forced trade possible today (no buying power). Today's minimum of 1 trade is **unmet** and it can't be met honestly.
- **Overnight:** all three positions are still open and will roll overnight, since closing them today could count as a same-day round trip (day-trade rule unverified) and no stop or target has been hit. Adopted sizes exceed $80. Planned at tomorrow's open+30min: trim KTOS to about $80, RKLB and OKLO to about $80 each (restores the size rule and frees about $180 of buying power), unless a stop or target is hit first.
- **Daily stats:** framework trades today 0 (organic 0 / forced 0), realized $0, unrealized about +$1.1 on cost, loss-limit headroom about $100.
