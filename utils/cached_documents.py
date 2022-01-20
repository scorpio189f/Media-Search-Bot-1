from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils

from .helpers import get_input_file_from_file_id


class InlineQueryResultCachedDocument(types.InlineQueryResult):
    """Link to a file stored on the Telegram servers.
    
    By default, this file will be sent by the user with an optional caption. 
    Alternatively, you can use input_message_content to send a message with the specified content instead of the file.
    
    Parameters:
        title (``str``):
            Title for the result.
        
        file_id (``str``):
            Pass a file_id as string to send a media that exists on the Telegram servers.
            
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
            
        description (``str``, *optional*):
            Short description of the result.
            
        caption (``str``, *optional*):
            Caption of the document to be sent, 0-1024 characters.
        
        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.
            
        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent.
    """

    def __init__(
        self,
        title: str,
        file_id: str,
        id: str = None,
        description: str = None,
        caption: str = "",
        parse_mode: Optional[str] = object,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("file", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self, client: "pyrogram.Client"):
        document = get_input_file_from_file_id(self.file_id)

        message, entities = (
            await utils.parse_text_entities(
                client,
                self.caption,
                self.parse_mode,
                self.caption_entities,
            )
        ).values()

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            document=document,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )