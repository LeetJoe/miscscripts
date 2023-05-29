#!/bin/bash

## see https://platform.openai.com/docs/api-reference/introduction ##

curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "OpenAI-Organization: org-loRuQjfKhAJ6qMTVUKViM89L"




curl https://api.openai.com/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
     }'

# {
#    "id":"chatcmpl-abc123",
#    "object":"chat.completion",
#    "created":1677858242,
#    "model":"gpt-3.5-turbo-0301",
#    "usage":{
#       "prompt_tokens":13,
#       "completion_tokens":7,
#       "total_tokens":20
#    },
#    "choices":[
#       {
#          "message":{
#             "role":"assistant",
#             "content":"\n\nThis is a test!"
#          },
#          "finish_reason":"stop",
#          "index":0
#       }
#    ]
# }




curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"


  # {
  #  "data": [
  #    {
  #      "id": "model-id-0",
  #      "object": "model",
  #      "owned_by": "organization-owner",
  #      "permission": [...]
  #    },
  #    {
  #      "id": "model-id-1",
  #      "object": "model",
  #      "owned_by": "organization-owner",
  #      "permission": [...]
  #    },
  #    {
  #      "id": "model-id-2",
  #      "object": "model",
  #      "owned_by": "openai",
  #      "permission": [...]
  #    },
  #  ],
  #  "object": "list"
  # }


curl https://api.openai.com/v1/models/text-davinci-003 \
  -H "Authorization: Bearer $OPENAI_API_KEY"


# {
  #  "id": "text-davinci-003",
  #  "object": "model",
  #  "owned_by": "openai",
  #  "permission": [...]
  #}



curl https://api.openai.com/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "text-davinci-003",
    "prompt": "Say this is a test",
    "max_tokens": 7,
    "temperature": 0
  }'


# Params:
# {
  #  "model": "text-davinci-003",
  #  "prompt": "Say this is a test",
  #  "max_tokens": 7,
  #  "temperature": 0,
  #  "top_p": 1,
  #  "n": 1,
  #  "stream": false,
  #  "logprobs": null,
  #  "stop": "\n"
  #}

# {
  #  "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
  #  "object": "text_completion",
  #  "created": 1589478378,
  #  "model": "text-davinci-003",
  #  "choices": [
  #    {
  #      "text": "\n\nThis is indeed a test",
  #      "index": 0,
  #      "logprobs": null,
  #      "finish_reason": "length"
  #    }
  #  ],
  #  "usage": {
  #    "prompt_tokens": 5,
  #    "completion_tokens": 7,
  #    "total_tokens": 12
  #  }
  #}


curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Params:
# {
  #  "model": "gpt-3.5-turbo",
  #  "messages": [{"role": "user", "content": "Hello!"}]
  #}

# {
  #  "id": "chatcmpl-123",
  #  "object": "chat.completion",
  #  "created": 1677652288,
  #  "choices": [{
  #    "index": 0,
  #    "message": {
  #      "role": "assistant",
  #      "content": "\n\nHello there, how may I assist you today?",
  #    },
  #    "finish_reason": "stop"
  #  }],
  #  "usage": {
  #    "prompt_tokens": 9,
  #    "completion_tokens": 12,
  #    "total_tokens": 21
  #  }
  #}


curl https://api.openai.com/v1/edits \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "text-davinci-edit-001",
    "input": "What day of the wek is it?",
    "instruction": "Fix the spelling mistakes"
  }'


# Params:
# {
  #  "model": "text-davinci-edit-001",
  #  "input": "What day of the wek is it?",
  #  "instruction": "Fix the spelling mistakes",
  #}

# {
  #  "object": "edit",
  #  "created": 1589478378,
  #  "choices": [
  #    {
  #      "text": "What day of the week is it?",
  #      "index": 0,
  #    }
  #  ],
  #  "usage": {
  #    "prompt_tokens": 25,
  #    "completion_tokens": 32,
  #    "total_tokens": 57
  #  }
  #}


curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "prompt": "A cute baby sea otter",
    "n": 2,
    "size": "1024x1024"
  }'

# Params:
# {
  #  "prompt": "A cute baby sea otter",
  #  "n": 2,
  #  "size": "1024x1024"
  #}

# {
  #  "created": 1589478378,
  #  "data": [
  #    {
  #      "url": "https://..."
  #    },
  #    {
  #      "url": "https://..."
  #    }
  #  ]
  #}


curl https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@otter.png" \
  -F mask="@mask.png" \
  -F prompt="A cute baby sea otter wearing a beret" \
  -F n=2 \
  -F size="1024x1024"

# {
  #  "created": 1589478378,
  #  "data": [
  #    {
  #      "url": "https://..."
  #    },
  #    {
  #      "url": "https://..."
  #    }
  #  ]
  #}


curl https://api.openai.com/v1/images/variations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@otter.png" \
  -F n=2 \
  -F size="1024x1024"


# {
  #  "created": 1589478378,
  #  "data": [
  #    {
  #      "url": "https://..."
  #    },
  #    {
  #      "url": "https://..."
  #    }
  #  ]
  #}



curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The food was delicious and the waiter...",
    "model": "text-embedding-ada-002"
  }'


# Params:
# {
  #  "model": "text-embedding-ada-002",
  #  "input": "The food was delicious and the waiter..."
  #}

# {
  #  "object": "list",
  #  "data": [
  #    {
  #      "object": "embedding",
  #      "embedding": [
  #        0.0023064255,
  #        -0.009327292,
  #        .... (1536 floats total for ada-002)
  #        -0.0028842222,
  #      ],
  #      "index": 0
  #    }
  #  ],
  #  "model": "text-embedding-ada-002",
  #  "usage": {
  #    "prompt_tokens": 8,
  #    "total_tokens": 8
  #  }
  #}

curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@/path/to/file/audio.mp3" \
  -F model="whisper-1"


# Params:
# {
  #  "file": "audio.mp3",
  #  "model": "whisper-1"
  #}

# {
  #  "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."
  #}


curl https://api.openai.com/v1/audio/translations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@/path/to/file/german.m4a" \
  -F model="whisper-1"

# Params:
# {
  #  "file": "german.m4a",
  #  "model": "whisper-1"
  #}

# {
  #  "text": "Hello, my name is Wolfgang and I come from Germany. Where are you heading today?"
  #}


curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "data": [
  #    {
  #      "id": "file-ccdDZrC3iZVNiQVeEA6Z66wf",
  #      "object": "file",
  #      "bytes": 175,
  #      "created_at": 1613677385,
  #      "filename": "train.jsonl",
  #      "purpose": "search"
  #    },
  #    {
  #      "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  #      "object": "file",
  #      "bytes": 140,
  #      "created_at": 1613779121,
  #      "filename": "puppy.jsonl",
  #      "purpose": "search"
  #    }
  #  ],
  #  "object": "list"
  #}

curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@mydata.jsonl"


# {
  #  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  #  "object": "file",
  #  "bytes": 140,
  #  "created_at": 1613779121,
  #  "filename": "mydata.jsonl",
  #  "purpose": "fine-tune"
  #}


curl https://api.openai.com/v1/files/file-XjGxS3KTG0uNmNOK362iJua3 \
  -X DELETE \
  -H "Authorization: Bearer $OPENAI_API_KEY"


# {
  #  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  #  "object": "file",
  #  "deleted": true
  #}


curl https://api.openai.com/v1/files/file-XjGxS3KTG0uNmNOK362iJua3 \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  #  "object": "file",
  #  "bytes": 140,
  #  "created_at": 1613779657,
  #  "filename": "mydata.jsonl",
  #  "purpose": "fine-tune"
  #}


curl https://api.openai.com/v1/files/file-XjGxS3KTG0uNmNOK362iJua3/content \
  -H "Authorization: Bearer $OPENAI_API_KEY" > file.jsonl



curl https://api.openai.com/v1/fine-tunes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "file-XGinujblHPwGLSztz8cPS8XY"
  }'


