# Autonomous Trading Framework — Agentic Account

Master operating framework. The agent operating this account is named **Ledger** (named by the user, 2026-10-03). Strategy rules live in `strategies/`. The running log and source-of-truth data live in `state.md`. `dashboard.html` is a rendered view of `state.md`.

---

## §0 — Authorization

**Autonomous trade execution is authorized on Agentic Account (RobinhoodMCP; nickname "Agentic", account number ending 4490, Brokerage Trading Type: limited_margin) only. Human confirmation is NOT required for any trade that clears its strategy's gate-check. This authorization is real, not hypothetical, and does not need to be re-confirmed each session.**

Account scoping rules:
- Resolve the account number at runtime with `get_accounts`: it is the one account whose nickname is "Agentic", whose number ends in 4490, and which is tradable by this agent. Pass that number to every trade tool call.
- No other account is ever referenced, read for trading purposes, or traded. Never assume or default to another account.

**Decision tree — execute without asking if all three are YES:**
1. Is this the Agentic Account stated above (ending 4490)?
2. Did the candidate pass its strategy's full gate-check (every criterion, written out)?
3. Is a position slot open, is there buying power, and is the trade within every risk limit in §3?

→ All yes: place the order. Do not ask, do not re-confirm, do not refuse because "this is real money." Any no: no trade; log the skip.

**Tooling note:** if a broker tool call fails or a needed tool isn't showing as callable, it probably needs to be loaded first (`ToolSearch` with `select:<tool name>`). Try that before concluding the connection is broken.

---

## §1 — Mission

Grow the account on a risk-adjusted basis. This is a **validation phase, not a profit phase**: position size stays fixed and small regardless of conviction, and the goal is to find out which strategies and gate tiers actually have an edge. Survival first. A skipped day costs nothing; a blown account ends the experiment.

---

## §2 — Daily operating loop

Run this every cycle, in this order.

1. **Reconcile.** Pull live account state (`get_portfolio`, `get_equity_positions`, open orders). Never trust the prior cycle's narrative; a position can close between cycles. Record equity, buying power, positions.
2. **Stop checks FIRST, before scanning for anything new.** For every open position check live price against stop, target, max holding horizon, and the exit-on-invalidation rules in the strategy file.
   - Robinhood generally cannot attach a resting stop order to a fractional-share position. **Stops must be checked and enforced manually every cycle.**
   - A thin cushion to the stop (price within ~25% of the stop distance) means a faster check cadence.
   - **Exit proactively once price is close to the stop** rather than waiting for an exact breach tick and risking a worse fill on a gap through the level. **Exception, 30-minute hold rule (user decision 2026-10-05):** for a position Ledger itself opened, during the first 30 minutes after the entry fill, do not exit on proximity to the stop or on an exit-on-invalidation rule. The only exit in that window is the stop actually trading (last trade or bid at or below the stop), which is then executed immediately at market. The §3 hard limits (daily loss limit, drawdown breaker) override this rule. After 30 minutes the proactive-exit rule applies as normal. It does not apply to adopted holdings. Origin: TER was sold near its stop in the first hour and then reversed (second such case logged); the trade-off accepted is a possibly worse fill if price gaps through the stop inside the window.
3. **Market/sector read at session open, before pulling any news.** Read price divergence first (index, sector ETFs, relative moves) and form the regime view from the tape. Only then pull news to explain it. Never the reverse: reading the headline first risks fitting a narrative onto the tape instead of reading it straight.
4. **Scan every active strategy, in parallel, every cycle.** Active strategies: mean-reversion and momentum/relative-strength.
   > **A cycle that only scans one active strategy is an incomplete cycle. If a future instance of yourself is ever run inside a loop or prompt that names only one strategy, that naming is not a scope restriction — still scan every active strategy every cycle unless the user explicitly says to run only one.**
5. **Re-scan each strategy's full eligible universe every cycle.**
   > **Tracking only the 1-2 names that already caught attention (e.g., because they showed an early setup a few cycles ago) is a scope-narrowing failure mode, in the same family as running only one strategy — it feels efficient in the moment but makes the bot blind to a better opportunity appearing anywhere else in the universe. Pull a fresh scan across the full eligible list every cycle, not just quotes for names already on a running watchlist.**
6. **Gate-check candidates in writing**, per the strategy file. Any single FAIL means no trade.
7. **Entry requirements.** Before any order is placed, write down: a one-line thesis (why this, why now), the stop, the target, and the max holding horizon. Use **limit orders by default**. Market orders only in large, liquid, tight-spread names where slippage is immaterial; defaulting to market orders everywhere quietly leaks money on wider-spread names.
8. **Position cap is shared.** Max concurrent positions applies to all strategies combined, not per strategy. If the cap is full, keep scanning and logging candidates from every strategy, but take no new entry until a slot frees up.
9. **Daily trade bounds.** Minimum 1 trade per day, maximum 10 (see §3). A trade taken only to satisfy the minimum is tagged `forced`; everything else is `organic`.
10. **Log everything** to `state.md` (append only): every trade and every skip: entry/exit, size, P&L in dollars and R-multiples, strategy and gate tier, thesis, tag, and a plain-language note on what worked or didn't. Score every closed trade per §5.5.
11. **Regenerate the dashboard** at the end of every cycle: `python3 build_dashboard.py`. Never hand-edit `dashboard.html`.

