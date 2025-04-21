import uuid
import aiofiles
import asyncio
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict
from src.core.state import SupportState

from src.utils.logger import setup_logger

logger = setup_logger(__name__, "logs/app.log")

# CSV file path
TICKETS_CSV = Path("data/tickets.csv")


async def log_ticket(ticket_id: str, query: str, category: str, created_at: str) -> None:
    """
    Log ticket details to CSV asynchronously with file locking.

    Args:
        ticket_id: Unique ticket identifier.
        query: Customer query.
        category: Query category.
        created_at: Timestamp of ticket creation.
    """
    try:
        async with aiofiles.open(TICKETS_CSV, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            await file.write(f"{ticket_id},{query.replace(',', ' ')},{category},{created_at}\n")
            await file.flush()
        logger.info(f"Logged ticket {ticket_id} for query: {query}")
    except PermissionError:
        logger.error(f"Permission denied writing to {TICKETS_CSV}")
        return None
    except Exception as e:
        logger.error(f"Error logging ticket {ticket_id}: {e}")
        return None
    

async def ticket_agent(state: SupportState) -> SupportState:
    """
    Create a ticket if escalation is required and update the state.

    Args:
        state: Current SupportState with escalate flag, query, category, etc.

    Returns:
        SupportState: Updated state with ticket_id and message .
    """
    try:
        escalate = state['escalate']
        if not escalate:
            logger.info("No escalation required; skipping ticket creation")
            return state

        # Generate unique ticket ID
        ticket_id = f"TICKET_{uuid.uuid4().hex[:8].upper()}"
        created_at = datetime.now().astimezone().isoformat()

        # Log ticket details
        await log_ticket(ticket_id, state["query"], state["category"], created_at)

        # Prepare user message
        message = (
            f"Your issue has been escalated. Ticket ID: {ticket_id}. "
            "Our customer care team will contact you soon."
        )

        # Update state
        state["ticket_id"] = ticket_id
        state["message"] = message

        logger.info(f"Created ticket {ticket_id} with message: {message}")
        return state

    except Exception as e:
        logger.error(f"Error creating ticket for query '{state['query']}': {e}")
        state["message"] = "An error occurred while escalating your issue. Please try again."
        return state
    


# if __name__=="__main__":
#     s = asyncio.run(log_ticket("nothing", "big , nothing", "Nothing", datetime.now()))
