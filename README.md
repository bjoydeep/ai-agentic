# ai-agentic
Explorting agentic workflows

Inspiration from:
- https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io
- https://github.com/langchain-ai/langgraph/tree/c3f6c58e13c09dc4870cb1748f2646dd72444151/examples



## What do you need to run
1. Clone this repo
1. create the .env file by copying `env-sample` and updating the values
1. Setup venv
    - `cd to the repo dir`
    - run: 
        ```
        python -m venv .aiagt
        source .aiagt/bin/activate
        pip install -r requirements.txt
        ```
    - run :`which python` and this show that python is being used from the venv directory
    - after all work is done, to exit the venv, just run: `deactivate`
1. To run Juyter notebook    

python -m ipykernel install --user --name=.aiagt

1. To run the Python app

python -m app.compose.app1.supervisor.entry

## Background

As all of you know, answering a simple question like `What is the health of my retail banking application` can be at best very labor intensive and at worse very complex. Let us take a look at what does it usually means to be able to answer this:

1. First, what constitutes the application `retail banking`? If you just don't happen to know the answer, it can be tricky. And in modern days, applications can be spread across clusters. Now of course we do assume certain kubernetes best practices around labeling/owner-referencing etc to be followed. _If these best practices are not followed, there is still a way out. We do not address this here yet. Hint: Use a human-in-loop pattern._
1. Now once we know the application composition, we need to do several things:
    1. Has anything changed around these? As we all know, most failures have a recent change lurking behind it.
    1. Are the pods consuming abnormal amount of CPU or memory or crashing looping?
    1. Are there errors emitting in the pod logs?
    1. What about alerts related to the application?
    1. Are there any application SLOs defined?
    1. Is the cluster on which the application running healthy?
1. And then all of this needs to be neatly summarized to the binary answer the human brain is looking for.

In short, looking at different screens and bringing this all together in the brain is at best very labor intensive and at worse very complex. 

### Agentic Pattern

The `Agentic Pattern` offers a great promise here:
Though there are number of patterns, we start experimenting with the [supervisor pattern](https://github.com/langchain-ai/langgraph/blob/c3f6c58e13c09dc4870cb1748f2646dd72444151/examples/multi_agent/agent_supervisor.ipynb).
1. There is the promise / study: [GPT-3.5 (zero shot) was 48.1% correct. GPT-4 (zero shot) does better at 67.0%. However, the improvement from GPT-3.5 to GPT-4 is dwarfed by incorporating an iterative agent workflow. Indeed, wrapped in an agent loop, GPT-3.5 achieves up to 95.1%. ](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io)
1. Breakdown the question into smaller tasks. If the task can be designed to be generic enough - then these could be reused across other questions. This is not only a well known software practice, this is a very well known engineering practice. 
1. As long the tasks confirm to the Agent API of the framework, we have the full liberty on how to design them. If there are deterministic tasks that need to be there - it can be incorporated. If there are other Algorithms that needs to be called like Causal Reasoning etc - it can be incorporated again. We have a reasonable leeway to fend for hallucinations (in reality its a trade off).
1. And finally all of this can be summarized to provide a result that can be consumed by a human without too much cognitive burden.
1. These tasks are probably delivered by different teams in an enterprise. These allows this to be scaled quickly.

## Structure of this Repo
```
app/
│
├── agents/
│   ├── __init__.py
│   ├── appdetect.py
│   ├── appchangedetect.py
│   ├── appmetric.py
│   ├── applog.py
│   ├── appalert.py
│   ├── appslo.py
│   ├── clusterhealth.py
│   ├── ........
├── tools/
│   ├── __init__.py
│   ├── appdef.py
│   ├── .....
├── compose/
│   ├── __init__.py
│   ├── app1/
│       └── __init__.py
│       └── supervisor/
│           └── entry.py
│           └── graph.py
│           └── supervisor.py
│           └── __init__.py
├── config/
│   ├── __init__.py
│   └── config.py
└── __init__.py
│
notebooks/
│   ├── agent-experiment-1.ipynb
│   ├── ........
```

1. `notebooks` contain the notebooks used to test concepts out.
1. `app` contains the agents and tools and the application that is being composed of it. 
1. Conceptually:
    1. The `agents` are like generic microservices with `tools`. 
    1. These can be developed across different teams - `agents` and `tools` are potentially reusable across different applications. 
    1. Each team uses them and creates their applications under `compose`. 
    1. In the example above, the application is called `app1`. 
    1. Likewise there could be `app2` etc that uses different compostion of agents.






