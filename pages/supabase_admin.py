from supabase import create_client

url = "https://your-project.supabase.co"
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpld21qdXJ5bG15andleXFvdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTQwMDA5NiwiZXhwIjoyMDc0OTc2MDk2fQ.8DfBdida1EE9RggZQnkARzvod2XR00isq8cXHXOWaQ8"  # Hentes fra Supabase → Project Settings → API

supabase_admin = create_client(url, service_role_key)