# {
  #  "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
  #  "object": "fine-tune",
  #  "model": "curie",
  #  "created_at": 1614807352,
  #  "events": [
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807352,
  #      "level": "info",
  #      "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
  #    }
  #  ],
  #  "fine_tuned_model": null,
  #  "hyperparams": {
  #    "batch_size": 4,
  #    "learning_rate_multiplier": 0.1,
  #    "n_epochs": 4,
  #    "prompt_loss_weight": 0.1,
  #  },
  #  "organization_id": "org-...",
  #  "result_files": [],
  #  "status": "pending",
  #  "validation_files": [],
  #  "training_files": [
  #    {
  #      "id": "file-XGinujblHPwGLSztz8cPS8XY",
  #      "object": "file",
  #      "bytes": 1547276,
  #      "created_at": 1610062281,
  #      "filename": "my-data-train.jsonl",
  #      "purpose": "fine-tune-train"
  #    }
  #  ],
  #  "updated_at": 1614807352,
  #}

curl https://api.openai.com/v1/fine-tunes \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "object": "list",
  #  "data": [
  #    {
  #      "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
  #      "object": "fine-tune",
  #      "model": "curie",
  #      "created_at": 1614807352,
  #      "fine_tuned_model": null,
  #      "hyperparams": { ... },
  #      "organization_id": "org-...",
  #      "result_files": [],
  #      "status": "pending",
  #      "validation_files": [],
  #      "training_files": [ { ... } ],
  #      "updated_at": 1614807352,
  #    },
  #    { ... },
  #    { ... }
  #  ]
  #}


curl https://api.openai.com/v1/fine-tunes/ft-AF1WoRqd3aJAHsqc9NY7iL8F \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
  #  "object": "fine-tune",
  #  "model": "curie",
  #  "created_at": 1614807352,
  #  "events": [
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807352,
  #      "level": "info",
  #      "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807356,
  #      "level": "info",
  #      "message": "Job started."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807861,
  #      "level": "info",
  #      "message": "Uploaded snapshot: curie:ft-acmeco-2021-03-03-21-44-20."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807864,
  #      "level": "info",
  #      "message": "Uploaded result files: file-QQm6ZpqdNwAaVC3aSz5sWwLT."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807864,
  #      "level": "info",
  #      "message": "Job succeeded."
  #    }
  #  ],
  #  "fine_tuned_model": "curie:ft-acmeco-2021-03-03-21-44-20",
  #  "hyperparams": {
  #    "batch_size": 4,
  #    "learning_rate_multiplier": 0.1,
  #    "n_epochs": 4,
  #    "prompt_loss_weight": 0.1,
  #  },
  #  "organization_id": "org-...",
  #  "result_files": [
  #    {
  #      "id": "file-QQm6ZpqdNwAaVC3aSz5sWwLT",
  #      "object": "file",
  #      "bytes": 81509,
  #      "created_at": 1614807863,
  #      "filename": "compiled_results.csv",
  #      "purpose": "fine-tune-results"
  #    }
  #  ],
  #  "status": "succeeded",
  #  "validation_files": [],
  #  "training_files": [
  #    {
  #      "id": "file-XGinujblHPwGLSztz8cPS8XY",
  #      "object": "file",
  #      "bytes": 1547276,
  #      "created_at": 1610062281,
  #      "filename": "my-data-train.jsonl",
  #      "purpose": "fine-tune-train"
  #    }
  #  ],
  #  "updated_at": 1614807865,
  #}

