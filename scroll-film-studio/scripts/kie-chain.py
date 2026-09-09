#!/usr/bin/env python3
"""kie-chain.py <storyboard.json> <outdir> — generate ONE continuous film, not a reel.

WHY THIS SCRIPT EXISTS. Every failed film in this project failed the same way: a
clip was asked to travel too far, so the model teleported instead of moving, and
the seam checks still passed because chaining makes seams match by construction.
Two things fix that, and both are enforced here rather than left to a prompt:

  1. KEYFRAMES ARE A CHAIN. Keyframe N+1 is generated with keyframe N as an image
     reference, serially. The world — palette, light, materials, scale — is
     inherited rather than re-invented, so consecutive stills belong to one place.

  2. CLIPS ARE PINNED AT BOTH ENDS. Veo 3.1's FIRST_AND_LAST_FRAMES_2_VIDEO takes
     [keyframe N, keyframe N+1] and must LAND on the second one. A start-frame-only
     model (Seedance i2v, Higgsfield) is free to drift anywhere and then cut back;
     that freedom is the bug. Both-ends-pinned removes it structurally.

Storyboard JSON:
  { "name": "amber",
    "aspect": "16:9",
    "style": "<one sentence appended to every keyframe prompt — the look>",
    "keyframes": [ {"id":"kf1","prompt":"..."}, ... ],          # N stills
    "clips":     [ {"id":"c1","prompt":"...", "duration":8}, ...] # N-1 moves
  }

Resumable: anything already on disk is not regenerated. Safe to re-run after a
crash or a 503 without paying twice.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

KEY = (os.environ.get("KIE_API_KEY")
       or (open(os.path.expanduser("~/.config/kie/key")).read().strip()
           if os.path.exists(os.path.expanduser("~/.config/kie/key")) else None))
if not KEY:
    sys.exit("ERROR: no Kie key (KIE_API_KEY or ~/.config/kie/key)")

# Kie's WAF returns 403 to anything without a browser User-Agent, GETs included.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
HDRS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "User-Agent": UA}

JOBS_CREATE = "https://api.kie.ai/api/v1/jobs/createTask"
JOBS_INFO = "https://api.kie.ai/api/v1/jobs/recordInfo"
VEO_GEN = "https://api.kie.ai/api/v1/veo/generate"
VEO_INFO = "https://api.kie.ai/api/v1/veo/record-info"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"


def req(url, body=None, method=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=HDRS,
                               method=method or ("POST" if data else "GET"))
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return json.loads(f.read())


def fetch(url, out, timeout=600):
    """Kie's CDN 403s anything without a browser UA — urlretrieve won't do."""
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=timeout) as src, open(out, "wb") as f:
        f.write(src.read())


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def credits():
    try:
        return req("https://api.kie.ai/api/v1/chat/credit")["data"]
    except Exception:
        return -1


# ---------------------------------------------------------------- keyframes
def gen_still(prompt, ref_url, aspect, out):
    """One still. ref_url anchors it to the previous frame's world."""
    inp = {"prompt": prompt, "aspect_ratio": aspect,
           "resolution": "2K", "output_format": "png"}
    if ref_url:
        inp["image_urls"] = [ref_url]
    d = req(JOBS_CREATE, {"model": "nano-banana-2", "input": inp})
    if d.get("code") != 200:
        raise RuntimeError(f"createTask: {d.get('msg')}")
    tid = d["data"]["taskId"]
    for _ in range(120):
        time.sleep(4)
        s = req(f"{JOBS_INFO}?taskId={tid}")["data"]
        if s.get("state") == "success":
            url = json.loads(s["resultJson"])["resultUrls"][0]
            fetch(url, out)
            return url
        if s.get("state") == "fail":
            raise RuntimeError(f"still failed: {s.get('failMsg')}")
    raise TimeoutError("still timed out")


def upload(path, folder):
    """Publish a LOCAL file (a real brand logo, a supplied plate) to Kie's CDN.

    Not used for keyframes. A 2K PNG base64-encodes to ~10MB and the uploader
    resets the connection partway through — and it is redundant anyway, because
    Nano Banana 2 results are already served from Kie's own CDN. Use the URL the
    generator hands back; only round-trip through here for files that started
    life on this machine.
    """
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    ext = os.path.splitext(path)[1].lstrip(".") or "png"
    d = req(UPLOAD, {"base64Data": f"data:image/{ext};base64,{b64}",
                     "uploadPath": f"kieai/343103/{folder}",
                     "fileName": os.path.basename(path)}, timeout=300)
    if not d.get("success"):
        raise RuntimeError(f"upload: {d}")
    return d["data"]["downloadUrl"]


