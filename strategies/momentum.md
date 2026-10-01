# Strategy: Momentum / Relative-Strength

Account scope: Agentic Account (ending 4490) only. Runs in parallel with `mean-reversion.md` every cycle; the full eligible universe is re-scanned each time. Risk numbers come from `framework.md` §3 ($105 fixed size, shared cap of 3 positions).

## Universe
- US-listed common stocks, market cap ≥ $2B.
- Liquidity: average daily volume ≥ 1M shares and ≥ $20M dollar volume; bid-ask spread ≤ 0.3% of price.
- Tradable fractionally on the broker.
- Grouped into peer complexes (sector/theme baskets). Relative strength is always measured against the stock's own peer complex.
- Not in an earnings window (no report within 2 trading days before entry), unless the earnings catalyst already happened and is the thesis.

## Gate-check (required in writing before ANY entry)
One FAIL means no trade.

1. **Relative-strength divergence.** A specific name separates from its peers (clearly outperforms the peer complex today and over the last several sessions). A uniform sector-wide move with no standout is a sign the whole group may still be falling together, not a signal to chase. Wait for a name that separates.
2. **Real catalyst.** Confirmed by more than a same-day price move alone (news, filing, estimate revisions, contract, guidance, sector driver). Cite it.
3. **Held pullback/retest.** Not the first tick down and never the first tick of a bounce off a low. Require **rising short-term support** (e.g., price holding above a rising 9/20 EMA on 5–15 min bars) and a **genuine base: a higher low versus the prior low**, not just a green candle.
4. **Timing.** **Never enter within the first 30–60 minutes of the session open.** Let the opening range establish first (earliest entry 10:30 ET). No new entries after 15:30 ET.

Process note: determine relative strength from the tape first, then explain with news (framework §2.3).

## Entry
- Entry on the continuation (a break back above the pullback high or a hold-and-reclaim of the short-term average).
- Limit order by default; market only for large, liquid, tight-spread names.
- Write down before ordering: one-line thesis; **stop** (below the higher low that formed the base, typically 3–4% below entry; 1R = distance × $105); **target** (≥ 2R, e.g., prior high plus measured move); **max holding horizon** (end of day by default; at most 3 sessions if the trend and relative strength stay intact).

## Position management
- Trim into 2R+ extensions, or ahead of a known upcoming catalyst, rather than holding for the full move unconditionally. After a trim, the stop moves to breakeven or the new higher low.
- Exit on invalidation, thesis change, or relative-strength loss vs the sector even above the stop. A name bleeding while its own sector or peer group holds is an exit signal on its own, separate from the hard stop. A close back below the rising short-term support is an invalidation.
- Prefer closing before the session ends rather than holding overnight. Hold overnight only if the thesis is explicitly still intact and no overnight catalyst is expected. If the loop or session is ending with a position still open, **say so explicitly**; never let it roll silently.
- Never average down. Stops are manual (fractional shares): exit proactively when price is close to the stop.

## Logging (append to `state.md`)
For every executed trade: ticker, time, peer complex and its relative-strength numbers, gate answers (all four, written), thesis, entry/stop/target/horizon, fill, exit, P&L ($ and R), tag (organic/forced), score and note.

For every candidate scanned but skipped: ticker, time, which gate criterion failed, price at the time, and **a follow-up** filled in later (e.g., whether it continued, whether the stop or target would have hit). Use these to check whether the gate criteria are accurate against reality over time.