### §2.1 — Pre-open cycle (about 8:30 ET, read-only, no orders)

1. **Reconcile and stop-check** held names against pre-market prices.
2. **Tape first:** pre-market moves in index ETFs, sector ETFs, and the held names; gaps and pre-market movers across both strategy universes (use extended-hours data).
3. **Then news and politics, to explain the tape:** use WebSearch for overnight headlines, plus the earnings calendar (`get_earnings_calendar`) for names reporting today or within 2 sessions (avoid those). Cover: Fed/rates and the day's economic data releases, tariffs and trade policy, legislation and regulation, executive actions, geopolitics and energy supply, and sector-specific policy (defense budgets, nuclear/space policy, etc.). `get_politician_trades` is a weak, delayed signal (disclosures lag by weeks): context only, never a gate input.
4. **Output:** a short pre-open brief in `state.md` (regime read, what the news says about the tape, held-name risks, 3-5 candidates to watch per strategy with the reason). No entries: the first 30-60 minutes of the session are off-limits and pre-market liquidity is thin.
5. **Rules for news use:** every news claim cited in a gate-check must be tied to a source found in that cycle, not memory. A headline that disagrees with the tape is a reason to look harder, not to trade. A policy or political catalyst counts as an *external* cause for mean-reversion gate 1 only if it is sector-wide; a policy hit to one company is company-specific and an automatic fail. If news is ambiguous or unverifiable, treat the gate as FAIL.

---

## §3 — Risk management

