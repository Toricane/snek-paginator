from dis_snek.errors import NotFound
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.discord_objects.components import (
    Button,
    ActionRow,
    SelectOption,
    Select,
)
from dis_snek.models.context import InteractionContext, ComponentContext
from dis_snek.models.enums import ButtonStyles, ComponentTypes
from dis_snek.models.events import Component
from dis_snek.client import Snake
from dis_snek.models.discord_objects.user import User, Member
from dis_snek.models.discord_objects.role import Role

from typing import List, Optional, Union, Awaitable, TYPE_CHECKING
from asyncio import TimeoutError, get_running_loop

if TYPE_CHECKING:
    from asyncio import Future


class Paginator:
    def __init__(
        self,
        bot: Snake,
        ctx: InteractionContext,
        pages: List[Embed],
        timeout: Optional[int] = None,
        author_only: Optional[bool] = False,
        only_for: Optional[
            Union[
                User,
                Member,
                Role,
                List[Union[User, Member, Role]],
            ]
        ] = None,
        use_select: Optional[bool] = True,
        use_buttons: Optional[bool] = True,
        disable_after_timeout: Optional[bool] = True,
        delete_after_timeout: Optional[bool] = False,
        extend_buttons: Optional[bool] = True,
        first_button: Button = Button(ButtonStyles.BLUE, emoji="⏮"),
        previous_button: Button = Button(ButtonStyles.BLUE, emoji="◀"),
        next_button: Button = Button(ButtonStyles.BLUE, emoji="▶"),
        last_button: Button = Button(ButtonStyles.BLUE, emoji="⏭"),
    ):
        self.bot = bot
        self.ctx = ctx
        self.pages = pages
        self.timeout = timeout
        self.author_only = author_only
        self.only_for = only_for
        self.use_select = use_select
        self.use_buttons = use_buttons
        self.disable_after_timeout = disable_after_timeout
        self.delete_after_timeout = delete_after_timeout
        self.extend_buttons = extend_buttons
        self.buttons = [first_button, previous_button, next_button, last_button]

        self.current_page = 1
        self.total_pages = len(pages)

    async def run(self):
        msg = await self.ctx.send(embeds=self.pages[0], components=self.components())
        while True:
            try:
                event: Union[
                    Component, Awaitable["Future"]
                ] = await self.bot.wait_for_component(
                    messages=msg,
                    check=self.check,
                    components=self.components(),
                    timeout=self.timeout,
                )
                component_ctx: ComponentContext = event.context
                if component_ctx.component_type == ComponentTypes.SELECT:
                    self.current_page = int(component_ctx.data["data"]["values"][0])
                elif component_ctx.component_type == ComponentTypes.BUTTON:
                    if component_ctx.custom_id == "first":
                        self.current_page = 1
                    elif component_ctx.custom_id == "prev":
                        self.current_page -= 1
                    elif component_ctx.custom_id == "next":
                        self.current_page += 1
                    elif component_ctx.custom_id == "last":
                        self.current_page = self.total_pages

                await component_ctx.edit_origin(
                    embeds=self.pages[self.current_page - 1],
                    components=self.components(),
                )
            except TimeoutError:
                try:
                    if self.delete_after_timeout:
                        await msg.edit(components=[])
                    elif self.disable_after_timeout:
                        await msg.edit(components=self.disabled())
                except NotFound:
                    pass
                break

    def check(self, event) -> bool:
        component_ctx: ComponentContext = event.context
        if self.author_only:
            if component_ctx.author.id != self.ctx.author.id:
                get_running_loop().create_task(
                    component_ctx.send(
                        f"{component_ctx.author.mention}, this paginator is not for you!",
                        ephemeral=True,
                    )
                )
                return False
        if self.only_for:
            check = False
            if isinstance(self.only_for, list):
                for user in filter(
                    lambda x: isinstance(x, (User, Member)), self.only_for
                ):
                    check = check or user.id == component_ctx.author.id
                    if check:
                        break
                if not check:
                    for role in filter(lambda x: isinstance(x, Role), self.only_for):
                        check = check or role in component_ctx.author.roles
                        if check:
                            break
            else:
                if isinstance(self.only_for, (User, Member)):
                    check = self.only_for.id == component_ctx.author.id
                elif isinstance(self.only_for, Role):
                    check = self.only_for in component_ctx.author.roles
            if not check:
                get_running_loop().create_task(
                    component_ctx.send(
                        f"{component_ctx.author.mention}, this paginator is not for you!",
                        ephemeral=True,
                    )
                )
                return False
        return True

    def select_row(self) -> ActionRow:
        select_options = []
        for page in self.pages:
            page_num = self.pages.index(page) + 1
            title = page.title
            if not title:
                select_options.append(
                    SelectOption(
                        label=f"{page_num}: Title not found",
                        value=str(page_num),
                    )
                )
            else:
                title = (title[:93] + "...") if len(title) > 96 else title
                select_options.append(
                    SelectOption(label=f"{page_num}: {title}", value=str(page_num))
                )
        select = Select(
            options=select_options,
            custom_id="select",
            placeholder=f"Page {self.current_page}/{self.total_pages}",
            min_values=1,
            max_values=1,
        )
        return ActionRow(select)

    def buttons_row(self) -> ActionRow:
        disable_left = self.current_page == 1
        disable_right = self.current_page == self.total_pages
        custom_ids = ["first", "prev", "next", "last"]
        for button in self.buttons:
            if button.custom_id != custom_ids[self.buttons.index(button)]:
                button.custom_id = custom_ids[self.buttons.index(button)]
            button.disabled = (
                disable_left if button.custom_id in ("first", "prev") else disable_right
            )
        return ActionRow(*self.buttons)

    def components(self) -> List[ActionRow]:
        return list(
            filter(
                None,
                [
                    self.select_row() if self.use_select else None,
                    self.buttons_row() if self.use_buttons else None,
                ],
            )
        )

    def disabled(self) -> List[ActionRow]:
        components = self.components()
        for action_row in components:
            for component in action_row.components:
                component.disabled = True
        return components
