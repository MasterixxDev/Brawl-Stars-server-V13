import csv
import os
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Reward:
    goal: str
    main_level: int
    sub_level: int
    end: int
    reward_type: str   # "1","3","6","7","9","10","12","13","14"
    count: int
    brawler_id: Optional[int] = None
    brawler_name: Optional[str] = None


class RewardDataLoader:
    # Разрешённые типы наград
    ALLOWED_TYPES = {"1", "3", "6", "7", "9", "10", "12", "13", "14"}

    # Имя бравлера -> ID
    BRAWLER_NAME_TO_ID = {
        "Shaman": 8,
        "Gunslinger": 1,
        "BullDude": 2,
        "Mechanic": 7,
        "RocketGirl": 3,
        "TntDude": 9,
        "BowDude": 14,
        "ClusterBombDude": 22,
        "Arcade": 27,
    }

    @staticmethod
    def _to_int(value, default=0) -> int:
        try:
            return int(str(value).strip())
        except Exception:
            return default

    @staticmethod
    def get_reward_data(level: int) -> Optional[List[Reward]]:
        file_path = "GameAssets/csv_logic/milestones.csv"
        if not os.path.exists(file_path):
            print(f"[ERROR] Milestones file not found at {file_path}")
            return None

        milestone_index = level - 1
        if milestone_index < 0:
            print(f"[ERROR] Invalid level {level} (after shift {milestone_index})")
            return None

        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file, quotechar='"')
                for row in reader:
                    if not row or not row[0] or row[0].startswith("#"):
                        continue

                    if row[0] == f"goal_6_{milestone_index}":
                        rewards: List[Reward] = []

                        goal = row[0]
                        main_level = RewardDataLoader._to_int(row[1])
                        sub_level  = RewardDataLoader._to_int(row[2])
                        end        = RewardDataLoader._to_int(row[3])

                        # Награды начинаются с 9-й колонки и далее каждые 4
                        for i in range(9, len(row), 4):
                            t = str(row[i]).strip() if i < len(row) else ""
                            # фильтруем пустые/служебные и неизвестные типы
                            if not t or t in {"0", "-1"} or t not in RewardDataLoader.ALLOWED_TYPES:
                                continue

                            count = RewardDataLoader._to_int(row[i+1]) if i+1 < len(row) else 0

                            brawler_id: Optional[int] = None
                            brawler_name: Optional[str] = None

                            # Если бравлер (type=3), читаем ячейку i+3 (id или имя)
                            if t == "3" and i+3 < len(row):
                                cell = str(row[i+3]).strip()
                                if cell and cell != "-1":
                                    if cell.isdigit():
                                        brawler_id = int(cell)
                                    else:
                                        brawler_name = cell
                                        brawler_id = RewardDataLoader.BRAWLER_NAME_TO_ID.get(brawler_name)

                            rewards.append(
                                Reward(
                                    goal=goal,
                                    main_level=main_level,
                                    sub_level=sub_level,
                                    end=end,
                                    reward_type=t,
                                    count=count,
                                    brawler_id=brawler_id,
                                    brawler_name=brawler_name,
                                )
                            )

                        # Для дебага: покажем, что именно распарсили
                        if rewards:
                            dbg = ", ".join(
                                f"{r.reward_type}:{r.count}" +
                                (f":{r.brawler_name or r.brawler_id}" if r.reward_type == '3' else "")
                                for r in rewards
                            )
                            print(f"[DEBUG] Parsed {goal} -> {dbg}")

                        return rewards if rewards else None

            print(f"[ERROR] No reward defined for level {level}")
            return None

        except Exception as e:
            print(f"[ERROR] Error reading milestones: {e}")
            return None

