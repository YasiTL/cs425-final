
# CS425 ERP project

## Requirements

Python scripts require [Psycopg 2](https://www.psycopg.org/) which can be installed using the command

>`pip install psycopg2-binary`

## Project requirements

Project Breakdown and timeline
First deliverable: Each group will develop an E-R model for the application on and upload it as any type of image format or pdf due by March03. You can use lucidchart or other software to draw your
diagram. The second deliverable: The E-R model will be translated into a relational schema implemented by an SQL script. The script should run on a PostgreSQL database (or a comparable database of your choice). In addition to defining the tables and constraints the script should create indexes where appropriate due by March28.
Last deliverable is an application that uses the relational schema defined in the first two deliverables.
Due last week of class May5.
Submittal
Everyone will submit the part they worked on. If the group decided to submit one final version,
each team member's contribution must be stated. The project will be submitted via blackboard. For the
last deliverable please submit one code.
Project Description
Design and prototype payment management database application. Your application will allow managing employee salary payment. 
Database Requirements
The application should be able to allow system administrator to manage the database base, add and change records, run reports…

The database is used by employees and administrators. The database helps managing:
 - Employee information such as first, last name, job title, salary type (hourly vs W2), etc.

Bonus percentages varies from an employee to another also from year to year, based on the employee performance and the company sale. Each company sets an allocated percentage that can be provided, if employees performed well, they get the entire percentage, if they did ok, they get half and if they did not do ok no bonus will be provided. For super performers they get the same rate as the manager which is 1.5 x allocated percentage. Hourly employees have no bonus.
 - Each employee lives in a state that has its own tax rate. 
 - All employees pay federal taxes based on the different brackets. Tax rates and brackets are set by the government and will change each year.
 - Each employee must pay social security and 2.5 percent Medicare. For the social security it is total of 15%. For W2 employee the employer pays 7.5 and the employee pays 7.5. Hourly employee pays it all.
 - Each employee has benefits selection such as health plan, 401k contribution, attorney plan, life insurance, etc.…The 401K benefit includes a company match of up to 7% dollar to dollar. Meaning that if the employee elected to contribute 5% the company would give another 5%, if the employee decided to contribute 10%, they will only get up to the 7% max match.
 - Each employee picks an insurance plan, each insurance plan has a premium cost for individual and premium cost for family, also the premium is paid by both employee and employer each will have a contribution.
 - Each employee can have one or multiple dependents. Dependent has a name, SSN, relation to employee, dependent can get the health benefits like dental, vision and life insurance. The employee and dependent can have different or same benefits.

Administrators shall run reports that provides the following information:
 - A biweekly paycheck print that includes the employee ssn, income, all tax deduction (state, federal, social security, and Medicare), 401K deduction and insurance premium,
 - Create a W2 that include the employee SSN, its yearly earned income, all the deduction and extra earning i.e., bonus.
 - Company employee expense report showing all the expense spent: wages, bonus, 401k contribution, employer SSN contribution, employer insurance contribution…