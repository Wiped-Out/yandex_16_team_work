import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class StateController:
    """Класс для сохранения состояния загрузки/выгрузки"""

    file_path: str
    state: Optional[int] = 0
    timestamp: Optional[datetime.datetime] = datetime.datetime(year=2022, month=1, day=1)

    def get_state(self):
        try:
            with open(self.file_path, 'r') as file:
                data = file.readline().split()
                self.state = int(data[0])
                self.timestamp = datetime.datetime.fromisoformat(data[1])
        except FileNotFoundError:
            self.state = 0
            self.timestamp = datetime.datetime(year=2022, month=1, day=1)

    def set_state(self):
        with open(self.file_path, 'w') as file:
            file.write('{state} {timestamp}'.format(state=self.state,
                                                    timestamp=self.timestamp))
