import json
D=json.load(open('beats.json')); B=D['beats']; STYLE=D['style']
for i,x in enumerate(B,1): x['n']=i; x['w']=len(x['text'].split())
# 1) group split halves of the same original beat
G=[]
for x in B:
    if G and G[-1][-1]['parent']==x['parent']: G[-1].append(x)
    else: G.append([x])
# 2) merge adjacent same-type groups (<=25 words ~10s) until <=146 clips, smallest first
LIMIT=140
words=lambda g:sum(x['w'] for x in g)
while len(G)>LIMIT:
    cands=[(words(G[i])+words(G[i+1]),i) for i in range(len(G)-1)
           if G[i][0]['t']==G[i+1][0]['t'] and words(G[i])+words(G[i+1])<=25]
    if not cands: break
    _,i=min(cands); G[i:i+2]=[G[i]+G[i+1]]
def motion(cam):
    c=cam.lower()
    if 'orbit' in c: return "smooth motion-controlled orbit around the subject at constant speed"
    if 'push-in' in c or 'dolly-in' in c: return "slow, steady push-in toward the subject"
    if 'pull-back' in c: return "slow, steady pull-back revealing more of the scene"
    if 'dolly' in c or 'pan' in c: return "slow lateral dolly/pan at constant speed"
    if 'tracking' in c or 'chase' in c: return "camera tracks alongside at matching speed, holding the framing steady with gentle float"
    if 'rack focus' in c: return "locked-off camera with a slow rack focus between elements"
    if 'pov' in c: return "first-person view with a very slight natural sway"
    return "locked-off camera with a barely perceptible slow drift"
TYPE_NOTE={
 "archival":"Animate as a still archival photograph: subtle film-grain flicker, faint gate weave and a slow digital push-in only; figures stay almost still.",
 "map":"Animate as a clean motion-graphics map: the route line draws on smoothly, the aircraft icon glides along it; no camera shake.",
}
out=[f"# Video Prompts — Why Did the Spirit of St. Louis Have No Front Window?",
     f"{len(G)} video prompts covering all {len(B)} image prompts (each clip uses its image prompt(s) as start/end frames). Visual style: **{STYLE}**.",""]
for k,g in enumerate(G,1):
    first,last=g[0],g[-1]; w=words(g); dur=max(3,round(w/2.5))
    ids=f"Image Prompt {first['n']}" if len(g)==1 else f"Image Prompts {first['n']}–{last['n']}"
    seg=' '.join(x['text'] for x in g)
    beats_desc=[]
    for j,x in enumerate(g):
        beats_desc.append(f"{'Opens on' if j==0 else 'Then transitions (seamless camera move, no hard cut) to'} {x['subject']}, {x['env_r']}; {x['action']} — camera: {x['camera']}")
    subj_motion='; '.join(beats_desc)
    note=TYPE_NOTE.get(first['t'],"Keep aircraft geometry rigid and accurate: no morphing, no extra wings, struts or engines; propeller blur only when the engine is running.")
    prompt=(f"{STYLE}, {dur}-second clip. {subj_motion}. Camera motion: {motion(first['camera'])}. "
            f"Lighting: {first['light_r']}. Mood: {first['mood']}. {note} "
            f"Smooth, slow, cinematic pacing; physically plausible motion; no on-screen text, no watermark, no sound; 16:9, 24 fps.")
    out+=[f"## Video Prompt {k} — {ids} (~{dur}s)",
          f"**[Script Segment]** \"{seg}\"","",
          f"**Video Prompt:** {prompt}","",
          f"- **Duration:** ~{dur}s ({w} words)",
          f"- **Camera Motion:** {motion(first['camera'])}",
          f"- **Subject Motion:** {'; '.join(x['action'] for x in g)}",""]
open('spirit-of-st-louis-video-prompts.md','w').write('\n'.join(out))
print(len(G),"video prompts; max dur",max(round(words(g)/2.5) for g in G))
