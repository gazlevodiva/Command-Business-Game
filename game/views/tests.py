from django.test import TestCase
from game.models import Moves
from game.models import Surprises
from game.models import MemoryAnswers
from game.models import Actions
from game.models import Player
from game.models import GameSessions
from game.views.player_panel.surprise import get_memory, set_memory


class MemoryTestCase(TestCase):
    def setUp(self):
        # Создайте тестовые объекты, которые будут использоваться в тестах
        self.game_session = GameSessions.objects.get(pk=8)
        self.player = Player.objects.create(
            name="Anatoliy", game_session=self.game_session
        )
        self.surprise = Surprises.objects.create(
            name="Test memory", count=1, category="MEMO", session_id=8
        )

    def test_get_memory_with_available_memories(self):
        # Предполагается, что есть доступные воспоминания
        memory = get_memory(self.player.moves.first())
        self.assertIsNotNone(
            memory, "Should return a memory object when available"
        )

    def test_get_memory_with_default_memories(self):
        # Предполагается, что доступных воспоминаний нет, но есть дефолтные
        Surprises.objects.filter(
            session_id=self.player.game_session.id
        ).delete()
        Surprises.objects.create(
            name="Default Surprise", count=1, category="MEMO", session_id=0
        )
        memory = get_memory(self.player.moves.first())
        self.assertIsNotNone(
            memory, "Should return a default memory when no session-specific memories are available"
        )

    def test_get_memory_without_any_memories(self):
        # Предполагается, что воспоминаний нет вообще
        Surprises.objects.all().delete()
        memory = get_memory(self.player.moves.first())
        self.assertIsNone(memory, "Should return None when no memories are available")

    def test_set_memory_creates_action(self):
        # Проверка, что действие создается, если воспоминание доступно
        memory = get_memory(self.player.moves.first())
        set_memory(self.player.moves.first())
        action_count = Actions.objects.filter(move=self.player.moves.first(), category="MEMO").count()
        self.assertEqual(action_count, 1, "Should create an action for the memory")

    # Можно добавить другие тесты для проверки исключительных ситуаций и ошибок
