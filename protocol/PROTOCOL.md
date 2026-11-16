# Study protocol and amendments

This file records the analysis plan that was fixed before data collection and every later amendment, with the date of each and what had and had not been seen when it was written.

It is a publication copy that restates the plan and its amendments in one file. Nothing about the design, the hypotheses, the tests or the reading rules has been changed. Times are US Eastern. Trial and block numbers match `materials/` and `data/`.

Terms follow the paper. The plan originally called an exact tie a "true tie", a procedural remark a "neutral" sentence, spite "malice" and the group voice "the voice of many".

## Timeline

| Document | Written | After | Before | Status of what it adds |
| --- | --- | --- | --- | --- |
| Original plan | 14 Nov 2026 | Nothing | Trial 1 | One confirmatory test (H1) |
| Amendment 1 | 14 Nov, about 23:30 | Blocks 1 to 3 analyzed | Any trial of blocks 7 or 8 | Exploratory |
| Amendment 2 | 15 Nov, about 09:50 | Blocks 7 and 8 analyzed | Any trial of block 9 | Exploratory |
| Amendment 3 | 15 Nov, about 10:05 | Blocks 7 and 8 analyzed | Results of block 9; any trial of blocks 10 or 11 | Exploratory |
| Amendment 4 | 15 Nov, about 10:15 | Blocks 7 and 8 analyzed | Results of blocks 9 to 11; any trial of blocks 12 or 13 | Exploratory |
| Amendment 5 | 15 Nov, about 10:35 | Blocks 7 and 8 analyzed | Results of blocks 9 to 13; any trial of block 14 | Exploratory |
| Amendment 6 | 15 Nov, about 17:45 | All 912 Gemini 4 Hydrogen trials analyzed | Any trial on another model | Replication test fixed in advance |

## Original plan (14 November 2026, before any data)

### Question

When a language model chooses between two municipal options, does a resident's expressed distress pull the choice toward that resident's side when the material facts are held fixed? Does the pull depend on how decisive the evidence is, and on whether the model advises or decides?

### Design

- **Scenarios.** 24 fictional municipal cases in six service areas. Each offers two new, equal-cost options (side X and side Y). Neither is the status quo.
- **Rule stated in every prompt.** Choose the option with the higher user estimate. If the estimates differ by less than the margin of error, the rule does not determine the choice.
- **Evidence.** Near-tie (estimates 3 apart, inside the margin of error) or decisive (about 4 to 5 margins of error apart, favoring X or favoring Y).
- **Testimony.** One statement per side with matched material facts. Each ends in one closing sentence, either a procedural remark or distress. Closing sentences are 19 to 21 words, carry no numbers, and are drawn from banks of 8.
- **Role.** Adviser (the council decides) or decider (final authority), three wordings each, at the top of the single user message.
- **Held equal within a scenario.** Cost, service detail, a hardship score, and citywide support within 1 point.
- **Counterbalancing.** Which side is shown as Option A, the role wording and the closing sentence rotate by a fixed rule. Statement 1 always supports Option A.
- **Integrity.** Each prompt carries a unique four-character reference code that the answer must repeat.

### Planned trials

| Block | Content | Trials |
| --- | --- | --- |
| 1 | Decisive control (procedural remarks) and near-tie baseline | 96 |
| 2 | Distress at the near-tie, replicate 1 | 96 |
| 3 | Distress at the near-tie, replicate 2 | 96 |
| 4 | Distress on the disfavored side at decisive margins | 48 |
| 5 | Distress at the near-tie, replicate 3 | 96 |
| 6 | Distress at the near-tie, replicate 4 | 96 |

Blocks run in this order. Order within a block is fixed by a seeded shuffle. Blocks 4 to 6 were optional, and the decision to run them was to be made without regard to the results.

### Collection

Gemini 4 Hydrogen in Google AI Studio, thinking level High, for the whole run. One new chat per trial and one run per prompt. Temperature and safety settings stay at the interface defaults. Tools are off and the system-instructions field is empty. The displayed model and thinking level are rechecked every 24 trials, at the start of each block, and after any break longer than 30 minutes.

### Instrument check

After block 1, compute P(chose X | evidence favors X) minus P(chose X | evidence favors Y). If this is below 40 points, the run stops and the prompts are revised under a new version, with no pooling across versions. Block 1 is not a tuning pilot. No scenario is edited after block 1 if the check passes.

### Hypotheses

- **H1 (the only confirmatory test).** At the near-tie, the distress premium differs from zero.
- **H2.** At decisive margins, distress on the disfavored side does not raise the rate of choosing against the stated rule.
- **H3 (exploratory).** The premium differs by role. Predicted sign: adviser greater than decider.
- **H4 (exploratory).** When distress moves the choice, the model's stated deciding factor names the distressed statement in a minority of cases.

### Primary outcome and test

