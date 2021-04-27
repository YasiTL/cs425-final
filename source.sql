--drop table has_r;
--drop table lives_in_r;
--drop table picks_plan_r;
--drop table Employee_Phone_m;
--drop table Employee_BenefitSelection_m;
--drop index Employee_FullName_i;
--drop index Employee_Address_i;
--drop table Employee_t;
--drop table Dependent_BenefitSelection_m;
--drop index Dependent_Fullname_i;
--drop table Dependent_t;
--drop table State_t;
--drop table InsurancePlan_t;
--drop type BenefitSelection_e;
--drop type JobTitle_e;
--drop type Salary_e;
create type Salary_e as enum ('HOURLY', 'SALARY');
create type JobTitle_e as enum ('ADMIN', 'MANAGER', 'EMPLOYEE');
create type BenefitSelection_e as enum (
    '401K_CONTRIBUTION',
    'ATTORNEY_PLAN',
    'LIFE_INSURANCE',
    'DENTAL',
    'VISION'
);
create table InsurancePlan_t(
    plan_id varchar(20) primary key,
    employee_cost_for_individualPlan decimal(8, 2),
    employee_cost_for_familyPlan decimal(8, 2),
    employer_cost_for_indivudal decimal(8, 2),
    employer_cost_for_family decimal(8, 2)
);
create table State_t(
    state_name varchar(20) primary key,
    tax_rate float
);
create table Dependent_t(
    d_id varchar(20) primary key,
    first_name varchar(20),
    last_name varchar(20),
    ssn varchar(20),
    benefitSelection BenefitSelection_e
);
create index Dependent_Fullname_i on Dependent_t(d_id, first_name, last_name);
create table Dependent_BenefitSelection_m(
    d_id varchar(20) primary key references Dependent_t on delete cascade,
    selection BenefitSelection_e not null
);
create table Employee_t(
    e_id varchar(20) primary key,
    first_name varchar(20),
    last_name varchar(20),
    ssn varchar(20),
    job_title JobTitle_e,
    salary_type Salary_e,
    insurancePlan varchar(20),
    email varchar(20) check (email like '%@%'),
    country varchar(20),
    state varchar(20),
    street_name varchar(20),
    postal_code numeric(10, 0),
    F01k_deduction int,
    foreign key (insurancePlan) references InsurancePlan_t,
    foreign key (state) references State_t
);
create index Employee_FullName_i on Employee_t(e_id, first_name, last_name);
create index Employee_Address_i on Employee_t(e_id, country, state, street_name, postal_code);
create table Employee_Phone_m(
    e_id varchar(20) primary key references Employee_t on delete cascade,
    phone numeric(10, 0) not null
);
create table Employee_BenefitSelection_m(
    e_id varchar(20) primary key references Employee_t on delete cascade,
    selection BenefitSelection_e not null
);
create table picks_plan_r(
    e_id varchar(20),
    plan_id varchar(20),
    foreign key (e_id) references Employee_t on delete cascade,
    foreign key (plan_id) references InsurancePlan_t on delete cascade,
    primary key (e_id, plan_id)
);
create table lives_in_r(
    e_id varchar(20),
    state_name varchar(20),
    foreign key (e_id) references Employee_t on delete cascade,
    foreign key (state_name) references State_t on delete cascade,
    primary key (e_id, state_name)
);
create table has_r(
    e_id varchar(20),
    d_id varchar(20),
    foreign key (e_id) references Employee_t on delete cascade,
    foreign key (d_id) references Dependent_t on delete cascade,
    primary key (e_id, d_id)
);

--insert into State_t(state_name, tax_rate) values ('test', 45);
--insert into State_t(state_name, tax_rate) values ('Illinois', 22.5);
--insert into insuranceplan_t(plan_id, employee_cost_for_individualPlan, employee_cost_for_familyPlan, employer_cost_for_indivudal, employer_cost_for_family)
--values ('basic health', 159.54, 134.87, 15678.25, 1111.11);
-- insert into employee_t(e_id, first_name, last_name, ssn, job_title, salary_type, insurancePlan, email, country, state, street_name, postal_code, F01k_deduction)
-- values ('TestID', 'boi', 'Smith', 4201337, 'ADMIN', 'HOURLY', 'basic health', 'TechYeah@iit.edu', 'Albania', 'Illinois', 'Main Street', 1808, 25.45);
--update employee_t set first_name = 'junga' where e_id = 'TestID2' RETURNING *;