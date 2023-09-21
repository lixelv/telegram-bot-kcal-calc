from aiogram.filters.state import StatesGroup, State

class sts(StatesGroup):

    get_name_of_product = State()
    get_kcal_of_product = State()
    get_protein_of_product = State()
    get_fat_of_product = State()
    get_carbonates_of_product = State()
