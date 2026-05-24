---
UID: Z202508131218000
public: true
---
vibe coding--even with spec-driven-development and robust tests--is extremely dangerous. you MUST adopt a mindset of skepticism and strict review, but DESPITE the "acceptance bias" that we all have for when something matches what we intend it to be. It is a more dramatic version of "you can't see your own typos" because **the whole point of agentic-coding is to operate at a much greater scale and depth than you could on your own. You're *asking* for blind spots**, and so putting on the reviewer hat both requires more intentionality to not put it on half-assedly, and more attention to the actual skeptical review conducted once the hat is on. *

_(2025-12-31: See also [integrate instead of merely collecting](integrate%20instead%20of%20merely%20collecting.html). And [AI as a thought partner](AI%20as%20a%20thought%20partner.html) becomes as much a warning as an aspiration.)_

It's also therefore (necessary but not sufficient) critical to always prompt for the absolute-minimum changes, with explication of why those that are included are truly needed. If you want to take the agent's "taste" or "while we're here" recommendations--including unrelated bugs it caught--those really need to be made separately. (So including a TODO list or add'l PRDs in a changeset is acceptable, it's *functional* changes that must be tightly-constrained).


A few days after making this observation, I came across this exact idea:

> **Language models don’t deliver productivity improvements. _They increase the volume_, unchecked by reason.**
>
> A core aspect of the theory-building model of software development is _code that developers don’t understand is a liability_. It means your mental model of the software is inaccurate which will lead you to _create bugs_ as you modify it or add other components that interact with pieces you don’t understand.
>
> Language model tools for software development are _specifically designed to create large volumes of code that the programmer doesn’t understand._ They are liability engines for all but the most experienced developer. You can’t solve this problem by having the “AI” understand the codebase and how its various components interact with each other because a language model isn’t a mind. It can’t have a mental model of anything. It only works through correlation.
>
> These tools will indeed make you go faster, but it’s going to be accelerating in the wrong direction. That is objectively worse than just standing still.

https://softwarecrisis.dev/letters/ai-and-software-quality/

