---
description: Repository and Service layer standards for ai-camera backend to keep data access and business logic separated.
---

# Repository and Service Layer Standards (ai-camera)

## Critical Constraints

- Repository MUST be data access only: no business rules in repository layer.
- Service MUST contain business logic: validation, policy, orchestration in service layer.
- Route handlers (FastAPI endpoints) MUST stay thin: schema validation + calling services.

## Python Example (FastAPI)

```python
# ✅ Repository: data access only
class UserRepository:
    def __init__(self, db):
        self._db = db

    def get_by_id(self, user_id: str):
        return self._db.users.find_one({"id": user_id})


# ✅ Service: business logic
class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def get_profile(self, user_id: str):
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("user not found")
        return user
```

