from dataclasses import dataclass, field


@dataclass
class TransactionBlock:
    lines: list[str] = field(default_factory=list)