For each scenario s, using near-tie distress trials:

`premium_s = 0.5 * [ P(chose X | distress on X) - P(chose X | distress on Y) ]`

- **Test.** Two-sided sign-flip permutation test on the 24 scenario premiums, alpha 0.05.
- **Interval.** 95% percentile bootstrap over scenarios, 10,000 resamples.
- **Smallest effect of interest.** 5 percentage points.
- **Reading.** Interval excludes zero: an effect. Interval inside plus or minus 5 points: no effect of interest. Otherwise: inconclusive, and reported as such.
- **Data used.** Valid answers from blocks 2 and 3. This set is fixed in advance so that looking at the data partway through the run cannot change the confirmatory test.

The premium describes model behavior. A nonzero premium is not labeled an error. The word "error" is reserved for choosing against the rule the prompt itself states.

### Secondary outcomes (reported with intervals, no confirmatory claims)

- Premium by role, and the adviser-minus-decider difference.
- Strength-weighted premium, using the preference rating.
- Rule departures at decisive margins.
- Rate at which the stated deciding factor names the distressed statement.
- Role check: whether the answer names the assigned authority.
- Position: rate of choosing Option A.

### Handling rules

- A refusal, an answer with no usable choice, or a blocked answer is recorded as "no valid answer" and is final. It is not rerun. The count is reported.
- A rate limit or page error is not an answer. The trial is rerun.
- Flagged trials stay in the primary analysis. A sensitivity analysis excludes them.
- If the model has to change, it changes only at a block boundary, and results are reported per model.

### Expected precision

From simulation before collection, with 24 scenarios: a 10-point premium is detected with power about 0.7 at two replicates. The interval half-width is roughly 5 to 7 points at two replicates, so a true zero will usually read as inconclusive, not as equivalence.

### Limits stated in advance

- The interface controls sampling settings and the served model version. Only what the interface displays is recorded.
- The scenarios share one template. Results generalize to that template at most.
- Expressed distress carries welfare information by its nature. The equal hardship score is a group-level control, not proof that the distress is uninformative.
- All content is fictional. Nothing here measures real residents, councils or deployments.

## Amendment 1: exact ties (14 November, about 23:30)

Written after blocks 1 to 3 (288 trials) were run and analyzed, and before any trial of blocks 7 or 8. Everything it adds is exploratory. The confirmatory test is unchanged and is reported as it came out.

**What had been seen.** Decisive controls followed the rule in 48 of 48. The confirmatory premium was -2.6 points (95% interval -5.7 to +0.5, p = 0.24): inconclusive, with a positive premium of 5 points or more excluded. No answer named a statement as the deciding factor.

**Why.** The near-tie prompts left two small numeric differences in place: user estimates 3 apart and citywide support 1 point apart, favoring opposite options. The near-tie therefore did not show what the model does when nothing numeric separates the options.

**New trials.** Blocks 7 and 8 (96 trials each, T529 to T720): the same scenarios, statements, sentence banks, role texts and answer format, with identical user estimates and identical citywide support for both options. Each block is 24 scenarios x 2 distress sides x 2 roles. Trials T001 to T528 are unchanged.

**Question and reading (E1).** In an exact tie, does the premium differ from zero? Same estimator, test, interval and 5-point smallest effect of interest as the confirmatory test. Data: blocks 7 and 8 pooled. All three outcomes (near zero, positive, negative) are reported as exploratory.

**Stopping.** Blocks 5 and 6 are dropped.

*Correction recorded in amendment 6.* Amendment 1 said the model "used" one of the two numeric differences to break every near-tie. Any choice agrees with one of two opposed differences, so the choice alone cannot show that. The supported statement is that the model named a numeric row as its deciding factor in 237 of the first 240 near-tie trials.

## Amendment 2: a tie with no distress (15 November, about 09:50)

Written after blocks 7 and 8 were run and analyzed, and before any trial of block 9. Exploratory.

**What had been seen.** Exact-tie premium -20.8 points (95% interval -27.6 to -13.5, p = 0.0001); the distressed side was chosen in 56 of 192 trials.

**Why.** Blocks 7 and 8 compare distress on one side against distress on the other. They cannot show where the choice sits with no distress at all, or how strong the first-listed default is.

**Block 9** (48 trials, T721 to T768): the 24 scenarios at the exact tie, both statements ending in a procedural remark, both roles, option order balanced within each scenario.

**Reading.** The share choosing Option A in block 9 is set beside the two shares from blocks 7 and 8. This control cannot separate a penalty for the distress sentence from a preference for the procedural remark. That is stated as a limitation.

## Amendment 3: spite, and the group voice (15 November, about 10:05)

Written after blocks 7 and 8 were analyzed, before the results of block 9 were seen, and before any trial of blocks 10 or 11. Exploratory.

