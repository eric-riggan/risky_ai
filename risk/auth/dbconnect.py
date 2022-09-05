import yaml

def pyodbc_connstring():
    with open('risk/auth/db_auth.yaml', 'r', encoding='utf8') as stream:
        config = yaml.safe_load(stream)
        connstring = f"DRIVER={{{config['driver']}}};SERVER={config['server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']};Encrypt=YES;TrustServerCertificate=YES"
        return connstring
