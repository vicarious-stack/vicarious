# Chapter 11: The Test

**Loomed** over the office floor as the logistics server sputtered and the monitoring dashboard flashed red. The sterile whine of the air‑conditioning system hummed in the background, a low, constant drone that seemed to pulse in time with Kiran’s heartbeat. The faint smell of burnt plastic escaped from the server rack as a cooling fan struggled, a metallic tang that cut through the more comforting scent of fresh coffee drifting from the nearby break‑room where a lone espresso machine hissed, releasing a rich, bitter aroma.

Kiran’s palms were slick with sweat, the cool metal of the keyboard beneath his fingers providing a grounding contrast. He could feel the **vibration** of his phone tucked in his pocket, a faint buzz that he deliberately ignored. The **rain** outside the office windows hammered against the glass in a rapid **drum‑roll**, each drop striking with a sharp *plink* that reverberated through the concrete structure.

**Saw** the error log flood the terminal: a cascade of deadlock warnings, transaction IDs tangled in a web of waiting locks. The console output scrolled rapidly, a sea of red text that seemed to pulse like a warning beacon.

```
2026-06-22 14:35:12.845 ERROR [deadlock] Transaction 0x7f3c1c8c waiting for lock on table `orders`
2026-06-22 14:35:12.846 ERROR [deadlock] Transaction 0x7f3c1c9d waiting for lock on table `inventory`
2026-06-22 14:35:12.847 ERROR [deadlock] Deadlock detected, rolling back transaction 0x7f3c1c8c
```

The **visual** of the red warnings was stark against the dark background, their intensity a stark reminder of the fragility of the system. Kiran inhaled deeply, the scent of **petrichor** seeping through the slightly ajar window, mixing with the metallic tinge of the server room.

He initiated his **box‑breathing** routine, a technique taught by Dr. Meera. He inhaled for four counts, held for four, exhaled for six, and held again for two. The **auditory** cue of his own breath filled the small space, the **tactile** sensation of his chest expanding and contracting providing a rhythmic anchor against the chaos.

**Focused** on the deadlock, Kiran opened the database schema. The `orders` table and `inventory` table both used the default **READ‑COMMITTED** isolation level, allowing overlapping transactions to lock rows in a way that could cause a circular wait.

He wrote a quick **SQL** snippet to alter the isolation level for the critical transaction:

```sql
-- Set the transaction isolation to SERIALIZABLE to prevent deadlocks
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Perform order insert and inventory update atomically
INSERT INTO orders (id, item, qty, status) VALUES (?,?,?,?);
UPDATE inventory SET stock = stock - ? WHERE item_id = ?;
COMMIT;
```

The **tactile** click of the mouse as he executed the script was satisfying, a small physical affirmation amidst the digital turmoil. The server responded with a clean **green** success message, the red warnings replaced by a quiet **OK**.

**Rohan Desai** arrived at Kiran’s desk, his coat damp from the rain, breath visible in the cool air of the server room. "The logistics API is still throwing a race condition in the async calls," he said, voice low but urgent. "The prototype crashes when two requests hit the same endpoint simultaneously."

Kiran opened the prototype code, a Node.js service handling asynchronous API calls with **async/await**. He inspected the function handling the request:

```javascript
async function processOrder(order) {
  const result = await externalService.call(order);
  await db.save(order);
  return result;
}
```

He realized that the **externalService** call could return after the **db.save** had already been invoked elsewhere, leading to an inconsistent state. He added a **mutex** using the `async-mutex` library to serialize access to the critical section.

```javascript
const { Mutex } = require('async-mutex');
const orderMutex = new Mutex();

async function processOrder(order) {
  return orderMutex.runExclusive(async () => {
    const result = await externalService.call(order);
    await db.save(order);
    return result;
  });
}
```

The **visual** feedback of the IDE turned green, the **auditory** chime sounding like a small triumph. He ran a stress test, spawning 200 concurrent requests. The console printed:

```
[INFO] All 200 requests completed successfully – no race condition detected.
```

**Priya Sharma** stepped in, notebook in hand, her pen scratching across the page. "Your fix solves the technical bug, but have you considered the user‑experience impact?" she asked, her tone analytical yet compassionate. "If the system queues every request, latency could increase, affecting the perception of reliability."

Kiran paused, feeling a **weight** lift from his shoulders at the acknowledgement of the broader picture. He glanced at the **digital ledger** notebook, the leather warm from his hands, the pages thick and slightly rough.

```json
{
  "screen_time": 210,
  "unlocks": 25,
  "focus": 6,
  "code": 210
}
```

*"210 min – simultaneous crisis resolved. Physical: server rack heat, rain drumroll, coffee aroma, cool keyboard. Mental: focused breathing, problem‑solving flow, collaborative pressure.*"

Below the JSON block, he scribbled a concise reflection:

> *Two systems failed at once – the logistics deadlock and the prototype race condition. By applying both physiological regulation (box breathing) and systematic code safeguards (transaction isolation, mutex), I turned chaos into controlled order. The real test was not just fixing code but maintaining composure.*

**Adi** sent a flurry of memes to the team's Slack channel, each a cartoon of a hamster on a wheel labeled “Production”. Kiran smiled despite himself, the brief humor cutting through the lingering tension. He replied with a short, supportive message: "Good work, team. Let’s keep the momentum."

The **rain** outside softened, each drop now a gentle **tap‑tap** against the window, a calming metronome that mirrored his breath. The **scent** of wet pavement mixed with the **sweetness** of a distant street vendor selling roasted peanuts, creating a layered olfactory backdrop.

**Returned** to his desk, Kiran opened a new terminal window and scripted a monitoring hook that would alert the team if any deadlock warning resurfaced within the next 24 hours.

```bash
#!/bin/bash
# Simple watchdog for deadlock warnings
while true; do
  if grep -q "Deadlock detected" /var/logs/server.log; then
    echo "[ALERT] Deadlock detected! notifying team..."
    curl -X POST -H "Content-Type: application/json" -d '{"text":"Deadlock alert!"}' https://hooks.slack.com/services/...
    sleep 3600
  else
    sleep 300
  fi
done
```

He saved the script as `deadlock_watchdog.sh`, made it executable, and added it to the crontab for nightly runs.

**Exhaled** slowly, the breath carrying the lingering scent of rain, coffee, and the faint metallic odor of the server. He felt a profound sense of **presence**, the sensory details of the moment anchoring him in the now.

*Thus concluded Chapter 11, a night of simultaneous crises that tested both the mind and the machinery, resolved through disciplined breathing, precise code, and collaborative insight.*

---

**Digital Ledger Entry (Chapter 11)**

```json
{
  "screen_time": 210,
  "unlocks": 25,
  "focus": 6,
  "code": 210
}
```
