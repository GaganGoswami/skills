# Assumption Categories

Four categories to scan when hunting for hidden assumptions in plans, designs, and code.

## Technical assumptions

Beliefs about how systems, infrastructure, and code behave.

- Performance: "This query will run in < 100ms at scale"
- Availability: "This service will be up when we need it"
- Compatibility: "This library version is compatible with our runtime"
- Data: "This field will always be populated / always be in this format"
- Limits: "We will never exceed X records / X concurrent users"
- Third-party behavior: "The API will always return in this shape"

**Decay rate: Medium** — watch after major deploys, library upgrades, or traffic spikes.

## User assumptions

Beliefs about what users will do, understand, feel, or tolerate.

- Behavior: "Users will complete onboarding before using feature X"
- Mental model: "Users understand what 'sync' means in this context"
- Tolerance: "Users will wait up to 3 seconds for this to load"
- Frequency: "Users will check this dashboard daily"
- Discovery: "Users will find the settings panel on their own"

**Decay rate: High** — user behavior shifts with product changes, competitor moves, and demographic shifts.

## Business assumptions

Beliefs about the market, economics, regulation, and organizational context.

- Market size: "There are enough customers who have this problem"
- Willingness to pay: "Users will pay $X/month for this"
- Regulatory: "This data processing is compliant with current regulations"
- Competitive: "No competitor will launch a similar feature in the next 6 months"
- Organizational: "Team X will maintain this after we ship it"
- Prioritization: "This is the highest-leverage thing we could build"

**Decay rate: High** — market conditions, regulations, and org structures change frequently.

## Temporal assumptions

Beliefs that were true at a point in time but may no longer hold.

- Stale data: "The benchmark/survey/interview that informed this decision is still relevant"
- Version lock: "The framework version we chose is still the right one"
- Team knowledge: "The person who made this decision is still available to explain it"
- Infrastructure state: "The infra that exists today will still exist when this ships"
- External dependencies: "The partner/vendor/API will still be available at launch"

**Decay rate: Very high** — anything older than 6 months should be re-verified. Anything older than 12 months should be treated as unverified.

## Scoring evidence quality

| Level | Description |
|---|---|
| **Strong** | Measured, recent (< 3 months), from primary source |
| **Weak** | Anecdotal, indirect, or > 6 months old |
| **None** | "We just assumed it" / never checked |
