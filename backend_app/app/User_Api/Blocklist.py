class Blocklist:
    tokens = set()

    @classmethod
    def add(cls, jti):
        cls.tokens.add(jti)

    @classmethod
    def contains(cls, jti):
        return jti in cls.tokens