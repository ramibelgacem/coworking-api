# Welcome to Coworking API!

API used by a coworking place to manage their companies, employees and equipments.

## Requirements

- Python > 3
- Docker
- Docker-Compose

## Setup

- Create a new directory, e.g api_workspace and move into it
- Clone this repository and navigate into it
- Build docker

``` Bach
docker-compose up --build
```

## How to use it

Open the navigator and access to this URL for example: http://0.0.0.0:8077api/v1/company/, it lists all companies

## Misc

The linter used for this project is flake8

## API Documentation

**Companies API**

- GET --> /company/ : to list companies

- POST --> /company/ : to create a new company
  - Return the new created company

- GET --> /company/{pk}/ : to read a company details
  - Return the requested company
  - Return 404 not found status if the company does not exist

- PUT --> /company/{pk}/ : to update a company
  - Return the updated company
  - Return 404 not found status if the company does not exist

- DELETE --> /company/{pk}/ : to delete a company
  - Return 404 not found status if the company does not exist

- GET --> /company/{pk}/activate/ : to activate a company
  - Return 404 not found status if the company does not exist

- GET --> /company/{pk}/desactivate/ : to desactivate a company
  - Return 404 not found status if the company does not exist

**Employees API**

- GET --> /employee/ : to list employees

- POST --> /employee/ : to create a new employee
  - Return the new created employee
  - Raise Error if the name and username already exist in the database
  - Raise ValueError if the employee's company is inactive

- GET --> /employee/{pk}/ : to read a employee details
  - Return the requested employee
  - Return 404 not found status if the employee does not exist

- PUT --> /employee/{pk}/ : to update a employee
  - Return the updated employee
  - Return 404 not found status if the employee does not exist

- DELETE --> /employee/{pk}/ : to delete a employee
  - Return 404 not found status if the employee does not exist

- GET --> /employee/{pk}/activate/ : to activate a employee
  - Return 404 not found status if the employee does not exist

- GET --> /employee/{pk}/desactivate/ : to desactivate a employee
  - Return 404 not found status if the employee does not exist

**Equipments API**

- GET --> /equipment/ : to list equipments

- POST --> /equipment/ : to create a new equipment
  - Return the new created equipment
  - Raise Error if the equipment is a Screen and the size is not defined
  - Raise Error if the equipment is a PC and the memory/disk size are not defined

- GET --> /equipment/{pk}/ : to read a equipment details
  - Return the requested equipment
  - Return 404 not found status if the equipment does not exist

- PUT --> /equipment/{pk}/ : to update a equipment
  - Return the updated equipment
  - Return 404 not found status if the equipment does not exist

- DELETE --> /equipment/{pk}/ : to delete a equipment
  - Return 404 not found status if the equipment does not exist

- GET --> /equipment/{employee_id}/list/ : list all employee's equipments
  - Return all equipments that are assigned to the given employee
  - Return 404 not found status if the employee does not exist

- POST --> /equipment/{pk}/{employee_id}/assign/ : assign an equipment to an employee
  - Return 200 OK status
  - Return 404 not found status if the equipment does not exist
  - Return 404 not found status if the employee does not exist
  - Raise ValueError if the equipment is already used
  - Raise ValueError if the employee is not active
  - Raise ValueError if the employee is an intern and has more than one PC or one screen
  - Raise a ValueError if the employee is a developer and has more than one PC or more than two screens
  - Raise a ValueError fi the employee is a techlead and his PC has less than 32go of memory or less than 512 of hard disk size

- POST --> /equipment/{pk}/{employee_id}/revoke/ : revoke an equipment to an employee
  - Return 200 OK status
  - Return 404 not found status if the equipment does not exist
  - Return 404 not found status if the employee does not exist

- POST --> /equipment/{employee_id}/revoke-all/ : revoke all employee's equipment
  - Return 200 OK status
  - Return 404 not found status if the employee does not exist

**Extra API**

- GET --> /employee/last-year/ : list tech lead employees joined in the last year
  - Return employee list

- GET --> /employee/{start_year}/{end_year}/ : list interns that joined between two given dates
  - Return employee list
  - Raise ValueError if start_date greater than end_year
