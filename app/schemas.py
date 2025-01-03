from pydantic import BaseModel
from typing import List, Optional

#user section
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str # Added password field for user creation

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

# Employee section
class EmployeeBase(BaseModel):
    name: str
    email: str

class EmployeeCreate(EmployeeBase):
    user: UserCreate # Expect nested UserCreate for creating a user along with employee

class EmployeeUpdate(EmployeeBase):
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    is_active: bool
    projects: List["Project"] = []
    user: Optional[User] = None # Added user relationship

    class Config:
        orm_mode = True

# Projects section
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    employees: List["Employee"] = [] # Added forward reference quotes

    class Config:
        orm_mode = True

# Call model_rebuild() after defining all models with forward references
Employee.model_rebuild()
Project.model_rebuild()
User.model_rebuild()