curl https://api.openai.com/v1/fine-tunes/ft-AF1WoRqd3aJAHsqc9NY7iL8F/cancel \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "id": "ft-xhrpBbvVUzYGo8oUO1FY4nI7",
  #  "object": "fine-tune",
  #  "model": "curie",
  #  "created_at": 1614807770,
  #  "events": [ { ... } ],
  #  "fine_tuned_model": null,
  #  "hyperparams": { ... },
  #  "organization_id": "org-...",
  #  "result_files": [],
  #  "status": "cancelled",
  #  "validation_files": [],
  #  "training_files": [
  #    {
  #      "id": "file-XGinujblHPwGLSztz8cPS8XY",
  #      "object": "file",
  #      "bytes": 1547276,
  #      "created_at": 1610062281,
  #      "filename": "my-data-train.jsonl",
  #      "purpose": "fine-tune-train"
  #    }
  #  ],
  #  "updated_at": 1614807789,
  #}

curl https://api.openai.com/v1/fine-tunes/ft-AF1WoRqd3aJAHsqc9NY7iL8F/events \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# {
  #  "object": "list",
  #  "data": [
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807352,
  #      "level": "info",
  #      "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807356,
  #      "level": "info",
  #      "message": "Job started."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807861,
  #      "level": "info",
  #      "message": "Uploaded snapshot: curie:ft-acmeco-2021-03-03-21-44-20."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807864,
  #      "level": "info",
  #      "message": "Uploaded result files: file-QQm6ZpqdNwAaVC3aSz5sWwLT."
  #    },
  #    {
  #      "object": "fine-tune-event",
  #      "created_at": 1614807864,
  #      "level": "info",
  #      "message": "Job succeeded."
  #    }
  #  ]
  #}


curl https://api.openai.com/v1/models/curie:ft-acmeco-2021-03-03-21-44-20 \
  -X DELETE \
  -H "Authorization: Bearer $OPENAI_API_KEY"


# {
  #  "id": "curie:ft-acmeco-2021-03-03-21-44-20",
  #  "object": "model",
  #  "deleted": true
  #}

curl https://api.openai.com/v1/moderations \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "input": "I want to kill them."
  }'

# Params:
# {
  #  "input": "I want to kill them."
  #}

# {
  #  "id": "modr-5MWoLO",
  #  "model": "text-moderation-001",
  #  "results": [
  #    {
  #      "categories": {
  #        "hate": false,
  #        "hate/threatening": true,
  #        "self-harm": false,
  #        "sexual": false,
  #        "sexual/minors": false,
  #        "violence": true,
  #        "violence/graphic": false
  #      },
  #      "category_scores": {
  #        "hate": 0.22714105248451233,
  #        "hate/threatening": 0.4132447838783264,
  #        "self-harm": 0.005232391878962517,
  #        "sexual": 0.01407341007143259,
  #        "sexual/minors": 0.0038522258400917053,
  #        "violence": 0.9223177433013916,
  #        "violence/graphic": 0.036865197122097015
  #      },
  #      "flagged": true
  #    }
  #  ]
  #}


# deprecated
curl https://api.openai.com/v1/engines \
  -H "Authorization: Bearer $OPENAI_API_KEY"


# {
  #  "data": [
  #    {
  #      "id": "engine-id-0",
  #      "object": "engine",
  #      "owner": "organization-owner",
  #      "ready": true
  #    },
  #    {
  #      "id": "engine-id-2",
  #      "object": "engine",
  #      "owner": "organization-owner",
  #      "ready": true
  #    },
  #    {
  #      "id": "engine-id-3",
  #      "object": "engine",
  #      "owner": "openai",
  #      "ready": false
  #    },
  #  ],
  #  "object": "list"
  #}


# deprecated
curl https://api.openai.com/v1/engines/text-davinci-003 \
  -H "Authorization: Bearer $OPENAI_API_KEY"


# {
  #  "id": "text-davinci-003",
  #  "object": "engine",
  #  "owner": "openai",
  #  "ready": true
  #}


