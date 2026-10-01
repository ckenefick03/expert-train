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
  "as_of": "2026-10-01 setup",
  "account": { "name": "Agentic Account", "last4": "4490", "type": "limited_margin" },
  "risk": { "position_size": 80, "max_positions": 3, "daily_loss_limit": 100, "breaker_pct": 10, "min_trades": 1, "max_trades": 10 },
  "status": "amber",
  "status_note": "Setup baseline: 3 legacy positions held, no framework trades yet",
  "peak_equity": 421.51,
  "day": { "date": "2026-10-01", "start_equity": 421.51, "trades": 0, "forced": 0 },
  "equity_history": [
    { "t": "2026-10-01 setup", "equity": 421.51 }
  ],
  "positions": [
    { "symbol": "KTOS", "strategy": "legacy", "legacy": true, "qty": 4.890677, "entry": 42.53, "price": null, "stop": null, "target": null },
    { "symbol": "RKLB", "strategy": "legacy", "legacy": true, "qty": 1.49887, "entry": 70.72, "price": null, "stop": null, "target": null },
    { "symbol": "OKLO", "strategy": "legacy", "legacy": true, "qty": 2.914497, "entry": 36.37, "price": null, "stop": null, "target": null }
  ],
  "trades": [],
  "regime": { "read": "No cycle run yet.", "chips": [] }
}
```

`trades` row shape: `{"symbol":"", "strategy":"mean-reversion|momentum", "tier":"A|B|C|-", "entry":0, "exit":0, "pnl":0, "r":0, "score":0, "tag":"organic|forced", "closed":"YYYY-MM-DD HH:MM"}`.
`regime.chips` row shape: `{"name":"SPY", "chg":-0.4}` (percent change on the day).

## Baseline (setup, 2026-10-01)

- Account: Agentic Account (ending 4490), type limited_margin. Total value $421.51; cash / buying power $0.04.
- Pre-existing positions (legacy, not framework trades, unmanaged unless the user says otherwise): KTOS 4.890677 sh @ $42.53 avg, RKLB 1.49887 sh @ $70.72 avg, OKLO 2.914497 sh @ $36.37 avg (cost ≈ $208 / $106 / $106).
- Consequence: buying power is $0.04, so no $80 entry is possible until cash is available (deposit, or the user sells or releases legacy holdings).
- Risk parameters: $80 fixed size; 3 max positions; $100 daily loss limit; 10% circuit breaker from peak (peak $421.51, breaker at equity ≤ $379.36); min 1 / max 10 trades per day; no leverage/options/shorting/averaging down.

## Cycle log

_(no cycles run yet — append entries below)_
