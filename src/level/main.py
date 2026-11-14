# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

class Level:
    @staticmethod
    def calculate_level(xp: int) -> int:
        """Reach levels 2, 5, and 10 at 100, 3000, and 15000 cumulative XP."""
        level = 1
        required_xp = 100

        while xp >= required_xp:
            level += 1
            if level < 5:
                required_xp += 100 * level**2
            else:
                required_xp += 300 * (level + 1)

        return level
