Have tried to create a tasks workload manager for our team. 
The idea  was administrator / Team manager can add new employees to our employee.db (hosted at Postgres)
Used 4 routes each for /employee/ and /project/ with appropriate parameters for each
The main feature tried to add was many-to-many relationships mapping with back_populates  and bcrypt hashing
Also added role based access control where administrator can add roles (R, W, NULL) for the projects and respective employees for the projects.
