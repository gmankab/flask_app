import datetime
from app.common import async_session
from app.models import User


async def predict_activity(user_id: int) -> float:
    '''
    - predict how likely a user is to be active next month
    - higher active_sessions increases chance
    - more recent registrations increase chance
    - result is clamped between 0 and 1
    '''
    async with async_session() as session:
        user = await session.get(User, user_id)
    assert user
    active_sessions = user.active_sessions if user.active_sessions is not None else 0
    registration_dt = datetime.datetime.fromtimestamp(
        timestamp=user.registration_date,
        tz=datetime.timezone.utc,
    )
    now = datetime.datetime.now(datetime.timezone.utc)
    days_since_registration = (now - registration_dt).days
    base_probability = 0.5
    session_factor = min(1.0, active_sessions / 10.0)
    recency_factor = max(0.1, 30 / (days_since_registration + 1))
    if recency_factor > 2.0:
        recency_factor = 2.0
    predicted_probability = base_probability * session_factor * recency_factor
    if predicted_probability > 1:
        predicted_probability = 1.0
    return predicted_probability

