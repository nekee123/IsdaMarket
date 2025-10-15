from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from ..database import get_db
import uuid

router = APIRouter(prefix="/messages", tags=["Messages"])

# Pydantic models
class MessageCreate(BaseModel):
    sender_uid: str
    sender_type: str  # "buyer" or "seller"
    recipient_uid: str
    recipient_type: str  # "buyer" or "seller"
    message: str

class MessageResponse(BaseModel):
    uid: str
    sender_uid: str
    sender_type: str
    recipient_uid: str
    recipient_type: str
    message: str
    created_at: str

# Get messages between two users
@router.get("/{user1_uid}/{user2_uid}", response_model=List[MessageResponse])
def get_messages(user1_uid: str, user2_uid: str):
    """Get all messages between two users"""
    driver = get_db()
    with driver.session() as session:
        query = """
        MATCH (m:Message)
        WHERE (m.sender_uid = $user1_uid AND m.recipient_uid = $user2_uid)
           OR (m.sender_uid = $user2_uid AND m.recipient_uid = $user1_uid)
        RETURN m.uid AS uid, m.sender_uid AS sender_uid, m.sender_type AS sender_type,
               m.recipient_uid AS recipient_uid, m.recipient_type AS recipient_type,
               m.message AS message, m.created_at AS created_at
        ORDER BY m.created_at ASC
        """
        result = session.run(query, {"user1_uid": user1_uid, "user2_uid": user2_uid})
        messages = []
        for record in result:
            messages.append({
                "uid": record["uid"],
                "sender_uid": record["sender_uid"],
                "sender_type": record["sender_type"],
                "recipient_uid": record["recipient_uid"],
                "recipient_type": record["recipient_type"],
                "message": record["message"],
                "created_at": record["created_at"]
            })
        return messages

# Send message
@router.post("/", response_model=MessageResponse)
def send_message(message: MessageCreate):
    """Send a message"""
    driver = get_db()
    with driver.session() as session:
        msg_uid = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        query = """
        CREATE (m:Message {
            uid: $uid,
            sender_uid: $sender_uid,
            sender_type: $sender_type,
            recipient_uid: $recipient_uid,
            recipient_type: $recipient_type,
            message: $message,
            created_at: $created_at
        })
        RETURN m.uid AS uid, m.sender_uid AS sender_uid, m.sender_type AS sender_type,
               m.recipient_uid AS recipient_uid, m.recipient_type AS recipient_type,
               m.message AS message, m.created_at AS created_at
        """
        
        result = session.run(query, {
            "uid": msg_uid,
            "sender_uid": message.sender_uid,
            "sender_type": message.sender_type,
            "recipient_uid": message.recipient_uid,
            "recipient_type": message.recipient_type,
            "message": message.message,
            "created_at": created_at
        })
        
        record = result.single()
        
        # Create notification for recipient about new message
        try:
            notif_uid = str(uuid.uuid4())
            # Truncate message for notification
            notif_message = f"New message from {message.sender_type}: {message.message[:50]}"
            if len(message.message) > 50:
                notif_message += "..."
            
            notif_query = """
            CREATE (n:Notification {
                uid: $uid,
                recipient_uid: $recipient_uid,
                recipient_type: $recipient_type,
                type: 'new_message',
                message: $message,
                read: false,
                created_at: $created_at
            })
            """
            
            session.run(notif_query, {
                "uid": notif_uid,
                "recipient_uid": message.recipient_uid,
                "recipient_type": message.recipient_type,
                "message": notif_message,
                "created_at": created_at
            })
        except Exception as e:
            print(f"Error creating message notification: {e}")
        
        return {
            "uid": record["uid"],
            "sender_uid": record["sender_uid"],
            "sender_type": record["sender_type"],
            "recipient_uid": record["recipient_uid"],
            "recipient_type": record["recipient_type"],
            "message": record["message"],
            "created_at": record["created_at"]
        }

# Get conversation list (optional - for future inbox page)
@router.get("/conversations/{user_uid}")
def get_conversations(user_uid: str):
    """Get list of conversations for a user"""
    driver = get_db()
    with driver.session() as session:
        query = """
        MATCH (m:Message)
        WHERE m.sender_uid = $user_uid OR m.recipient_uid = $user_uid
        WITH m,
             CASE WHEN m.sender_uid = $user_uid THEN m.recipient_uid ELSE m.sender_uid END AS other_uid,
             CASE WHEN m.sender_uid = $user_uid THEN m.recipient_type ELSE m.sender_type END AS other_type
        WITH other_uid, other_type, m
        ORDER BY m.created_at DESC
        WITH other_uid, other_type, collect(m)[0] AS last_message
        RETURN other_uid, other_type, last_message.message AS last_message_text, 
               last_message.created_at AS last_message_time
        """
        result = session.run(query, {"user_uid": user_uid})
        conversations = []
        for record in result:
            # Get the other user's name
            other_uid = record["other_uid"]
            other_type = record["other_type"]
            
            # Fetch name based on type
            if other_type == "buyer":
                name_query = "MATCH (b:Buyer {uid: $uid}) RETURN b.name AS name"
            else:
                name_query = "MATCH (s:Seller {uid: $uid}) RETURN s.name AS name"
            
            name_result = session.run(name_query, {"uid": other_uid})
            name_record = name_result.single()
            other_name = name_record["name"] if name_record else "Unknown"
            
            conversations.append({
                "other_user_uid": other_uid,
                "other_user_name": other_name,
                "other_user_type": other_type,
                "last_message": record["last_message_text"],
                "last_message_time": record["last_message_time"],
                "unread_count": 0  # TODO: Implement unread count
            })
        return conversations
