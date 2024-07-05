# PyData Manchester Talk - 30th July

Planning on giving a talk at PyData Manchester on July 30th. 

### Description of Talk

Having worked helping businesses adopt LLM workflows such as RAG pipelines and function calling, a common challenge is benchmarking and measuring how well the application is performing. This talk aims to explore some of the existing open-source tooling to help with this and look at some best practices when building out such applications.

### Preperation Notes - 05/07

[Haystack Tutorial](https://haystack.deepset.ai/tutorials/35_evaluating_rag_pipelines) - Evaluating RAG Pipeline 

- Can split evaluating RAG Pipelines into two steps. Evaluating the retrieval and evaluating the generation
- Referenced evaluation frameworks: [DeepEval](https://github.com/confident-ai/deepeval), [RAGAS](https://github.com/explodinggradients/ragas) and [UpTrain](https://github.com/uptrain-ai/uptrain)
- Uses the PubMed QA dataset
- Metrics used for the evaluation in the tutorial:
    - Document mean reciprocal rank: it checks at what rank ground truth labels appear in the list of retrieved docs (requires GroundTruth)
    - Semantic search similarity:  (requires GroundTruth) uses a fine tuned LLM to give the semantic similarity of a predicted answer and the ground truth label
    - Faithfulness: uses an LLM to evaluate whether a generated answer can be inferred from a given context (doesn’t require GroundTruth)



### Useful Resources
 
- [Benchmarking Haystack Pipelines](https://haystack.deepset.ai/blog/benchmarking-haystack-pipelines)
- [Evaluating RAG Pipelines](https://haystack.deepset.ai/tutorials/35_evaluating_rag_pipelines)