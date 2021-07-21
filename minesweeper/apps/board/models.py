from decimal import Decimal

from django.conf import settings
from django.db import models

from minesweeper.core.models import BaseModel


class Board(BaseModel):
    height = models.IntegerField()
    width = models.IntegerField()
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal(0)
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='games',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )


class BoardCell(BaseModel):
    FLAG_VALUE = -1

    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField(default=0)
    show = models.BooleanField(default=False)
    board = models.ForeignKey(
        'Board',
        related_name='board_cells',
        on_delete=models.CASCADE
    )

    @property
    def is_flag(self):
        return self.value == BoardCell.FLAG_VALUE
