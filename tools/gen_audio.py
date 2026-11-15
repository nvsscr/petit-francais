# usage: python tools/gen_audio.py petit-francais.html audio/clips.json [--all]
# Records every phrase of the /*DATA*/ block, all with the same young voice (the app uses sound effects for everything else).
# Output: one JSON {text: "data:audio/mpeg;base64,..."}. Clips that already exist are kept unless --all is given.
import asyncio, base64, json, sys, os
import edge_tts

page, out = sys.argv[1], sys.argv[2]
redo = "--all" in sys.argv
html = open(page, encoding="utf-8").read()
cats = json.loads(html.split("/*DATA*/")[1].split("/*END*/")[0])
common = json.loads(html.split("/*COMMON*/")[1].split("/*ENDCOMMON*/")[0])

BOY = ("fr-FR-EloiseNeural", "+6%", "-6Hz")
TEACHER = ("fr-FR-VivienneMultilingualNeural", "+2%", "+4Hz")
CHICK = ("fr-FR-EloiseNeural", "+8%", "+28Hz")
VOICE = {"b": BOY, "t": BOY, "m": BOY}   # one voice for everything

jobs = {}
for c in cats:
    for it in c["items"]:
        jobs[it[0]] = VOICE[c["v"]]

old = {}
if os.path.exists(out) and not redo:
    old = json.load(open(out, encoding="utf-8"))

sem = asyncio.Semaphore(8)
async def synth(text, voice):
    name, rate, pitch = voice
    async with sem:
        for attempt, nm in enumerate([name, name, "fr-FR-DeniseNeural"]):
            try:
                buf = b""
                async for ch in edge_tts.Communicate(text, nm, rate=rate, pitch=pitch).stream():
                    if ch["type"] == "audio": buf += ch["data"]
                if buf: return buf
            except Exception:
                pass
            await asyncio.sleep(1 + attempt)
        raise RuntimeError("failed: " + text)

async def main():
    todo = [k for k in jobs if k not in old]
    res = await asyncio.gather(*(synth(k, jobs[k]) for k in todo))
    clips = {k: old[k] for k in jobs if k in old}
    for k, b in zip(todo, res):
        clips[k] = "data:audio/mpeg;base64," + base64.b64encode(b).decode()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    s = json.dumps(clips, ensure_ascii=False)
    open(out, "w", encoding="utf-8").write(s)
    print("clips", len(clips), "new", len(todo), round(len(s) / 1e6, 2), "MB")
asyncio.run(main())
