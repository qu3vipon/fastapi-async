from typing import ClassVar

import bcrypt


class PasswordService:
	ENCODING: ClassVar[str] = "utf-8"

	def hash_password(self, plain_text: str) -> str:
		hashed_password_bytes: bytes = bcrypt.hashpw(
			plain_text.encode(self.ENCODING), bcrypt.gensalt()
		)
		return hashed_password_bytes.decode(self.ENCODING)

	def check_password(self, plain_text: str, hashed_password: str) -> bool:
		return bcrypt.checkpw(
			plain_text.encode(self.ENCODING), hashed_password.encode(self.ENCODING)
		)
