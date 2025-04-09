import os

# Koneksi ke Database OLTP (Sumber Data)
oltp_conn_pg_payroll = {
    'host': os.getenv('OLTP_DB_PG_HOST'),
    'port': os.getenv('OLTP_DB_PG_PORT'),
    'user': os.getenv('OLTP_DB_PG_USER'),
    'password': os.getenv('OLTP_DB_PG_PASSWORD'),
    'database': os.getenv('OLTP_DB_PG_DATABASE_PAYROLL'),
}

oltp_conn_pg_performance = {
    'host': os.getenv('OLTP_DB_PG_HOST'),
    'port': os.getenv('OLTP_DB_PG_PORT'),
    'user': os.getenv('OLTP_DB_PG_USER'),
    'password': os.getenv('OLTP_DB_PG_PASSWORD'),
    'database': os.getenv('OLTP_DB_PG_DATABASE_PERFORMANCE'),
}

oltp_conn_mariadb = {
    'host': os.getenv('OLTP_DB_MARIADB_HOST'),
    'port': os.getenv('OLTP_DB_MARIADB_PORT'),
    'user': os.getenv('OLTP_DB_MARIADB_USER'),
    'password': os.getenv('OLTP_DB_MARIADB_PASSWORD'),
    'database': os.getenv('OLTP_DB_MARIADB_DATABASE'),
}

oltp_conn_mongodb = {
    'host': os.getenv('OLTP_DB_MONGODB_HOST'),
    'port': os.getenv('OLTP_DB_MONGODB_PORT'),
    'user': os.getenv('OLTP_DB_MONGODB_USER'),
    'password': os.getenv('OLTP_DB_MONGODB_PASSWORD'),
    'database': os.getenv('OLTP_DB_MONGODB_DATABASE'),
    'collection': os.getenv('OLTP_DB_MONGODB_COLLECTION'),
}

# Koneksi ke Data Warehouse (Tujuan ETL)
dwh_conn = {
    'host': os.getenv('DWH_DB_HOST'),
    'port': os.getenv('DWH_DB_PORT'),
    'user': os.getenv('DWH_DB_USER'),
    'password': os.getenv('DWH_DB_PASSWORD'),
    'database': os.getenv('DWH_DB_DATABASE')
}

# Mapping antara tabel sumber (OLTP) dan tabel tujuan (Data Warehouse)
table_mapping = {
    "users": {"source": "tb_users", "destination": "dim_user"},
    "payments": {"source": "tb_payments", "destination": "dim_payment"},
    "shippers": {"source": "tb_shippers", "destination": "dim_shipper"},
    "ratings": {"source": "tb_ratings", "destination": "dim_rating"},
    "vouchers": {"source": "tb_vouchers", "destination": "dim_voucher"},
    "orders": {
        "source": ["tb_orders", "tb_users", "tb_payments", "tb_shippers", "tb_ratings", "tb_vouchers"],
        "destination": "fact_orders"
    }
}

oltp_tables = {
    "users": "tb_users",
    "payments": "tb_payments",
    "shippers": "tb_shippers",
    "ratings": "tb_ratings",
    "vouchers": "tb_vouchers",
    "orders": "tb_orders"
}

warehouse_tables = {
    "users": "dim_user",
    "payments": "dim_payment",
    "shippers": "dim_shipper",
    "ratings": "dim_rating",
    "vouchers": "dim_voucher",
    "orders": "fact_orders"
}

# Mapping dari sumber (OLTP) ke tujuan (Data Warehouse)
etl_config_dim_employee = {
    "employee": {
        "source_table": "tb_management_payroll",
        "destination_table": "dim_employee",
        "column_mapping": {
            "EmployeeID": "employee_id",
            "Name": "name",
            "Gender": "gender",
            "Age": "age",
            "Department": "department",
            "Position": "position",
        },
        "query": """
            SELECT 
                DISTINCT
                "EmployeeID",
                "Name",
                "Gender",
                "Age",
                "Department",
                "Position"
            FROM tb_management_payroll
            ORDER BY "EmployeeID"
        """
    },
}

etl_config_fact_payroll = {
    "payroll": {
        "source_table": "tb_management_payroll",
        "destination_table": "fact_payroll",
        "column_mapping": {
            "EmployeeID": "employee_id",
            "PaymentDate": "payment_date",
            "Salary": "salary",
            "OvertimePay": "overtime_pay",
        },
        "query": """
            SELECT 
                DISTINCT
                "EmployeeID",
                "PaymentDate",
                "Salary",
                "OvertimePay"
            FROM tb_management_payroll
            ORDER BY "EmployeeID"
        """
    },
}

etl_config_fact_performance_review = {
    "performance_review": {
        "source_table": "tb_performance_management",
        "destination_table": "fact_performance_review",
        "column_mapping": {
            "EmployeeID": "employee_id",
            "ReviewPeriod": "review_period",
            "Rating": "rating",
            "Comments": "comments",
        },
        "query": """
            SELECT 
                DISTINCT
                "EmployeeID",
                "ReviewPeriod",
                "Rating",
                "Comments"
            FROM tb_performance_reviews
            ORDER BY "EmployeeID"
        """
    },
}

etl_config_fact_training = {
    "training": {
        "source_table": "tb_training_development",
        "destination_table": "fact_training",
        "column_mapping": {
            "EmployeeID": "employee_id",
            "TrainingProgram": "training_program",
            "StartDate": "start_date",
            "EndDate": "end_date",
            "Status": "status",
        },
        "query": """
            SELECT 
                DISTINCT
                `EmployeeID`,
                `TrainingProgram`,
                `StartDate`,
                `EndDate`,
                `Status`
            FROM tb_training_development
            ORDER BY `EmployeeID`
        """
    },
}

etl_config_dim_candicate = {
    "candidate": {
        "collection_name": "recruitment_selection",
        "destination_table": "dim_candidate",
        "column_mapping": {
            "CandidateID": "candidate_id",
            "Name": "name",
            "Gender": "gender",
            "Age": "age"
        },
        "query": {}  # Bisa tambahkan filter MongoDB di sini kalau perlu
    }
}

etl_config_fact_recruitment = {
    "recruitment": {
        "collection_name": "recruitment_selection",
        "destination_table": "fact_recruitment",
        "column_mapping": {
            "CandidateID": "candidate_id",
            "Position": "position_applied",
            "ApplicationDate": "application_date",
            "InterviewDate": "interview_date",
            "Status": "status",
            "OfferStatus": "offer_status"
        },
        "query": {}  # Bisa tambahkan filter MongoDB di sini kalau perlu
    }
}
