# evalrag/core/eval.py
"""
Evaluation of RAG system has tow main parts:
1. Component wise:
    1. Retrieval:
        1. Context Recall
        2. Context Percision
        3. Context Relevancy
        4. Context Entity Recall
    
    2. Generation:
        1. Faithfulness
        2. Answer Relevancy

        
2. End to End:
    1. Answer Semantic Similarity
    2. Answer Correctness

    
"""

"""
Steps to evaluate RAG answers:
    1.  Prepare source documents and index them using a vector database.
    2. Setup agents(e.g., Mixtral("mistralai/Mixtral-8x7B-Instruct-v0.1")) for question generation, retrieval, and answer generation.
    3.  Setup critique agents (e.g., GPT-4) for evaluating the generated answers.
    4.  For each user question:
        1. Generate sub-questions if needed.
        2. Retrieve relevant contexts from the vector database.
        3. Generate answers using the retrieved contexts.
        4. Evaluate the generated answers using the critique agents.

1. Use a judge model (e.g., GPT-4) to evaluate the generated answer against the question and retrieved contexts.
2. Define evaluation criteria such as correctness, faithfulness, and relevance.
3. For each criterion, create prompts that guide the judge model to provide scores and feedback.
4. Aggregate the scores from different criteria to get an overall evaluation score.


"""


from typing import List, Dict, Any


class Evaluator:

    """
    Evaluation helper for assessing RAG answers.

    Responsibilities:
      - Use a judge model to evaluate answers.
      - Compute metrics like correctness, faithfulness, and relevance.
      - Aggregate scores based on configured weights.
    Typical usage:
      1. `evaluate_answer(question, answer, contexts)` to get evaluation scores.
    Args:
        config: Configuration object or mapping used by evaluation routines.
    """

    def __init__(self, config) -> None:

        """
        Initialize the Evaluator.

        Args:
            config: Configuration object or mapping used by evaluation processes.

        The provided `config` is stored on the instance for later use by
        other methods in this class.
        """
        self.config = config
    
    def cost_correctness(self):
        pass
    
    def cost_faithfulness(self):
        pass
    
    def cost_relevance(self):
        pass 

    def evaluate_answer(self, question: str, answer: str, contexts: List[Dict]) -> Dict[str, Any]:
        """
        Evaluate the given `answer` to `question` using `contexts`.
        Args:
            question: The user question text.
            answer: The generated answer text.
            contexts: List of context chunks used to generate the answer.
        Returns:
            A dict containing evaluation scores and feedback.
        """
        # placeholder implementation
        scores = {
            "correctness": 4,
            "faithfulness": 5,
            "relevance": 4,
        }
        feedback = "The answer is mostly correct and faithful to the context."
        result = {
            "scores": scores,
            "feedback": feedback,
        }
        return result