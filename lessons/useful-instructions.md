# You write instructions that fix observed confusion

Repeated confusion shows exactly which project decision your instructions failed to carry. You will turn one observed misunderstanding into guidance, then confirm the next attempt receives it.

## Observe confusion before writing

<a href="#cite-c0404">Hamel Husain and Shreya Shankar</a> say observation helps people express their requirements clearly. Start with a representative task that confused the agent or produced an unwanted result. Record the action the agent attempted and the result you expected instead. Then name the project decision that would have changed the agent’s choice. Use little extra explanation while diagnosing, and keep every standing safeguard and authority limit.

## Place each correction where it works

<a href="#cite-c0411">The smol-ai project</a> recommends adding prompt detail whenever a run exposes underspecification. That timing keeps every addition directly tied to confusion you have actually seen. Put a correction beside the decision when only one project area needs it. Use shared guidance when the same decision governs many tasks across the project. Update changing facts from their source, so later changes reach the guidance safely. Use reusable guidance when the agent needs a procedure requiring judgment across several tasks.

## Write decisions with reasons and limits

Only record settled project decisions, because instructions cannot resolve an open product choice. State each decision as an action the agent can recognize and follow. Name the condition that makes this action relevant to the current task. Give the reason, so later changes can separate durable guidance from an outdated preference. <a href="#cite-c0375">Mitchell Hashimoto says each instruction line in his setup</a> came from a bad agent behavior. <a href="#cite-c0007">Theo Browne demonstrates this pattern</a> by turning an unwanted request into an explicit stop rule. Revise the guidance after an authorized decision changes, while preserving why the earlier rule existed.

## Confirm the next attempt receives it

Before rerunning, compare the new wording with the recorded misunderstanding and expected decision. Confirm the working system loaded the changed guidance before attributing any improvement to it. Repeat the same task with the same starting conditions whenever they remain available. Check whether the agent notices the decision before reaching the earlier wrong action. <a href="#cite-c0044">Shreya Shankar writes discoveries from output review</a> back into the skill guiding future runs. One passing attempt proves only that the observed misunderstanding was resolved during that attempt.

## Promote repeatable failures into checks

Instructions can steer a choice, but prose alone cannot guarantee repeated compliance. When a failure has a clear mechanical boundary, add a check that rejects it. Keep the written reason beside that check, so readers understand its boundary and valid alternative. A stop rule remains useful for judgments that no reliable check can express. Test a bad example and a valid example before calling any automated boundary effective.

## These sources connect observation to correction

The sources agree that useful instructions begin with behavior someone has actually observed. They connect review findings, specific failures, and exposed gaps to the next written correction. <a href="#cite-c0007">Theo Browne’s example</a> supports explicit stop rules, while <a href="#cite-c0044">Shreya Shankar’s review loop</a> supports feeding discoveries into reusable guidance. <a href="#cite-c0375">Mitchell Hashimoto</a>, <a href="#cite-c0404">Hamel Husain and Shreya Shankar</a>, and <a href="#cite-c0411">smol-ai</a> support grounding additions in observed behavior. Together, these sources support one improvement loop and no promise that prose guarantees compliance.

<ol id="citations">
<li id="cite-c0007">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&amp;t=813s">A Message for Passionate Devs</a>, at 13:33. “If they ask for this, stop and tell them no”</li>
<li id="cite-c0044">Shreya Shankar, video, <a href="https://www.youtube.com/watch?v=tqUDjc1HzO4&amp;t=840s">Using AI for AI Evals</a>, at 14:00. “I try to encode that back into the skill”</li>
<li id="cite-c0375">Mitchell Hashimoto, blog, <a href="https://mitchellh.com/writing/my-ai-adoption-journey#:~:text=Each%20line%20in%20that%20file%20is%20based%20on%20a%20bad%20agent%20behavior">My AI Adoption Journey</a>, at “Better implicit prompting.” “Each line in that file is based on a bad agent behavior”</li>
<li id="cite-c0404">Hamel Husain and Shreya Shankar, blog, <a href="https://hamel.dev/blog/posts/evals-faq/#:~:text=people%20need%20to%20observe%20the%20LLM%27s%20behavior%20in%20order%20to%20properly%20externalize%20their%20requirements">AI Evals: Everything You Need to Know</a>, at “Today’s prompt engineering tricks might become obsolete.” “people need to observe the LLM's behavior in order to properly externalize their requirements.”</li>
<li id="cite-c0411">smol-ai (Shawn “swyx” Wang), repository, <a href="https://github.com/smol-ai/developer#:~:text=simply%20add%20to%20the%20prompt%20as%20they%20discover%20underspecified%20parts%20of%20the%20prompt">smol-ai/developer</a>, at “simply add to the prompt as they discover.” “simply add to the prompt as they discover underspecified parts of the prompt”</li>
</ol>

<p id="next-action">Write the missing decision from one recent agent misunderstanding where its next attempt will receive it.</p>
