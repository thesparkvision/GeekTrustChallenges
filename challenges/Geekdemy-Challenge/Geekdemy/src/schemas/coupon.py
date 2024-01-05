class Coupon:
    def __init__(
        self, 
        name: str,
        is_explicitly_required: bool = False,
        min_amount: float = 0.0,
        min_programs_count: int = 0
    ):
        self.name = name
        self._is_explicitly_required = is_explicitly_required
        self._min_amount = min_amount
        self._min_programs_count = min_programs_count

    def is_explicitly_required(self) -> bool:
        return self._is_explicitly_required

    def get_minimum_amount_for_applying(self) -> float:
        return self._min_amount

    def get_minimum_programs_count_for_applying(self) -> int:
        return self._min_programs_count