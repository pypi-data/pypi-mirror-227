#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

from typing import Callable, List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

ORIGINAL_INSTRUCTION_EU = 0xE59F002C
OFFSET_EU = 0x1238
ORIGINAL_INSTRUCTION_US = 0xE59F0038
OFFSET_US = 0x15DC


class FixMemorySoftlockPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "FixMemorySoftlock"

    @property
    def description(self) -> str:
        return _(
            "Prevents the game from crashing if it runs out of memory when trying to display a sprite (this can "
            "happen during cutscenes when using custom sprites or the randomizer). Instead, the game will be "
            "forced to continue, which will most likely prevent the crash but could cause glitches."
        )

    @property
    def author(self) -> str:
        return "End45"

    @property
    def version(self) -> str:
        return "0.1.1"

    def depends_on(self) -> List[str]:
        return ["ExtraSpace"]

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(rom.arm9, OFFSET_US) != ORIGINAL_INSTRUCTION_US
            if config.game_region == GAME_REGION_EU:
                return read_u32(rom.arm9, OFFSET_EU) != ORIGINAL_INSTRUCTION_EU
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        # Apply the patch
        apply()

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
