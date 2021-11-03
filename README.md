# snek-paginator
Paginator for Dis-Snek Python Discord API wrapper

## Installation:

```
pip install -U snek-paginator
```

## Basic Example:

```py
from dis_snek.client import Snake
from dis_snek.models.application_commands import slash_command
from dis_snek.models import Embed
from snek_paginator import Paginator

bot = Snake()

@slash_command('paginator')
async def paginator(ctx):
    embeds = [
        Embed(title='Page 1', description='This is page 1'),
        Embed(title='Page 2', description='This is page 2'),
        Embed(title='Page 3', description='This is page 3'),
        Embed(title='Page 4', description='This is page 4'),
        Embed(title='Page 5', description='This is page 5'),
    ]
    await Paginator(bot, ctx, embeds).run()
```

## *class* Paginator

### *method* run(*args, **kwargs)

#### Required:

- `bot: Snake` - The bot instance
- `ctx: InteractionContext` - The context of the command or component
- `pages: list[Embed]` - A list of Embed objects to paginate

#### Optional:

- `timeout: int = None` - How long in seconds the paginator should run
- `author_only: bool = False` - Whether the paginator should only be used by the author
- `only_for: Union[User, Member, Role, List[Union[User, Member, Role]]] = None` - Who should use the paginator
- `use_select: bool = True` - Whether the paginator should use the select
- `use_buttons: bool = True` - Whether the paginator should use the buttons
- `disable_after_timeout: bool = True` - Whether the components should disable after timeout
- `delete_after_timeout: bool = False` - Whether the components should delete after timeout
- `extend_buttons: bool = True` - Whether the first and last page buttons should be used
- `first_button: Button = Button(ButtonStyles.BLUE, emoji="⏮")` - The first page button
- `previous_button: Button = Button(ButtonStyles.BLUE, emoji="◀")` - The previous page button
- `next_button: Button = Button(ButtonStyles.BLUE, emoji="▶")` - The next page button
- `last_button: Button = Button(ButtonStyles.BLUE, emoji="⏭")` - The last page button
