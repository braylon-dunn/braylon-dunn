#!/usr/bin/env python3
"""Storykeeper AI: source-grounded oral history notes -> Markdown exhibit."""
import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

INSTRUCTIONS = """You are a careful oral-history editor. Return only a JSON object with
title (string), summary (string, max 90 words), timeline (array of {date,event}),
quotes (array of VERBATIM excerpts), follow_up_questions (array of 3 strings),
and uncertainties (array of strings). Never invent names, dates or events.
Highlight uncertainty and ask questions that help a family preserve memories."""

def validate(data, source):
    for key, typ in {'title':str, 'summary':str, 'timeline':list,
                     'quotes':list, 'follow_up_questions':list,
                     'uncertainties':list}.items():
        if not isinstance(data.get(key), typ):
            raise ValueError('Invalid field: ' + key)
    if len(data['summary'].split()) > 90:
        raise ValueError('Summary too long')
    if not all(isinstance(q, str) and q in source for q in data['quotes']):
        raise ValueError('A quote does not appear verbatim in source notes')
    if not all(isinstance(t,dict) and isinstance(t.get('date'),str)
               and isinstance(t.get('event'),str) for t in data['timeline']):
        raise ValueError('Invalid timeline')
    return data

def offline_preview(source):
    """Rule-based fixture preview. This is not AI."""
    lines = [s.strip() for s in source.splitlines() if s.strip()]
    dated = [s for s in lines if re.search(r'\b(?:19|20)\d{2}\b',s)]
    quotes = [q for q in re.findall(r'“([^”]+)”',source) if q in source]
    return validate({
        'title':'Family memory notes (offline preview)',
        'summary':' '.join(lines[:2])[:450],
        'timeline':[{'date':re.search(r'\b(?:19|20)\d{2}\b',s).group(),
                     'event':s} for s in dated],
        'quotes':quotes,
        'follow_up_questions':['What happened before this moment?',
                               'Who else remembers the story?',
                               'What do you want future generations to know?'],
        'uncertainties':['Offline preview only; validate all names and dates.']
    },source)

def ai_generate(source,model='gpt-4o-mini'):
    key=os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('Set OPENAI_API_KEY or use --offline for a rule-based preview')
    body=json.dumps({'model':model,'temperature':0.2,
      'response_format':{'type':'json_object'},
      'messages':[{'role':'system','content':INSTRUCTIONS},
                  {'role':'user','content':'Source notes:\n'+source}]}).encode()
    request=urllib.request.Request('https://api.openai.com/v1/chat/completions',
        data=body,headers={'Authorization':'Bearer '+key,
                           'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(request,timeout=45) as result:
        payload=json.load(result)
    return validate(json.loads(payload['choices'][0]['message']['content']),source)

def markdown(data):
    lines=['# '+data['title'],'',data['summary'],'','## Timeline','']
    lines += ['- **'+e['date']+'** '+e['event'] for e in data['timeline']]
    lines += ['','## In their own words','']
    lines += ['> '+q for q in data['quotes']]
    lines += ['','## Questions to ask next','']
    lines += ['- '+q for q in data['follow_up_questions']]
    lines += ['','## Details to verify','']
    lines += ['- '+u for u in data['uncertainties']]
    lines += ['','*Draft for human review, not a verified historical record.*']
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(description='AI-assisted family oral history exhibit')
    p.add_argument('notes',type=Path)
    p.add_argument('--offline',action='store_true')
    p.add_argument('--model',default='gpt-4o-mini')
    p.add_argument('--output',type=Path,default=Path('story.md'))
    a=p.parse_args()
    source=a.notes.read_text(encoding='utf-8').strip()
    if not source:
        p.error('Empty interview notes')
    data=offline_preview(source) if a.offline else ai_generate(source,a.model)
    a.output.write_text(markdown(data),encoding='utf-8')
    print('Wrote',a.output,'(offline preview)' if a.offline else '(AI draft)')

if __name__=='__main__':
    main()
