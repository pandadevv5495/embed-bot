import interactions
from datetime import datetime

# Replace with your bot's token
TOKEN = "YOUR_BOT_TOKEN"

class EmbedData:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.color = 0xFFFFFF
        self.fields = []
        self.footer = ""
        self.thumbnail_url = ""
        self.image_url = ""
        self.timestamp = datetime.now()

    def to_embed(self):
        embed = interactions.Embed(
            title=self.title,
            description=self.description,
            color=self.color,
            footer=interactions.EmbedFooter(text=self.footer),
            thumbnail=interactions.EmbedThumbnail(url=self.thumbnail_url),
            image=interactions.EmbedImage(url=self.image_url),
            timestamp=self.timestamp
        )
        for field in self.fields:
            embed.add_field(name=field['name'], value=field['value'], inline=field.get('inline', False))
        return embed

embed_data = EmbedData()

bot = interactions.Client(token=TOKEN)

# Slash command with options
@bot.command(
    name="create_embed",
    description="Interactive embed creator",
    options=[
        interactions.Option(
            name="title",
            description="Set the title of the embed",
            type=interactions.OptionType.STRING,
            required=False
        ),
        interactions.Option(
            name="description",
            description="Set the description of the embed",
            type=interactions.OptionType.STRING,
            required=False
        ),
        # Add other options like color, fields, footer, etc.
    ]
)
async def create_embed(ctx: interactions.CommandContext, title: str = None, description: str = None):
    if title:
        embed_data.title = title
    if description:
        embed_data.description = description
    # Handle other options similarly
    embed = embed_data.to_embed()
    await ctx.send(embeds=[embed], ephemeral=True)

# Context menu for adding fields
@bot.context_menu(
    name="Add Field to Embed",
    type=interactions.CommandType.MESSAGE
)
async def add_field(ctx: interactions.CommandContext, message: interactions.Message):
    field_name = "Field"
    field_value = message.content
    embed_data.fields.append({"name": field_name, "value": field_value, "inline": False})
    await ctx.send(f"Field added: {field_value}", ephemeral=True)

bot.start()
