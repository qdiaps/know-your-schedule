from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def add_default_navigation_buttons(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(InlineKeyboardButton(text='⬅️', callback_data='left'))
    builder.add(InlineKeyboardButton(text='➡️', callback_data='right'))
    return builder


def create_page(objects: list[str]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for obj in objects:
        builder.add(
            InlineKeyboardButton(
                text=obj,
                callback_data=obj
            )
        )
    builder.adjust(*([1] * len(objects)))
    return builder


def create_page_with_navigation(objects: list[str]) -> InlineKeyboardBuilder:
    builder = create_page(objects)
    builder = add_default_navigation_buttons(builder)
    builder.adjust(*([1] * len(objects)), 2)
    return builder


def create_navigation_inline_buttons() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder = add_default_navigation_buttons(builder)
    builder.adjust(2)
    return builder
