from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import builders

router = Router()


def change_number_page(data, lenght_list, current_page):
    if data == 'left':
        return lenght_list - 1 if current_page == 0 else current_page - 1
    elif data == 'right':
        return 0 if current_page == lenght_list - 1 else current_page + 1


@router.callback_query(F.data.in_(['left', 'right']))
async def change_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.answer()
    else:
        list_keys = tuple(data['pages_obj'].keys())
        if len(list_keys) > 1:
            current_page = data['current_page']
            current_page = change_number_page(callback.data, len(list_keys), current_page)
            builder = builders.create_page_with_navigation(data['pages_obj'][list_keys[current_page]])
            await state.update_data(current_page=current_page)
            if 'can_edit_text' not in data.keys():
                await callback.message.edit_reply_markup(
                    inline_message_id=callback.inline_message_id, 
                    reply_markup=builder.as_markup())
            elif data['can_edit_text'] == 'yes':
                await callback.message.edit_text(
                    text=f'<b><i>{list_keys[current_page]}:</i></b>', 
                    inline_message_id=callback.inline_message_id, 
                    reply_markup=builder.as_markup())
        await callback.answer()
