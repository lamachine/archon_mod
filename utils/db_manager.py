import os
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.supabase: Client = create_client(url, key)

    def create_conversation(self, user_id: str) -> int:
        response = self.supabase.table('conversations').insert({
            'user_id': user_id
        }).execute()
        return response.data[0]['id']

    def add_message(self, session_id: int, role: str, message: str, embedding: List[float] = None):
        self.supabase.table('messages').insert({
            'session_id': session_id,
            'role': role,
            'message': message,
            'embedding_nomic': embedding
        }).execute()

    def get_recent_messages(self, session_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        response = self.supabase.table('messages')\
            .select('role, message')\
            .eq('session_id', session_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return response.data

    def search_similar_messages(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        response = self.supabase.rpc(
            'match_messages',
            {
                'query_embedding': embedding,
                'match_threshold': 0.7,
                'match_count': limit
            }
        ).execute()
        return response.data 