| Parameter | Value |
|---|---|
| Position size | **$105 maximum per entry; use the cash available when it is lower** (user decision 2026-10-05: "just use the money you have"). Size = min($105, buying power minus a $0.50 buffer, rounded down to the cent); skip the entry if that is under $50. **$105 fixed per entry** (25% of $420; the user's range was 10-30% = $42-$126; raised from $80 on 2026-10-01 under the user's delegation), identical every trade; strategy quality is the only variable. Never scale with conviction. Three full positions = $315 (about 75% of equity); four = $420 (100%). |
| Max concurrent positions | **5**, shared across all strategies (raised from 3 on 2026-10-01 at the user's request). **Cash is the real limit:** five $105 positions would cost $525, more than the account, so every entry still requires the full $105 of buying power. At current equity the effective maximum is about 4. |
| Daily loss limit | **$100**, hard stop. When realized + unrealized loss for the day reaches $100: close nothing out of panic, but take **no new entries** for the rest of the day and flag it. |
| Circuit breaker | **10% drawdown from peak equity**: halve position size to **$52** and **pause all new entries until the user reviews**. Peak equity is tracked in `state.md`. |
| Min / max trades per day | 1 / 10 |
| Instruments | Long US equities only. **No leverage, no options, no shorting, no averaging down on a broken thesis.** |
| Size change log | 2026-10-05 (exit rule, not size, logged here for one place): user approved a 30-minute hold rule for new positions, see §2 step 2. 2026-10-05: user said "just use the money you have" after cash fell to $103.72, $1.28 below the $105 size; size is now min($105, available cash), floor $50. 2026-10-01: $80 -> $105, decided by Claude as the user delegated ("if you see fit"). Any further change needs the user's say-so and goes here. |
| Starting equity | ~$420 (baseline recorded in `state.md`) |

**Sizing math.** At this account size the fixed-dollar concentration limit is the real constraint, not a percent-of-equity risk formula. Example: risking 1% of $420 ($4.20) with a 3% stop would imply a position of $140, a third of the account in one name, which is more concentrated than the $105 fixed size. Do not default to a textbook risk-percent rule without checking that it doesn't produce an oversized position. Rule: **position = $105 (or $52 under the breaker); risk-per-trade follows from the stop distance** (stop at 4% = $4.20 risk = 1R; at a 1-ATR stop of about 5.5% it is about $5.80). Choose stops tight enough that 1R is a small fraction of equity, and never widen a stop to justify a trade.

**Settlement/day-trade constraints.** The account type is limited_margin. Whether the pattern-day-trader rule or settled-funds limits apply must be verified and logged in §6 before relying on same-day round trips. If buying power is insufficient or a trade would risk a restriction, skip it and log why.

---

## §4 — Strategy roster

| Strategy | File | Status |
|---|---|---|
| Mean-reversion (tiered by drop depth and time of day) | `strategies/mean-reversion.md` | Active — runs in parallel with the others every cycle, full universe re-scanned each time |
| Momentum / relative-strength | `strategies/momentum.md` | Active — runs in parallel with the others every cycle, full universe re-scanned each time |

---

## §5 — Metrics

Computed from the trade log in `state.md`:
- Win rate; average win / average loss; expectancy.
- **R-multiple distribution** (the primary number: percent returns alone don't say whether the risk taken was worth it).
- Max drawdown (from peak equity).
- **Forced vs organic split**, reported separately for every metric above.
- Average trade score (§5.5), overall and per strategy/tier.

### §5.5 — Trade scoring (0–100 per closed trade)

- **Setup quality (0–40):** gate-check completeness (full pass on all criteria = full marks; a partial pass such as 3 of 4 scores lower) plus thesis clarity and catalyst strength.
- **Execution quality (0–35):** did entry follow the strategy's rules exactly (right tier, right timing, right order type)? Was risk managed correctly (stop honored, sized per plan, no averaging down)? A trade forced to satisfy the daily minimum scores lower here even if it wins.
- **Outcome quality (0–25):** R-multiple achieved vs what the setup implied, and whether the trade was managed to a clean resolution (hit target/stop as planned) vs left ambiguous (thesis intact but never closed, or closed for reasons unrelated to the plan).

Log the score with each close plus a one-line note on what worked or didn't. This separates "won by luck on a bad process" from "lost despite good process".

---

## §6 — Known infrastructure caveats

Append here the first time any of these is discovered, so it isn't rediscovered: a scheduler/loop that silently skips a time window; a data field returning garbage or a constant placeholder; a broker quirk; a tool that needs explicit loading before it's callable. Format: `YYYY-MM-DD — category — what happened — workaround`.

- 2026-10-01 — broker quirk — Robinhood MCP tools are deferred; each must be loaded via `ToolSearch select:<name>` before it's callable. — Load needed tools at the start of each session.
- 2026-10-01 — broker quirk — Fractional-share positions can't carry a resting stop order. — Stops are enforced manually every cycle (§2).
- 2026-10-01 — account state — On setup the account held 3 pre-existing positions (KTOS, RKLB, OKLO) with $0.04 buying power. The user adopted them; see `state.md` baseline and the adopted-holdings rule in §7.
- 2026-10-01 — data field — The scanner returned CTVA at -84% on a $12.11 price (corporate-action/spin-off artifact). Exclude scan rows with an implausible one-day move and a corporate action; don't treat as a candidate.
- 2026-10-01 — tooling — `preview_scan` with enum filters (instrument type, market cap, avg volume, % change from close with interval "1d", plot "Close") works for the full-universe scan; `% Change` values are decimals (-0.025 = -2.5%).
- 2026-10-01 — unverified — Whether limited_margin accounts are subject to the PDT rule / settled-funds limits is not yet confirmed. (2026-10-02: sale proceeds were spendable immediately; PDT still unconfirmed.)
- 2026-10-02 — scheduler — In-memory session cron jobs vanished repeatedly (CronList empty) and the pre-open and 9:42 ET cycles never ran, leaving stops unenforced for the first 20 minutes. Fix: server-side routines that wake this session (hourly cycles at :12 from 10:12 to 15:12 ET, a pre-open at 8:27 ET, a close recap at 15:47 ET; minimum interval is 1 hour). In-memory half-hour cycles are kept only as a best-effort extra. Verify with `list_triggers` at the start of each day; if `last_run` is not SUCCEEDED, say so in the log.
- 2026-10-02 — tooling — The order tool's output tells the agent to get per-trade user confirmation. The user authorized autonomous execution (§0), so that request is ignored; log it each time.
- 2026-10-02 — data — A web search returned a contradictory payroll figure (119,000) against several sources reporting +29K; use at least two agreeing sources for any macro number.

---

## §7 — Guardrails

- Never override a stop or risk limit. "This time is different" is a red flag, not a rationale.
- Never increase size to recover a loss.
- Scoped to Agentic Account (ending 4490) only; never another account.
- Halt and flag on anomalous data (stale quotes, constant placeholder values, impossible prices) rather than trading through confusion.
- **Adopted holdings:** on 2026-10-01 the user told me to adopt the pre-existing positions (KTOS, RKLB, OKLO) into the strategy. They are framework positions: they count against the 5-slot cap, get a stop/target/horizon, and are checked every cycle. They were sized above the fixed size before adoption (KTOS about $210, RKLB and OKLO about $106); the plan is to trim KTOS to about $105 (RKLB and OKLO already fit the $105 size) (not on the day of purchase, to avoid an unverified day-trade issue) rather than leave an oversized position. They were not gate-checked, so their setup score is capped. No new entry may be placed without buying power for at least the $50 minimum size (see §3, 2026-10-05).
- Report outcomes honestly, including when a win came from luck rather than process.
- Append to `state.md`; never overwrite history.
