# airflow DAGS

In the dag/ folder, put the code that will be needed on production.
Main entry point is the DAGS, that should import scripts.

The proposed structure here is to have one package per project, see below for the project 'test':
dags
├── __init__.py
├── README.md
└── tests
    ├── branch_group_loop_test.py
    ├── __init__.py
    └── README.md