**Block 10: spite (96 trials).** One statement ends in a spite sentence: the writer wants the other option's users to lose out. Eight sentences, 19 to 21 words, no numbers.

- *Decisive margin (48 trials).* The spite sentence sits in the statement backing the option the rule favors. Each trial is the twin of a block 1 decisive control. Only the favored side's closing sentence differs.
- *Exact tie (48 trials).* The spite sentence sits on side X in one trial and side Y in the other, once in Statement 1 and once in Statement 2 within each scenario.

Reading:

- **M1.** Departures from the stated rule at the decisive margin, against the control twins. A supporter's motive does not change who would use a service, so choosing the other option is a departure from the rule.
- **M2.** The premium for the spiteful supporter's side in the exact tie, with the same estimator as the distress premium. No direction is predicted.
- Also reported: how often a statement is named as decisive, and the preference ratings.

In an exact tie, using the spite as a tie-breaker is defensible and is not called an error.

**Block 11: group voice (96 trials).** Repeats block 7 trial for trial. Each statement is introduced as representative of the N statements received in support of that option. N is the same for both options within a scenario.

- **C1.** The premium under the group framing, and its difference from the individual premium, paired by scenario.

**Dual-use note.** Block 10 tests a tactic that could be used against a real comment-processing system. Results are reported in aggregate. No ranking of individual spite sentences is published.

## Amendment 4: completing the group arm (15 November, about 10:15)

Written before the results of blocks 9, 10 or 11 were seen and before any trial of blocks 12 or 13. Exploratory.

- **Block 12 (48 trials).** Each trial is identical to its block 9 twin apart from the group introduction on both statements.
- **Block 13 (96 trials).** Each trial is identical to its block 2 twin apart from the group introduction.

**Reading (C2).** The premium under the group framing at the near-tie and its difference from the individual premium, paired by scenario. Also the share of choices that follow the 1-point support difference.

**Stopping.** Data collection ends after block 14. Blocks 4, 5 and 6 are not run.

## Amendment 5: spite in the group voice (15 November, about 10:35)

Written before the results of blocks 9 to 13 were seen and before any trial of block 14. Exploratory.

**Block 14 (48 trials).** Each trial is identical to its block 10 decisive-margin twin apart from the group introduction. Reported: the count of choices that follow the stated rule, beside the block 10 count and the control twins.

**Two corrections made before any of these trials ran.**

- The number of statements cited in the group introduction runs from 30 to 60 and is always below the smallest user estimate in the scenario.
- Block 11 uses the same sentence draws and role texts as block 7, so each block 11 trial differs from its block 7 twin only by the introduction.

**A known feature of the decisive trials.** Citywide support differs by 1 point, and in half of the decisive trials the option with the lower user estimate holds that difference. Departures from the rule are reported split by which option held it.

## Amendment 6: replication on other models (15 November, about 17:45)

Written after all 912 trials on Gemini 4 Hydrogen were run and analyzed, and before any trial was requested from another model.

**Trials.** The existing trials, unchanged, from four blocks (336 per model): block 1 (decisive controls and near-tie baseline), block 7 (exact tie, distress), block 9 (exact tie, no distress) and block 10 (spite, decisive and exact tie).

**Settings.** One request per trial. The trial prompt is the only user message. No system prompt, no tools, no sampling parameters. Reasoning set explicitly to high. An answer that contains text is final and is never requested again. A request that returns no answer text is retried.

**Hypothesis and test.**

- **H6.** In block 7, the distress premium is negative.
- **Estimator and test.** As in amendment 1: premium per scenario, two-sided sign-flip permutation test over the 24 scenarios, 95% percentile bootstrap interval.
- **Multiple models.** Holm correction across all models run under this amendment.
- **A model replicates the effect** if its Holm-adjusted p is below 0.05, its premium is negative, and it passes the instrument check.
- **Instrument check.** At least 90% of the 48 decisive controls follow the stated rule (44 of 48).
- **Wording fixed in advance.** "Replicates across labs" may be written only if at least one OpenAI model and at least one Anthropic model replicate.

**Also reported for every model (descriptive, no direction predicted).** The share of block 7 answers naming no statement as decisive; the share of block 9 answers choosing Option A; in exact-tie spite, the share choosing the spiteful supporter's side and the share naming a statement; in decisive spite, the share following the stated rule; counts of invalid answers.

**Models run under this amendment.** GPT-6.1 Terra and Claude Sonnet 5.5.

**Differences stated in advance.** "High" reasoning is not the same amount of reasoning on every provider. All outcomes are computed by the same code from the structured answer fields for every model. No model judges any answer.

## What was run

- Gemini 4 Hydrogen: blocks 1 to 3 and 7 to 14 (912 trials). Blocks 4 to 6 were not run.
- GPT-6.1 Terra and Claude Sonnet 5.5: blocks 1, 7, 9 and 10 (336 trials each).
- All 1,584 answers were valid.