# --------------------------------------------------------------------- clips
def gen_clip(prompt, first_url, last_url, dur, aspect, out):
    d = req(VEO_GEN, {"prompt": prompt, "imageUrls": [first_url, last_url],
                      "model": "veo3",
                      "generationType": "FIRST_AND_LAST_FRAMES_2_VIDEO",
                      "aspect_ratio": aspect, "duration": dur,
                      "resolution": "1080p"})
    if d.get("code") != 200:
        raise RuntimeError(f"veo/generate: {d.get('msg')}")
    tid = d["data"]["taskId"]
    log(f"    task {tid}")
    for i in range(180):  # up to 30 min; a 1080p 8s clip runs 2-5 min
        time.sleep(10)
        s = req(f"{VEO_INFO}?taskId={tid}")["data"]
        flag = s.get("successFlag")
        if flag == 1:
            # `response` comes back as a dict on some jobs and a JSON string on
            # others; both carry resultUrls. Accept either, and fall back to the
            # top level rather than crashing after the clip is already paid for.
            r = s.get("response") or {}
            if isinstance(r, str):
                r = json.loads(r)
            url = (r.get("resultUrls") or s.get("resultUrls") or [None])[0]
            if not url:
                raise RuntimeError(f"no resultUrls in success response: "
                                   f"{json.dumps(s)[:400]}")
            fetch(url, out)
            return
        if flag in (2, 3):
            raise RuntimeError(f"clip failed: {s.get('errorMessage')}")
        if i % 6 == 0:
            log(f"    ...{i * 10}s")
    raise TimeoutError("clip timed out")


# ---------------------------------------------------------------------- main
def main():
    sb = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    kfd, cld = os.path.join(out, "keyframes"), os.path.join(out, "clips")
    os.makedirs(kfd, exist_ok=True)
    os.makedirs(cld, exist_ok=True)
    aspect = sb.get("aspect", "16:9")
    style = sb.get("style", "")
    kfs, clips = sb["keyframes"], sb["clips"]
    assert len(clips) == len(kfs) - 1, \
        f"{len(kfs)} keyframes need {len(kfs)-1} clips, got {len(clips)}"

    log(f"{sb['name']}: {len(kfs)} keyframes -> {len(clips)} clips. "
        f"credits {credits()}")

    urls, prev = [], None
    for i, k in enumerate(kfs):
        p = os.path.join(kfd, f"{k['id']}.png")
        um = os.path.join(kfd, f"{k['id']}.url")
        if os.path.exists(um):                       # resume
            u = open(um).read().strip()
            log(f"  {k['id']} cached")
        else:
            log(f"  {k['id']} generating"
                f"{' (chained from ' + kfs[i-1]['id'] + ')' if prev else ''}")
            u = gen_still(f"{k['prompt']} {style}".strip(), prev, aspect, p)
            open(um, "w").write(u)
        urls.append(u)
        prev = u

    for i, c in enumerate(clips):
        p = os.path.join(cld, f"{i:02d}-{c['id']}.mp4")
        if os.path.exists(p) and os.path.getsize(p) > 100000:
            log(f"  {c['id']} cached")
            continue
        log(f"  {c['id']} {kfs[i]['id']}->{kfs[i+1]['id']} "
            f"({c.get('duration', 8)}s)")
        gen_clip(c["prompt"], urls[i], urls[i + 1],
                 c.get("duration", 8), aspect, p)
        log(f"    done {os.path.getsize(p)//1024}KB  credits {credits()}")

    # Concat. Re-encode rather than stream-copy: the clips come back with
    # matching params today, but a silent container mismatch produces a file
    # that plays for the first clip and then stalls, which reads as a "bug in
    # the website" hours later.
    # ABSOLUTE paths: ffmpeg resolves concat entries relative to the LIST FILE's
    # directory, not the cwd, so a relative path that looks correct from where
    # you launched the script silently becomes gen/gen/clips/... and the whole
    # assembly dies after every clip has already been paid for.
    lst = os.path.join(out, "concat.txt")
    with open(lst, "w") as f:
        for i, c in enumerate(clips):
            p = os.path.abspath(os.path.join(cld, "%02d-%s.mp4" % (i, c["id"])))
            f.write("file '%s'\n" % p)
    master = os.path.join(out, "master.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", lst, "-an", "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", master], check=True)
    log(f"master {os.path.getsize(master)//1024//1024}MB")
    log(f"NEXT: extract frames, then run continuity-gate.sh — do NOT build "
        f"until it passes.")


if __name__ == "__main__":
    main()
