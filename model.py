from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = 'users' # Corrected typo: __tablename__

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique= True, index = True)

    hashed_password = Column(String) # Changed from password_hash for consistency

    is_active = Column(Boolean, default = True)
    is_superuser = Column(Boolean, default = False)

    employees = relationship('Employee', back_populates = 'user') # Corrected relationship name

    def verify_password(self, password:str): # Corrected method name
        return bcrypt.verify(password, self.hashed_password)



class Project(Base):
    __tablename__  = 'project'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    description = Column(String, nullable = True)

    employees = relationship('Employee', secondary = 'employee_project_mapping', back_populates = 'projects')

#create a model named Employee to map for our employees table in database
class Employee(Base):

    __tablename__ = 'employees'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    email = Column(String, index = True, unique = True)
    is_active = Column(Boolean, default = True)
    user_id = Column(Integer, ForeignKey('users.id')) # Added foreign key for User relationship

    user = relationship('User', back_populates = 'employees') # Define relationship to User
    projects = relationship('Project', secondary = 'employee_project_mapping', back_populates ='employees')

#Many to many relationship mapping
employee_project_mapping = Table(
    'employee_project_mapping',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key = True),
    Column('project_id', Integer, ForeignKey('project.id'), primary_key = True),
)
