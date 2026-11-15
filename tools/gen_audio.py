# usage: python gen_audio2.py <page.html> <outDir>
# Builds <outDir>/boy/<catId>.json and <outDir>/teacher/<catId>.json: {display text: "data:audio/mpeg;base64,..."}
import asyncio, base64, json, sys, os, re
import edge_tts

page, out = sys.argv[1], sys.argv[2]
html = open(page, encoding="utf-8").read()
cats = json.loads(html.split("/*DATA*/")[1].split("/*END*/")[0])
common = json.loads(html.split("/*COMMON*/")[1].split("/*ENDCOMMON*/")[0])

# (voice, rate, pitch): livelier than default, a bit faster and brighter
VOICES = {
    "boy":     ("fr-FR-EloiseNeural", "+6%", "-6Hz"),
    "teacher": ("fr-FR-VivienneMultilingualNeural", "+4%", "+6Hz"),
}
CHICK = ("fr-FR-EloiseNeural", "+8%", "+28Hz")

def ask(cat, w):
    return ("Où est " + w + " ?") if cat["ask"] == "ou" else ("Montre-moi : " + w)

def spoken(text):
    # short pause before the target word and an excited ending, so it sounds less flat
    m = re.match(r"^Montre-moi : (.*)$", text)
    if m:
        w = m.group(1).rstrip()
        if not w.endswith(("?", "!")): w += " !"
        return "Montre-moi... " + w
    m = re.match(r"^Où est (.*) \?$", text)
    if m:
        return "Où est... " + m.group(1) + " ?"
    return text

def jobs_for(narrator):
    jobs = {}
    for c in cats:
        lst = []
        for it in c["items"]:
            if c.get("type") == "move":
                lst.append((it[0], it[0], CHICK)); continue
            lst.append((it[0], it[0], narrator))
            q = ask(c, it[0]); lst.append((q, spoken(q), narrator))
        jobs[c["id"]] = lst
    lst = [(c["fr"], c["fr"], narrator) for c in cats]
    lst += [(t, t, narrator) for t in common["teacher"]]
    lst += [("m:" + t, t, CHICK) for t in common["chick"]]
    jobs["common"] = lst
    return jobs

sem = asyncio.Semaphore(8)
async def synth(text, voice):
    name, rate, pitch = voice
    tries = [(text, name), (text, name), (text, "fr-FR-DeniseNeural"), (text.rstrip(" !?.") + ".", "fr-FR-DeniseNeural")]
    async with sem:
        for attempt, (tx, nm) in enumerate(tries):
            try:
                buf = b""
                async for ch in edge_tts.Communicate(tx, nm, rate=rate, pitch=pitch).stream():
                    if ch["type"] == "audio": buf += ch["data"]
                if buf: return buf
            except Exception:
                pass
            await asyncio.sleep(1 + attempt)
        raise RuntimeError("failed: " + text)

async def main():
    total = 0
    for vname, voice in VOICES.items():
        d = os.path.join(out, vname); os.makedirs(d, exist_ok=True)
        for fid, lst in jobs_for(voice).items():
            uniq = {k: (t, v) for k, t, v in lst}
            res = await asyncio.gather(*(synth(t, v) for t, v in uniq.values()))
            data = {k: "data:audio/mpeg;base64," + base64.b64encode(b).decode() for k, b in zip(uniq.keys(), res)}
            s = json.dumps(data, ensure_ascii=False)
            open(os.path.join(d, fid + ".json"), "w", encoding="utf-8").write(s)
            total += len(s); print(vname, fid, len(uniq), round(len(s) / 1e6, 2), "MB", flush=True)
    print("total MB", round(total / 1e6, 1))
asyncio.run(main())
