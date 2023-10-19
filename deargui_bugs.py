# пример демонстрирующий проблемы dearpygui при работе с кириллицей

import dearpygui.dearpygui as dpg
import os

# создание в папке приложения тестовых папок с русскими именами
TEST_PATH = "\\TestCyr\\Проверка 2\\Проверка путей 3"
current_folder = os.path.abspath(os.getcwd())
FULL_PATH = f'{current_folder}{TEST_PATH}'
if not os.path.isdir(FULL_PATH):
	os.makedirs(FULL_PATH)

dpg.create_context()
# данные для мэпинга кириллицы
big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
small_let_end = 0x00FF  # small "я" in cyrillic alphabet
remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped

# подключение стандартного 
with dpg.font_registry():
	with dpg.font("times.ttf", 20) as default_font:
		dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
		dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
		biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
		for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
			dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
			dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
			biglet += 1  # choose next letter

# колбэки для виджета выбора файлов
def callback(sender, app_data):
	print('OK was clicked.')
	print("Sender: ", sender)
	print("App Data: ", app_data)
	dpg.set_value('RESULT', f'Результат выбора:\n{app_data.get("file_path_name")}\
			\nЗайти внутрь папки не получилось!')

def cancel_callback(sender, app_data):
	print('Cancel was clicked.')
	print("Sender: ", sender)
	print("App Data: ", app_data)
	dpg.set_value('RESULT', f'Зайти внутрь папки не получилось!')


# колбэк для кнопки открытия виджета выбора файлов
def openFD_callback(sender, app_data, user_data):
	dpg.show_item(user_data)

# создание окна
with dpg.window(label="Тест"):
	inp1 = dpg.add_input_text(hint = 'Пробуйте ввод кириллицы в этом поле ввода',  width = 600)
	dpg.add_spacer(height = 10)
	dpg.add_text('Нажмите кнопку и откройте диалог выбора файлов. \
		Попробуйте войти внутрь папки с названием "Проверка 2".\
		Внутри находится еще одна папка с именем "Проверка путей 3".\
		Получилось?', wrap = False, color=[128, 128, 255, 255])
	dpg.add_spacer(height = 10)
	dpg.add_button(label = 'Открыть окно выбора', callback = openFD_callback,\
		user_data = 'file_dialog_id')
	dpg.add_text(wrap = False, color=[255, 0, 0, 255], tag='RESULT')
	dpg.add_spacer(height = 10)
	dpg.add_text('Нажмите кнопку и задайте русское название view_port. получилось?', \
		wrap = False, color=[128, 255, 128, 255])
	dpg.add_spacer(height = 10)
	with dpg.group(horizontal=True):
		dpg.add_input_text(hint='Введите название главноего окна кириллицей', tag = 'TITLE')
		dpg.add_button(label = 'Установить', callback = \
			lambda: dpg.set_viewport_title(dpg.get_value('TITLE')))

	f1 = dpg.add_file_dialog(show = False, label = 'Откройте папку с Русским названием', \
		default_path = f'{current_folder}\\TestCyr', directory_selector = True,\
		callback = callback, tag = "file_dialog_id", cancel_callback = cancel_callback,\
		width = 700, height = 400)

dpg.focus_item(inp1)
dpg.bind_font(default_font)
# dpg.bind_item_font(inp1, default_font)
# dpg.bind_item_font(f1, default_font)

dpg.create_viewport(title = 'Demo cirrilyc trouble in File&Dir selector', width = 800, height = 600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()