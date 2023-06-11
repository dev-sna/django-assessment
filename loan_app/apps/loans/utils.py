def get_exam_result(quiz_data, user_answers):
    total_score = len(quiz_data["questions"])
    achieved_score = 0
    for user_answer in user_answers:
        question = list(
            filter(
                lambda x: str(x["id"]) == str(user_answer["question"]),
                quiz_data["questions"],
            )
        )[0]
        answer_ids = [
            answer["id"] for answer in question["answers"] if answer["is_correct"]
        ]
        if answer_ids == user_answer["selected_answers"]:
            achieved_score += 1

    return {"achieved_score": achieved_score, "total_score": total_score}
