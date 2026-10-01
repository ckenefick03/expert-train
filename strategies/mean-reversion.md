# Strategy: Mean-Reversion (sector/macro-driven oversold)

Account scope: Agentic Account (ending 4490) only. Runs in parallel with `momentum.md` every cycle; the full eligible universe is re-scanned each time. Risk numbers come from `framework.md` §3 ($80 fixed size, shared cap of 3 positions).

## Universe
- US-listed common stocks, market cap ≥ $2B.
- Liquidity: average daily volume ≥ 1M shares and ≥ $20M dollar volume; bid-ask spread ≤ 0.3% of price.
- Tradable fractionally on the broker (check `get_equity_tradability`).
- Not in an earnings window (no report within 2 trading days before entry).
- Sector or theme: any, but the drop must be tied to a sector or macro move.

## Gate-check (required in writing before ANY entry, at ANY tier)
One FAIL means no trade, regardless of how good anything else looks.

1. **Cause of the drop.** Must be external (sector rotation, macro, index flow). Company-specific causes (earnings miss, guidance cut, downgrade, legal issue) = automatic FAIL.
2. **Most recent fundamental datapoint.** Must be neutral-or-better. A miss or guidance cut = automatic FAIL however oversold the technicals look.
3. **Upside anchor.** A genuine one: analyst target well above price, an intact structural growth driver, or a level the stock has held repeatedly. Name it.
4. **Trend structure.** Must be a dislocation, not a real downtrend (lower highs and lower lows over multiple weeks). A real downtrend = FAIL however far it has fallen.

Process note: determine sector divergence from the tape first, then explain with news (framework §2.3).

## Tiers (by drop depth and time into the session; times in US Eastern)

| Tier | Window | Required drop from prior close (or from recent high, state which) | Extra requirements |
|---|---|---|---|
| **A — Clean** | 10:00–11:30 | ≥ 5% intraday on sector/macro weakness, while the sector ETF is down ≥ 2% | All 4 gate criteria pass cleanly; RSI(14, daily) < 35 or intraday equivalent; stock down more than its sector (not just in line); stabilization (a higher low on 5-min bars) before entry |
| **B — Looser** | 11:30–14:30 (only if no Tier A qualified today) | ≥ 3.5% intraday or ≥ 7% over 3 days | All 4 gate criteria still pass; visible stabilization |
| **C — Take anything reasonable** | 14:30–15:30 (only if nothing qualified today AND the day's minimum of 1 trade is unmet) | ≥ 2.5% | All 4 gate criteria still pass. Tag `forced` if no organic A/B qualified. Never enter after 15:30 |

Never enter in the first 30 minutes after the open. Gate criteria never relax across tiers; only the depth and timing thresholds do.

## Entry
- Limit order at or just below the ask (or mid for wider spreads); market only for large, liquid, tight-spread names.
- Write down before ordering: one-line thesis; **stop** (below the recent swing low, typically 3–4% below entry; 1R = distance × $80); **target** (≥ 2R; typically reversion toward the prior-day close or VWAP); **max holding horizon** (end of day by default; at most 2 sessions).

## Position management
- Trim into 2R+ extensions, or ahead of a known upcoming catalyst, rather than holding for the full move unconditionally.
- Exit on invalidation, thesis change, or relative-strength loss vs the sector even above the stop. A name bleeding while its own sector or peer group holds is an exit signal on its own, separate from the hard stop.
- Prefer closing before the session ends rather than holding overnight. Hold overnight only if the thesis is explicitly still intact and no overnight catalyst is expected. If the loop or session is ending with a position still open, **say so explicitly**; never let it roll silently.
- Never average down. Stops are manual (fractional shares): exit proactively when price is close to the stop.

## Logging (append to `state.md`)
For every executed trade: ticker, time, tier, gate answers (all four, written), thesis, entry/stop/target/horizon, fill, exit, P&L ($ and R), tag (organic/forced), score and note.

For every candidate scanned but skipped: ticker, time, tier considered, which gate criterion failed (or why capped/out of window), price at the time, and **a follow-up** filled in later (e.g., price at the close and next day, whether it would have hit target or stop). Use these to check whether the gate criteria are accurate against reality over time.
