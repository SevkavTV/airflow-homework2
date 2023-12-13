import psycopg2

def connect_db():
    return psycopg2.connect(host="localhost", database="db", user="admin", password="12345")

def check_and_update_company(company_info):
    conn = connect_db()
    cur = conn.cursor()
    
    company_name = company_info.get('name', '')
    company_domain = company_info.get('domain', '')
    additional_info = company_info.get('additional_info', '')

    # Check if the company exists in the database
    cur.execute("SELECT id FROM companies WHERE domain = %s", (company_domain,))
    result = cur.fetchone()

    if result:
        # Company exists, update its record
        company_id = result[0]
        cur.execute("UPDATE companies SET name = %s, additional_info = %s WHERE id = %s", 
                    (company_name, additional_info, company_id))
    else:
        # Insert a new company record
        cur.execute("INSERT INTO companies (name, domain, additional_info) VALUES (%s, %s, %s)", 
                    (company_name, company_domain, additional_info))

    conn.commit()
    cur.close()
    conn.close()

