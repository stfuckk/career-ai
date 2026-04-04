from pydantic import BaseModel, Field, model_validator


class CareerTestScoresRequest(BaseModel):
    people_score: int = Field(ge=0, le=12)
    research_score: int = Field(ge=0, le=12)
    practical_score: int = Field(ge=0, le=12)
    aesthetic_score: int = Field(ge=0, le=12)
    extreme_score: int = Field(ge=0, le=12)
    economic_score: int = Field(ge=0, le=12)

    @model_validator(mode='after')
    def validate_total_score(self):
        total = (
            self.people_score
            + self.research_score
            + self.practical_score
            + self.aesthetic_score
            + self.extreme_score
            + self.economic_score
        )
        if total != 24:
            raise ValueError('Sum of all scores must be equal to 24')
        return self


class CareerTestSubmitAnonymousRequest(BaseModel):
    scores: CareerTestScoresRequest


class CategoryScoreRead(BaseModel):
    key: str
    title: str
    score: int
    label: str


class RecommendedProfessionRead(BaseModel):
    name: str
    rationale: str
    fit_score: int = Field(ge=0, le=100)


class VacancyRead(BaseModel):
    hh_vacancy_id: str
    title: str
    employer_name: str | None = None
    area_name: str | None = None
    alternate_url: str
    salary_from: int | None = None
    salary_to: int | None = None
    currency: str | None = None
    snippet: dict | None = None


class CareerTestPreviewRead(BaseModel):
    attempt_token: str
    methodology_slug: str
    preview_summary: str
    scores: list[CategoryScoreRead]
    dominant_categories: list[str]
    registration_required: bool = True


class AboutUserRead(BaseModel):
    age: str
    experience: str
    strengths: list[str]
    education: str


class CareerFitRead(BaseModel):
    title: str
    summary: str
    professions: list[str]


class DevelopmentRecommendationsRead(BaseModel):
    title: str
    summary: str
    steps: list[str]


class CareerPathStep(BaseModel):
    title: str
    skills_to_learn: list[str]
    experience_required: str
    hh_search_query: str


class CareerPathRead(BaseModel):
    current_position: str
    steps: list[CareerPathStep]


class CareerTestResultRead(BaseModel):
    created_at: str
    updated_at: str
    attempt_token: str
    methodology_slug: str
    preview_summary: str
    best_specialty: str
    scores: list[CategoryScoreRead]
    dominant_categories: list[str]
    about_user: AboutUserRead
    career_fit: CareerFitRead
    development_recommendations: DevelopmentRecommendationsRead
    career_path: CareerPathRead | None = None
    vacancies: list[VacancyRead] = []
