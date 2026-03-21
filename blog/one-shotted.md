# One-Shotted

![Minard's 1869 chart of Napoleon's Russian campaign](minard-1869.png)

This is Charles Joseph Minard's 1869 chart of Napoleon's march to Moscow. It shows six variables on a single plane: the size of the army, its location, the direction of movement, temperature, latitude and longitude, and dates. No legend. No chart-type selector. No dashboard toggle. The form *is* the argument. The shrinking band *is* the dying army. You read it once and you understand what happened to six hundred thousand men.

It is, by wide consensus, one of the greatest data visualizations ever made.

---

Here's an experiment. Open your favorite AI tool and type: "Visualize Napoleon's march to Moscow."

You'll get something. A map with red dots along the route. A line chart of troop strength over time. A timeline with key battles annotated. Maybe a bar chart comparing the outbound army to the survivors.

Every one of those outputs is correct. None of them is *this*.

The gap between "correct" and "this" is the entire subject of this post.

---

Minard didn't pick a chart type from a menu. He invented one. He took the geographic path of the march and turned it into the horizontal axis. He made the width of the band proportional to the number of surviving soldiers, so the visual shrinks as you read it left to right -- and then shrinks further on the return. He added a temperature line along the bottom, aligned to the same geography, so you don't just see the army dying, you see *why*. The Berezina River crossing. Minus 30 degrees.

No chart library would suggest this. No prompt would produce it. Minard made a hundred editorial decisions to get here. What to combine: geography and mortality and temperature on a single plane. What to omit: battles, supply lines, politics, the names of generals. What to bend: the path isn't geographically precise, because precision would have made it harder to read. He sacrificed accuracy for clarity, deliberately, because he understood what the data was trying to say.

That is editorial judgment. It is a completely different skill from execution.

---

Most of your friends or colleagues are getting one-shotted by AI.

Here's what I mean. Someone has a dataset. They open Claude or ChatGPT or Copilot and say "make me a chart." They get a chart. It looks clean, the axes are labeled, the code runs. They ship it.

They never consider a second option. They never look at the output and ask: is this the right chart, or just *a* chart? They got one-shotted -- they accepted the first thing the machine produced, and moved on.

This isn't limited to charts. A product manager asks AI to draft a strategy doc and ships the first version. A developer asks for a database schema and implements what comes back. A designer asks for a landing page layout and builds it. In each case, the output is competent. It follows conventions. It hits the expected beats. And in each case, the person never paused to ask: is this what *this specific problem* needs, or is this what *most problems like this* get?

The difference matters. Convention is a statistical average of past solutions. Your problem isn't average. But you'll never discover that if you don't look.

This isn't because people are lazy. It's because of a deeper shift in how work feels.

When making a chart took four hours, you spent the first hour thinking about *which* chart to make. You sketched on paper. You argued with a colleague. You considered three approaches and threw out two. The friction of execution created a natural pause, and the pause is where judgment lives.

When making a chart takes thirty seconds, the pause disappears. You type, you get output, you ship. The tool that removes friction also removes the moment where you would have thought about whether this was the right thing to build.

The bottleneck moved, and most people didn't notice.

---

For decades, the skill stack in most knowledge work looked like this: a thin layer of taste and judgment on top, a thick layer of implementation on the bottom. Knowing what to build was important but fast. Actually building it was the slow, expensive, career-defining part. You got hired and promoted for execution. Junior devs, junior analysts, junior designers -- they all started by proving they could *make things*.

AI just inverted that stack.

Implementation is now cheap and fast. Any junior dev can generate a working component. Any analyst can get a chart. Any designer can produce a layout. The thick layer at the bottom compressed to almost nothing.

What's left is the thin layer at the top. Taste. Editorial judgment. The ability to look at a dataset and see that it's not a bar chart, it's a flow. The ability to look at an AI-generated draft and know it's wrong before you can articulate *why* it's wrong. The ability to throw away a working output because working isn't the same as good.

These skills were always valuable. But they used to be 20% of the job. Now they're 90% of the job, and most people haven't adjusted.

There's a second-order effect too. When execution was expensive, bad ideas died early. You wouldn't spend three weeks building a dashboard nobody asked for. The cost imposed discipline. Now that execution is nearly free, there's nothing stopping you from building the wrong thing instantly. The number of artifacts in the world -- charts, docs, apps, analyses -- is exploding, and the average quality is dropping, because the filter that used to exist between "I had an idea" and "I shipped it" has been removed.

This is the environment you now operate in. A flood of competent, conventional, AI-generated output. The way to stand out isn't to produce more of it faster. It's to produce something the flood can't.

---

The common advice is "learn to prompt better." I think that's wrong, or at least incomplete. Prompting is still execution. It's the new typing. Getting good at prompting is like getting good at using a better hammer -- you'll drive nails faster, but you still need to know where to put them.

What actually matters now is learning to see.

Study Minard. Study Tufte. Study the NYT graphics desk, who consistently produce visualizations that no prompt could generate, because the form of each piece is an argument about the data that required a human to construct. Look at W.E.B. Du Bois's hand-drawn infographics from 1900, which made an argument about Black American life that was inseparable from their visual design. Look at Florence Nightingale's coxcomb diagram, which saved lives not because it was technically impressive but because she understood that the British military establishment would be moved by a particular kind of visual evidence.

Before you open an AI tool, sit with your data. Ask what story it's trying to tell. Ask what a reader needs to understand, and what would get in the way. Ask whether the obvious chart type -- the one AI will suggest -- is actually the right one, or just the default.

Here's a concrete practice: write down what you want before you prompt. Not the prompt -- the *intent*. "I want to show that the decline accelerates after 2015" is an editorial statement. "Make me a chart of this data" is a delegation of judgment. The first will lead you to a specific form. The second will lead you to whatever the model's default is. One sentence of intent, written before you touch the keyboard, is worth more than ten rounds of prompt refinement after.

And when you do get output, resist the pull of completion. A finished-looking artifact triggers a satisfaction response -- it looks done, so it feels done. Train yourself to distrust that feeling. The first output is a draft, not an answer. Ask: what did this miss? What would I change if I had to present this to someone whose opinion I respect? What would Minard do?

The people who will do remarkable work with AI are the same people who would have done remarkable work without it. They'll just move faster. They were never bottlenecked by execution in the first place. They were bottlenecked by hours in the day, and AI gives them more of those. Everyone else gets to produce more mediocrity, faster.

---

The gap between AI-generated and AI-assisted is the gap between taking the first draft and knowing what to ask for next. Between accepting a correct output and pushing toward a *good* one. Between being one-shotted and doing the hard work of seeing clearly.

That gap is the whole game.
