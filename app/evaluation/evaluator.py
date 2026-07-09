import json
from app.pipeline.query_pipeline import run_text_query
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from datasets import Dataset
from app.config.settings import GROQ_API_KEY


def load_test_questions(file_path: str) -> list:
    """
    Load test questions from JSON file
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def run_evaluation():
    print("\n" + "="*60)
    print("STARTING RAGAS EVALUATION")
    print("="*60)

    # Setup Groq LLM
    groq_llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        max_tokens=2048,
        temperature=0.1
    )

    # Setup Embeddings
    hf_embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Wrap for RAGAS
    ragas_llm = LangchainLLMWrapper(groq_llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(hf_embeddings)

    # Initialize metrics
    metrics = [
        Faithfulness(llm=ragas_llm),
        AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
        ContextPrecision(llm=ragas_llm),
        ContextRecall(llm=ragas_llm)
    ]

    # Load from file
    questions_path = "./app/evaluation/test_questions.json"
    test_questions = load_test_questions(questions_path)
    print(f"Loaded {len(test_questions)} questions!")

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for i, item in enumerate(test_questions):
        print(f"\n{i+1}/{len(test_questions)}: {item['question']}")
        result = run_text_query(item["question"])
        answer = result["answer"]
        chunks = result["retrieved_chunks"]

        questions.append(item["question"])
        answers.append(answer)
        ground_truths.append(item["ground_truth"])

        context_list = [
            chunk["content"][:300]
            for chunk in chunks
        ] if chunks else ["No context"]
        contexts.append(context_list)

        print(f"Answer ready!")

    # Create dataset
    eval_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

    # Run evaluation
    print("\nRunning RAGAS...")
    results = evaluate(
        eval_dataset,
        metrics=metrics,
        raise_exceptions=False
    )

    # Get scores
    df = results.to_pandas()
    faithfulness = float(df['faithfulness'].mean())
    answer_relevancy = float(df['answer_relevancy'].mean())
    context_precision = float(df['context_precision'].mean())
    context_recall = float(df['context_recall'].mean())
    overall = (
        faithfulness +
        answer_relevancy +
        context_precision +
        context_recall
    ) / 4

    print("\n" + "="*60)
    print("RAGAS RESULTS")
    print("="*60)
    print(f"Faithfulness:      {faithfulness:.4f}")
    print(f"Answer Relevancy:  {answer_relevancy:.4f}")
    print(f"Context Precision: {context_precision:.4f}")
    print(f"Context Recall:    {context_recall:.4f}")
    print(f"Overall Score:     {overall:.4f}")
    print("="*60)

    # Save results
    results_dict = {
        "faithfulness": faithfulness,
        "answer_relevancy": answer_relevancy,
        "context_precision": context_precision,
        "context_recall": context_recall,
        "overall_score": overall
    }

    with open("./app/evaluation/results.json", 'w') as f:
        json.dump(results_dict, f, indent=4)

    print("\n Saved to results.json")
    return results_dict


if __name__ == "__main__":
    run_evaluation()