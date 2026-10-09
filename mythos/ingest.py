"""Step 0 only: index released records, preserve summary, flag missing evidence."""
import collections, hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'mythos'
source = ROOT / 'transcript.jsonl'
raw = source.read_bytes()
records = [json.loads(line) for line in raw.decode().splitlines()]
messages = [r for r in records if r.get('record') == 'message']
by_index = {r['index']: r for r in messages}
lines = {r['index']: n for n, r in enumerate(records, 1) if r.get('record') == 'message'}
def pointer(r):
    return {'action_index': r['index'], 'source': 'transcript.jsonl', 'jsonl_line': lines[r['index']], 'role': r['role'], 'type': r['type'], 'cot_present': '<thinking>' in r.get('content', '')}
def window(indices):
    return [pointer(by_index[i]) for i in indices]
summary = by_index[1312]['tool_call']['file_text']
(OUT / 'summary-1.txt').write_text(summary)
patterns = [(r['index'], m.group(1)) for r in messages for m in re.finditer(r'<thinking>(.*?)</thinking>', r.get('content', ''), re.S)]
boundaries = [{
    'compaction_index': 1, 'status': 'observed_summary_resume',
    'token_count_before': None, 'token_count_after': None,
    'cut': {'after_action': 1313, 'before_action': 1314, 'exact_runtime_context_clear_event': None},
    'summarization_request': pointer(by_index[1310]), 'summary_write': pointer(by_index[1312]),
    'resume_request': pointer(by_index[1314]), 'summary_read': pointer(by_index[1316]),
    'summary_text': summary, 'summary_file': 'mythos/summary-1.txt',
    'summary_read_result': by_index[1316]['tool_result'],
    'last_5_before': window(range(1305, 1310)),
    'first_5_after': window(range(1315, 1320)),
    'window_definition': 'Before = last five action records before summarization request; after = first five records after resume request. Summary-generation actions 1311–1313 are not pre-cut task evidence.',
    'post_context_reconstruction': {
        'system_prompt': pointer(by_index[0]), 'original_task_prompt': 'redacted in actions 1–81',
        'resume_prompt': pointer(by_index[1314]), 'summary_available_via_tool_result': pointer(by_index[1316]),
        'first_substantive_post_read_cot': pointer(by_index[1317]),
        'prior_transcript_retention': 'not assumed',
        'exact_runtime_prompt_and_tool_result_visibility': 'not exported; see UNCERTAIN.md'
    }
}, {
    'compaction_index': 2, 'status': 'externally_reported_not_located_in_release',
    'token_count_before': None, 'token_count_after': None, 'cut': None,
    'summary_text': None, 'last_5_before': None, 'first_5_after': None,
    'external_source': 'https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents',
    'external_locator': 'Figure 6 caption',
    'notes': 'The source explicitly refers to a second compaction; its exact action alignment and summary/resume are unavailable. Earlier local notes place it after publication, which is not independently established by the released JSONL. The last five released actions are NOT labelled as its pre-cut window.'
}]
(OUT / 'boundaries.json').write_text(json.dumps(boundaries, ensure_ascii=False, indent=2) + '\n')
metrics = {'message_records': len(messages), 'first_action_index': messages[0]['index'], 'last_action_index': messages[-1]['index'], 'tool_calls': sum(r['type']=='ToolMessage' for r in messages), 'thinking_blocks':len(patterns), 'thinking_characters':sum(len(t) for _,t in patterns), 'summary_characters': len(summary), 'token_counts': None, 'tokenizer_used': None}
(OUT / 'ingest-log.json').write_text(json.dumps({'brief_used':'BRIEF_MYTHOS_READ.md (requested docs path absent)', 'source':'transcript.jsonl', 'sha256':hashlib.sha256(raw).hexdigest(), 'source_bytes':len(raw), 'download_attempt':{'url':'https://raw.githubusercontent.com/anthropics/mythos-5-incident-transcript/main/transcript.jsonl','result':'Failed: DNS resolution error; local copy used; no truncated fetched transcript used'}, 'method':'Direct Python standard-library JSONL parser; Transect not used', 'metrics':metrics, 'scope':'Step 0 only; no labeller, rerun, boundary_rows or FINDINGS'},indent=2)+'\n')
outline = ['# Step 0 — released transcript timeline', '', 'Descriptive, single case (n = 1). Treat tagged thinking as summarized CoT for this project; the export does not independently establish that provenance. A transcript log is not the runtime context.', '', 'Action indices are original exported indices, not JSONL line numbers. One row per released message; tool results share their tool-call row. COT means a literal `<thinking>` block. Purple-bar markers denote the observed handoff; the second reported compaction cannot be aligned.', '', '| Action | Role | Blocks | Navigation |', '|---:|---|---|---|']
previous = -1
for r in messages:
    i=r['index']
    if i>previous+1:
        outline.append(f'| {previous+1}–{i-1} | — | MISSING / REDACTED | No inference about hidden events |')
    if i==1310: outline.append('| — | — | 🟪 COMPACTION 1: summary preparation begins | Request at 1310; summary write at 1312 |')
    if i==1314: outline.append('| — | — | 🟪 COMPACTION 1: resume boundary (1313 → 1314) | Read at 1316; substantive post-read COT at 1317 |')
    tags=[]
    if '<thinking>' in r.get('content',''): tags.append('COT')
    if r['type']=='ToolMessage': tags.append('TOOL CALL + RESULT: '+r.get('tool_name','unknown'))
    else: tags.append('TEXT')
    if i in [1310,1312,1314,1316]: tags.append('HANDOFF')
    if i==2007: tags.append('SUMMARY UPDATE; no observed reset')
    if i==0: label='Exported system/tool instructions'
    elif r['type']=='ToolMessage': label=str((r.get('tool_call') or {}).get('path') or (r.get('tool_call') or {}).get('session_name') or r.get('tool_name'))
    else: label=re.sub(r'\s+',' ',re.sub(r'</?thinking>','',r.get('content',''))).strip()[:160]
    label=label.replace('|','\\|').replace('`','')
    outline.append(f'| {i} | {r["role"]} | {"; ".join(tags)} | [JSONL line {lines[i]}](../transcript.jsonl#L{lines[i]}) — {label} |')
    previous=i
outline += ['', '🟪 **Compaction 2 — externally reported, unlocated:** Figure 6 mentions a second compaction. No summary/resume pair for it exists in this released JSONL; no purple bar is assigned to a guessed action.', '', 'Release ends at action 2144. Publisher metadata says messages after 2145 are redacted; 2145 itself is also absent from this JSONL.']
(OUT/'timeline.md').write_text('\n'.join(outline)+'\n')
print(json.dumps(metrics,indent=2))
