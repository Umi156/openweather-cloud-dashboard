from supabase import Client, create_client

from weather.config import SUPABASE_URL, SUPABASE_API_KEY

def get_supabase_client() -> Client:
    """Create a Supabase client."""

    return create_client(SUPABASE_URL, SUPABASE_API_KEY)
