from supabase import create_client

url = "https://your-project.supabase.co"
service_role_key = "your-service-role-key"  # Hentes fra Supabase → Project Settings → API

supabase_admin = create_client(url, service_role_key)
