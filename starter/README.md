# Starter files

The two practice apps, as they are at the start of the labs. Copy them to
`~/practice`, where the lessons expect them:

```bash
mkdir -p ~/practice
cp -R hello-ai hello-model ~/practice/
```

| Folder | Used from | What it is |
|---|---|---|
| `hello-ai` | Lesson 2 | A small FastAPI service with `/health` and `/predict`. Its "model" is a keyword counter, so the image stays small and builds in seconds. |
| `hello-model` | Lesson 5 | A FastAPI service that runs a real sentiment model, [DistilBERT SST-2](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) (Apache-2.0, about 268 MB), on the CPU. |

Neither folder has a `Containerfile`. Writing it is the lab.

`hello-ai/.env` holds a fake API key on purpose. Part of Lesson 2's lab is
making sure that file never ends up inside your image.
