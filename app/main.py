from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from passlib.hash import bcrypt  
from db import engine, get_db
import model
import schemas
model.Base.metadata.create_all(bind=engine)
app = FastAPI(title="QuickML Projects", version="0.1.0")
@app.post('/users/', response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    db_user = model.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.post("/employees/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(employee.user.password)
    db_user = model.User(username=employee.user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_employee = model.Employee(name=employee.name, email=employee.email, user_id=db_user.id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(model.Employee).options(joinedload(model.Employee.user)).offset(skip).limit(limit).all()
    return employees
@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(model.Employee).filter(model.Employee.id == employee_id).options(joinedload(model.Employee.projects), joinedload(model.Employee.user)).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
@app.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee_in: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(model.Employee).filter(model.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_data = employee_in.dict(exclude_unset=True)
    for key, value in employee_data.items():
        setattr(db_employee, key, value)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
@app.delete("/employees/{employee_id}", status_code=200, response_model=dict) 
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(model.Employee).filter(model.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
@app.post('/projects', response_model=schemas.Project, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = model.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
@app.get('/projects/', response_model=List[schemas.Project])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(model.Project).offset(skip).limit(limit).all()
    return projects
@app.get('/projects/{project_id}', response_model=schemas.Project)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    project = db.query(model.Project).filter(model.Project.id == project_id).options(joinedload(model.Project.employees)).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
@app.put('/projects/{project_id}', response_model=schemas.Project)
def update_project(project_id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(model.Project).filter(model.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project_in.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return project
@app.delete('/projects/{project_id}', status_code=200, response_model=dict) 
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(model.Project).filter(model.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}
@app.post('/employees/{employee_id}/projects/{project_id}', response_model=schemas.Employee)
def assign_employee_to_project(employee_id: int, project_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(model.Employee).filter(model.Employee.id == employee_id).first()
    db_project = db.query(model.Project).filter(model.Project.id == project_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_employee.projects.append(db_project)
    db.commit()
    db.refresh(db_employee)
    return db_employee
app.mount("/static", StaticFiles(directory="static"), name="static")
