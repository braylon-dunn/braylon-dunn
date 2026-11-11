# Storykeeper AI — oral-history storytelling experiment

**Newly authored portfolio sample (November 2026).** This is an experiment outside my usual UI engineering work: helping families preserve stories behind photos and videos using an AI-assisted interview editor.

It turns a text interview into a family-history exhibit with a summary, dated memories, verbatim quotes, follow-up interview questions and uncertainty notes. The program validates that quoted passages exist in the original interview. Every AI output still needs human review.

## Run (Python 3.10+, standard library only)

```bash
# Reproducible offline preview (rule-based, not an AI result)
python storykeeper-ai/storykeeper.py storykeeper-ai/examples/interview.txt --offline --output story.md

# Actual AI generation (OpenAI API access required)
export OPENAI_API_KEY=your-key
python storykeeper-ai/storykeeper.py storykeeper-ai/examples/interview.txt --output story.md

# Unit tests
python -m unittest discover -s storykeeper-ai/tests -v
```

PowerShell: `$env:OPENAI_API_KEY="your-key"`.

The example interview is entirely fictional. Do not send private family stories to an API without consent. The offline mode is a deterministic demonstration and explicitly not AI-generated. A source-verbatim quote check does not guarantee factual correctness; review all details with the storyteller.

## Project files
- `storykeeper.py`: interview-to-story CLI, AI integration and validation
- `examples/interview.txt`: fictional source notes
- `tests/test_storykeeper.py`: source-grounding checks
