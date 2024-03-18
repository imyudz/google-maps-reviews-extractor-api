import os
from supabase import create_client, Client
from supabase.client import ClientOptions

class SupabaseConnector:
    def __init__(self, url, key) -> None:
        self.session = None
        self.token = None
        self.__SUPABASE_URL: str = url
        self.__SUPABASE_KEY: str = key
        self.__supabase: Client = create_client(self.__SUPABASE_URL, self.__SUPABASE_KEY,
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10
            ))

    def get_supabase_client(self):
        return self.__supabase
            
            
            