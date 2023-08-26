from abc import ABC, abstractmethod

# from src.creators.directors.buttons_director import ButtonsDirector
# from src.creators.directors.texts_director import TextsDirector
# from src.utilities.utils import COLORS
# from src.utilities.constants import ScpupViewTypes

class AbstractView(ABC):
    __slots__ = [
        "players"
    ]

    def __init__(self) -> None:
        ...
        # self._initial_texts_ = {}
        # self._buttons_args_ = {}
        # self.background_service = AbstractService.get('BackgoundService')
        # self.players_service = AbstractService.get('PlayersService')
        # self.background_service = BackgroundService()
        # self.players_service = PlayersService()
        # self.clicked_item = None
        # self.set_background()

    # def init_assets(self, targs, bargs) -> None:
    #     if targs is None:
    #         targs = {}
    #     self.texts_group = TextsDirector().create(self.__class__.__name__, **targs)
    #     if bargs is None:
    #         bargs = {}
    #     self.buttons_group = ButtonsDirector().create(self.__class__.__name__, **bargs)

    def clear(self, dest, area) -> None:
        if self.buttons_group is not None:
            self.buttons_group.clear(dest, area)
        if self.texts_group is not None:
            self.texts_group.clear(dest, area)
        # self.clear_other()
        for player in self.players_service.players:
            player.clear(dest, area)

    def draw(self, dest) -> None:
        """ Draw Buttons, Texts and then Players (First Area and then Sprite) """
        if self.buttons_group is not None:
            self.buttons_group.draw(dest)
        if self.texts_group is not None:
            self.texts_group.draw(dest)
        # self.draw_other()
        if not self.players_service.editing:
            for player in self.players_service.playing:
                player.draw(dest, False)

    # def lines(self, *args, **kwargs) -> None:
    #     pass

    # def set_background(self) -> None:
    #     self.background_service.background = getattr(self, "background", COLORS.BACKGROUND)
    #     self.lines()

    # def clear_other(self) -> None:
    #     pass

    # def draw_other(self) -> None:
    #     pass

    def update(self, *, skip_sprites=False) -> None:
        """ 
        Main update method runs if editing mode is not on
        Only updates players 'playing' (First updates buffer's
        time and then player sprites, which are animations and
        time based movements)
        """
        if self.players_service.editing:
            return
        for player in self.players_service.playing:
            player.update(skip_sprites)

    # def refresh_assets(self, *, targs=None) -> None:
    def refresh_texts(self, *, targs=None) -> None:
        if self.texts_group is not None:
            self.texts_group.update(**targs)

    # def collide_button(self, position):
    #     if self.buttons_group is not None:
    #         return self.buttons_group.get_collition(position)
    #     return None

    def click(self, start, player_num) -> bool:
        """
        Method used in click_action which will handle the click event actions for menus and minigames. 
        If this method returns False or None then the 'release click' event will not be triggered. 
        For minigames if a player clicks a special button then this method will not run

        Thoughts: Maybe I could overide this so that only runs when start is True, and for minigames I could
        add some sort of condition to determine if this method should run (which right now it is done at the
        start of each override, see PocketFarkel and MemorizeIt).
        """
        return True

    @abstractmethod
    def click_action(self, start, position, player_num=None):
        """ Abstract method used in the main game loop to handle click interactions with views. This 
        method was designed in a way so that the inheritors of this class use the 'click' method inside
        and also this method must be defined in base classes (classes that are going to be subclassed,
        like BaseMinigame or BaseMenu, and not on the final classes like PocketFarkelGame or MemorizeItGame.
        In any case the 'click' method is the method tht should be overriden in the final classes)."""
        pass

    def handle_combination(self, player_num, combination):
        pass

