from pydantic import BaseModel


class MethodologyQuestionRead(BaseModel):
    number: int
    text: str
    options: dict[str, str]


class MethodologyCategoryRead(BaseModel):
    key: str
    column: int
    title: str
    description: str


class InterpretationRangeRead(BaseModel):
    from_score: int
    to_score: int
    label: str


class TestMethodologyRead(BaseModel):
    slug: str
    version: str
    title: str
    source_pdf_name: str | None = None
    questions: list[MethodologyQuestionRead]
    categories: list[MethodologyCategoryRead]
    interpretation_ranges: list[InterpretationRangeRead]
