import requests 
import html
import random

class GameManager:
    def __init__(self):
        self.base_url = "https://opentdb.com/api.php"

    def get_question(self, game_type, category, difficulty):
        params = {
            "amount": 1,
            "type": "boolean" if game_type == "1" else "multiple",
            "difficulty": difficulty.lower()
        }

        category_mapping = {
            "General Knowledge": 9,
            "Entertainment: Books": 10,
            "Entertainment: Film": 11,
            "Entertainment: Music": 12,
            "Entertainment: Video Games": 15,
            "Science: Computers": 18,
            "Geography": 22,
            "History": 23,
            "Computer Science": 18,  # MC only
            "Logical Reasoning": 0    # No category or MC only fallback
        }

        # For True/False game mode, restrict to categories with available TF questions
        allowed_tf_categories = [9, 11, 12, 15, 18, 22, 23]

        if game_type == "1":  # True/False
            if category in category_mapping and category_mapping[category] in allowed_tf_categories:
                params["category"] = category_mapping[category]
            else:
                # Fallback to General Knowledge if selected category not supported for TF
                params["category"] = 9
        else:
            # Multiple Choice categories as usual, skip if category id is 0 (invalid)
            if category in category_mapping and category_mapping[category] != 0:
                params["category"] = category_mapping[category]

        response = requests.get(self.base_url, params=params)
        data = response.json()

        if data["response_code"] != 0 or len(data["results"]) == 0:
            return {
                "category": category,
                "difficulty": difficulty,
                "question": "No questions available.",
                "Option A": "",
                "Option B": "",
                "Option C": "",
                "Option D": "",
                "answer": ""
            }

        result = data["results"][0]
        question_text = html.unescape(result["question"])
        correct_answer = html.unescape(result["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in result["incorrect_answers"]]

        if game_type == "1":  # True/False
            return {
                "category": result["category"],
                "difficulty": result["difficulty"],
                "question": question_text,
                "answer": correct_answer
            }
        else:
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)
            option_labels = ['A', 'B', 'C', 'D']
            option_dict = {f"Option {label}": option for label, option in zip(option_labels, options)}
            correct_option = option_labels[options.index(correct_answer)]

            return {
                "category": result["category"],
                "difficulty": result["difficulty"],
                "question": question_text,
                **option_dict,
                "answer": correct_option
            }

    def check_answer(self, user_answer, correct_answer):
        return user_answer.strip().lower() == correct_answer.strip().lower()

    def adjust_difficulty(self, streak):
        if streak >= 5:
            return 'hard'
        elif streak >= 3:
            return 'medium'
        else:
            return 'easy'
