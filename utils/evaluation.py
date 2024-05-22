def static_essay_assessment_criteria():
    return """
    1. Thesis clarity: Clear and focused thesis statement that addresses the essay prompt
    2. Analysis Depth: In-depth analysis of the topic with supporting evidence
    3. Organization: Well structured and logically organized essay
    4. Writing Clarity: Clear and concise writing with proper grammar and punctuation
    5. Conclusion
    """


def evaluate_essay(content):
    # Additional logic for essay evaluation if needed
    return content


def evaluate_other(content):
    # Additional logic for other types of documents if needed
    return content


def get_rubric_metrics(subject):
    # Define rubric metrics for different subjects
    rubric_metrics = {
        "math": ["accuracy", "completeness", "reasoning"],
        "science": ["accuracy", "experimental design", "conclusion"],
        "essay-writing": [
            "1. Thesis Clarity: Clear and focused thesis statement that addresses the essay prompt\n",
            "2. Analysis Depth: In-depth analysis of the topic with supporting evidence\n",
            "3. Organization: Well structured and logically organized essay\n",
            "4. Writing Clarity:  Clear and concise writing with proper grammar and punctuation\n",
            "5. Conclusion"],
        # Add more subjects and metrics as needed
    }
    return '\n'.join(rubric_metrics[subject])
