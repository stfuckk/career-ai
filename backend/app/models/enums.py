from enum import StrEnum


class SexEnum(StrEnum):
    male = 'male'
    female = 'female'


class EducationLevelEnum(StrEnum):
    school = 'school'
    college = 'college'
    bachelor = 'bachelor'
    master = 'master'
    specialist = 'specialist'
    other = 'other'
