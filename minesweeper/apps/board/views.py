from board.logic import BoardCellLogic, BoardLogic
from rest_framework import serializers, status
from rest_framework.response import Response

from minesweeper.core.views import BaseDetailView, BaseView
from minesweeper.views import BaseAPIView


class BoardView(BaseView):

    def __init__(self):
        super().__init__()

        self.logic = BoardLogic()

    def post(self, request, *args, **kwargs):
        board = self.logic.create(user=request.user.id, **request.data)
        board_cell_logic = BoardCellLogic()
        board_cell_logic.generate_board_cells_by_board(board=board)
        data = self.logic.serialize(board)
        return Response(data, status=status.HTTP_201_CREATED)


class BoardDetailView(BaseDetailView):

    def __init__(self):
        super().__init__()

        self.logic = BoardLogic()


class InspectBoardCellView(BaseAPIView):

    class InputSerializer(serializers.Serializer):
        x = serializers.IntegerField()
        y = serializers.IntegerField()

    def patch(self, request, pk, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logic = BoardCellLogic()
        board_cell = logic.get(board_id=pk, **serializer.validated_data)
        adjacents = logic.inspect_board_cell(start=board_cell)
        logic.bulk_update(adjacents, fields=['show'])
        data = logic.serialize(adjacents, many=True)
        return Response(data)
