class TgUser:
    def __init__(self, id, tg_username, gratitude_id=0, suggestion_id=0, claim_id=0):
        self.id = id
        self.tg_username = tg_username
        self.gratitude_id = gratitude_id
        self.suggestion_id = suggestion_id
        self.claim_id = claim_id

    def __repr__(self):
        return (f"<TgUser(id={self.id}, "
                f"\tg_username={self.tg_username}, "
                f"gratitude_id={self.gratitude_id}, "
                f"suggestion_id={self.suggestion_id}, "
                f"claim_id={self.claim_id})>")