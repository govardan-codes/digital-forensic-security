# ==========================================================
# services/test_engine.py — Test Creation & Question Linking
# ==========================================================
from datetime import datetime
from models import db
from models.test import Test, TestQuestion
from models.skill import Skill
from models.question import Question
from services.ai_question import generate_questions_for_skill


def create_ai_test_for_student(student_id, skill_ids):
    """Create one unified test and attach AI-generated questions (5 per skill)."""
    if len(skill_ids) != 5:
        raise ValueError("Exactly 5 skills must be selected.")

    # 1️⃣ create Test entry
    test = Test(
        student_id=student_id,
        started_at=datetime.utcnow(),
        duration_secs=1800,  # 30 min
        total_questions=25,
        status="in_progress",
    )
    db.session.add(test)
    db.session.commit()

    # 2️⃣ generate + link questions per skill
    for skill_id in skill_ids:
        skill = Skill.query.get(skill_id)
        if not skill:
            continue

        questions = generate_questions_for_skill(skill)
        for q in questions:
            # normalize answer to single-letter if possible
            ans = str(q.get("answer", "")).strip().upper()
            if ans not in ["A", "B", "C", "D"]:
                ans = ans[:1] or "A"

            new_q = Question(
                skill_id=skill.id,
                question_text=q.get("question", "").strip(),
                option_a=q["options"][0] if len(q["options"]) > 0 else "",
                option_b=q["options"][1] if len(q["options"]) > 1 else "",
                option_c=q["options"][2] if len(q["options"]) > 2 else "",
                option_d=q["options"][3] if len(q["options"]) > 3 else "",
                correct_option=ans,
                source="ai",
            )
            db.session.add(new_q)
            db.session.flush()  # get new_q.id

            link = TestQuestion(test_id=test.id, question_id=new_q.id)
            db.session.add(link)

        db.session.commit()

    return test
