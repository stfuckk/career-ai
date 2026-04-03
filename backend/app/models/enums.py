from enum import StrEnum


class EducationLevel(StrEnum):
    school = "school"
    college = "college"
    bachelor = "bachelor"
    master = "master"
    gap_year = "gap_year"
    self_education = "self_education"
    other = "other"


class SessionStatus(StrEnum):
    created = "created"
    competency_questions_ready = "competency_questions_ready"
    answers_received = "answers_received"
    recommendations_ready = "recommendations_ready"
    failed = "failed"


class QuestionStage(StrEnum):
    onboarding = "onboarding"
    competency = "competency"


class QuestionInputType(StrEnum):
    boolean = "boolean"
    single_choice = "single_choice"
    multi_choice = "multi_choice"
    text = "text"
    number = "number"
    scale = "scale"
