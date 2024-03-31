from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
from datetime import datetime
import inspect
import logging
import logging.handlers
import os
import pprint
import re
import textwrap
import time
from collections.abc import Callable
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
from bpy.app.translations import pgettext
from bpy.props import EnumProperty
from bpy.types import bpy_prop_array, bpy_struct
import bpy

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        from typing import Any
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        from bpy.types import UILayout, Context, Operator

__all__ = (
    "CONSOLE_ESC_SEQ",
    "AddonLogger",
)


class CONSOLE_ESC_SEQ:
    """
    Набори символів для встановлення кольору тексту в консолі.
    """
    RESET = '\x1b[0m'
    BLUE = '\x1b[1;34m'
    CYAN = '\x1b[1;36m'
    PURPLE = '\x1b[1;35m'
    GRAY = '\x1b[38;20m'
    YELLOW = '\x1b[33;20m'
    RED = '\x1b[31;20m'
    BOLD_RED = '\x1b[31;1m'
    GREEN = '\x1b[1;32m'


class AddonLogger:
    """
    Клас для роботи з лоґами. Для налагодження доповнень часто важко визначити за яких саме обставин у користувача
    виникли неполадки, тому повні лоґи завжди треба виводити в файл - інформація у ному може розповісти більше ніж
    користувач. Тому тут відбувається виведення логів і в консоль і в файл.

    Клас рекомендується наслідувати для конкретного доповнення, оскільки може виникнути необхідність використовувати
    декілька систем логів для одного доповнення.
    """

    log: None | __IndentLogger = None
    "Доступ до ініціалізованого лоґґера"

    directory: str = ""
    "Директорія до якої зберігаються файли лоґів"

    filename: str = ""
    "Назва файлу лоґу поточної сесії"

    class __IndentLogger(logging.Logger):

        def __init__(self, name):
            super().__init__(name)
            self.indent = 0

        def push_indent(self):
            self.indent += 1
            return self

        def pop_indent(self):
            self.indent = max(0, self.indent - 1)
            return self

        def _indented(self, level, msg):
            indent = ' ' * self.indent * 4

            indented_message = "{caller:25}".format(caller=inspect.stack()[2].function) + '|' + indent + ' ' + msg

            super().log(level, indented_message)
            return self

        def debug(self, msg):
            return self._indented(logging.DEBUG, msg)

        def info(self, msg):
            return self._indented(logging.INFO, msg)

        def warning(self, msg):
            return self._indented(logging.WARNING, msg)

        def error(self, msg):
            return self._indented(logging.ERROR, msg)

        def critical(self, msg):
            return self._indented(logging.CRITICAL, msg)

        def log(self, level, msg):
            self._indented(level, msg)
            return self

    class __ColoredFormatter(logging.Formatter):
        msg = '%(message)s'
        format = '%(name)s (%(levelname)s): '

        FORMATS = {
            logging.DEBUG: CONSOLE_ESC_SEQ.BLUE + format + CONSOLE_ESC_SEQ.RESET + msg,
            logging.INFO: CONSOLE_ESC_SEQ.CYAN + format + CONSOLE_ESC_SEQ.RESET + msg,
            logging.WARNING: CONSOLE_ESC_SEQ.YELLOW + format + CONSOLE_ESC_SEQ.RESET + msg,
            logging.ERROR: CONSOLE_ESC_SEQ.RED + format + CONSOLE_ESC_SEQ.RESET + msg,
            logging.CRITICAL: CONSOLE_ESC_SEQ.BOLD_RED + format + CONSOLE_ESC_SEQ.RESET + msg
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    @classmethod
    def initialize(cls, *, logger_name: str, directory: str, max_num_logs: int = -1):
        """
        Метод для ініціалізації системи логів. Його потрібно викликати під час реєстрації доповнення.

        :param logger_name: Назва лоґґера. Її буде виведено лише у консоль, оскільки файли лоґів і так позиціонуються як
            файли лоґів для конкретного доповнення.
        :type logger_name: str
        :param directory: Директорія у яку буде записано файли лоґів.
        :type directory: str
        :param max_num_logs: Максимальна кількість лоґів у директорії. Якщо значення позитивне то файли логів буде
            перераховано, а зайві - видалено, за замовчуванням -1
        :type max_num_logs: int, optional
        """
        cls.directory = directory
        cls.filename = datetime.now().strftime('log %d-%m-%Y %H-%M-%S.%f.txt')
        log_filepath = os.path.join(directory, cls.filename)

        cls.log = cls.__IndentLogger(logger_name)
        cls.log.setLevel(logging.DEBUG)

        if not cls.log.handlers:
            __fh = logging.FileHandler(filename=log_filepath, mode='w', encoding='utf-8')
            __fh.setLevel(logging.DEBUG)

            __ch = logging.StreamHandler()
            __ch.setLevel(logging.WARNING)

            __fh.setFormatter(logging.Formatter('%(levelname)10s: %(message)s'))
            __ch.setFormatter(cls.__ColoredFormatter())

            cls.log.addHandler(__fh)
            cls.log.addHandler(__ch)

        if max_num_logs > 0:
            pattern = re.compile(r'log (\d{2}-\d{2}-\d{4} \d{2}-\d{2}-\d{2}\.\d{6})\.txt')

            def extract_datetime(filename):
                match = re.search(pattern, filename)
                if match:
                    datetime_str = match.group(1)
                    return datetime.strptime(datetime_str, "%d-%m-%Y %H-%M-%S.%f")
                return datetime.min

            sorted_files = sorted(os.listdir(cls.directory), key=extract_datetime, reverse=True)
            log_ext = os.path.splitext(log_filepath)[1]

            _logs_to_remove = set()

            i = 0
            for filename in sorted_files:
                if os.path.splitext(filename)[1] == log_ext:
                    if i > max_num_logs:
                        _logs_to_remove.add(filename)
                    else:
                        i += 1

            for filename in _logs_to_remove:
                try:
                    os.remove(os.path.join(cls.directory, filename))
                except OSError:
                    break

    @classmethod
    def shutdown(cls):
        """
        Метод для закриття виводу в файл і консоль. Його потрібно викликати під час видалення реєстрації доповнення.
        """
        for handler in cls.log.handlers:
            handler.close()
        cls.log.handlers.clear()
        cls.log = None

        cls.directory = ""
        cls.filename = ""

    @staticmethod
    def _filter_paths_from_keywords(*, keywords: dict[str, Any]) -> dict[str, Any]:
        _str_hidden = "(hidden for security reasons)"
        arg_filepath = keywords.get("filepath", None)
        arg_directory = keywords.get("directory", None)
        arg_filename = keywords.get("filename", None)

        if arg_filepath is not None and arg_filepath:
            if os.path.exists(bpy.path.abspath(arg_filepath)):
                filepath_fmt = f"Existing File Path {_str_hidden}"
            else:
                filepath_fmt = f"Missing File Path {_str_hidden}"

            keywords["filepath"] = filepath_fmt

        if arg_directory is not None and arg_directory:
            if os.path.isdir(bpy.path.abspath(arg_directory)):
                directory_fmt = f"Existing Directory Path {_str_hidden}"
            else:
                directory_fmt = f"Missing Directory Path {_str_hidden}"

            keywords["directory"] = directory_fmt

        if arg_filename is not None and arg_filename:
            keywords["filename"] = f"Some Filename {_str_hidden}"

        return keywords

    @classmethod
    def report_and_log(
        cls,
        operator: Operator,
        *,
        level: int,
        message: str,
        msgctxt: str,
        **msg_kwargs: None | dict[str, Any]
    ):
        """
        Метод для використання з операторами що дозволяє одночасно зробити репорт, враховуючи інтернаціоналізацію
        і вивести лоґ.

        :param operator: Оператор для якого відбудеться репорт.
        :type operator: `Operator`_
        :param level: Рівень лоґу.
        :type level: int
        :param message: Формат повідомлення.
        :type message: str
        :param msgctxt: Контекст інтернаціоналізації.
        :type msgctxt: str
        """
        cls.log.log(level=level, msg=message.format(**msg_kwargs))

        report_message = pgettext(msgid=message, msgctxt=msgctxt).format(**msg_kwargs)

        match level:
            case logging.DEBUG | logging.INFO:
                operator.report(type={'INFO'}, message=report_message)
            case logging.WARNING:
                operator.report(type={'WARNING'}, message=report_message)
            case logging.ERROR | logging.CRITICAL:
                operator.report(type={'ERROR'}, message=report_message)

    @classmethod
    def log_execution_helper(
        cls,
        ot_execute_method: Callable[[Operator, Context], set[int | str]]
    ) -> Callable[[Operator, Context], set[int | str]]:
        """
        Декоратор для методу виконання оператора. Він спершу видрукує який оператор і з якими опціями виконується,
        далі викличе метод оператора і видрукує результат виконання в лоґ.

        :param ot_execute_method: Метод виконання оператора.
        :type ot_execute_method: Callable[[Operator, Context], set[int | str]]
        :return: Декорований метод виконання.
        :rtype: Callable[[Operator, Context], set[int | str]]
        """

        def execute(operator: Operator, context: Context) -> set[int | str]:
            props = operator.as_keywords()

            if props:
                props_fmt = textwrap.indent(
                    pprint.pformat(
                        AddonLogger._filter_paths_from_keywords(keywords=props),
                        indent=4,
                        compact=False),
                    prefix=' ' * 40
                )
                cls.log.debug("\"{label}\" execution begin with properties:\n{props}".format(
                    label=operator.bl_label, props=props_fmt)).push_indent()
            else:
                cls.log.debug("\"{label}\" execution begin".format(label=operator.bl_label)).push_indent()

            dt = time.time()

            ret = ot_execute_method(operator, context)

            cls.log.pop_indent().debug("\"{label}\" execution ended as {flag} in {elapsed:.6f} second(s)".format(
                label=operator.bl_label, flag=ret, elapsed=time.time() - dt))

            return ret

        return execute

    @staticmethod
    def _get_value(*, item: object, identifier: str):
        return getattr(item, identifier, "(readonly)")

    @staticmethod
    def _format_setting_value(*, value: object) -> str:
        if isinstance(value, float):
            value: float
            return '%.6f' % value
        elif isinstance(value, str):
            value: str
            if '\n' in value:
                return value.split('\n')[0][:-1] + " ... (multi-lined string skipped)"
            elif len(value) > 50:
                return value[:51] + " ... (long string skipped)"
        elif isinstance(value, bpy_prop_array):
            return ", ".join((AddonLogger._format_setting_value(value=_) for _ in value))

        return value

    @classmethod
    def log_settings(cls, *, item: bpy_struct):
        """
        Метод для лоґу властивостей структури. Його можна використати наприклад, для лоґу налаштувань з якими було
        запущено доповнення.

        :param item: Структура.
        :type item: bpy_struct
        """
        for prop in item.bl_rna.properties:
            identifier = prop.identifier
            if identifier != 'rna_type':
                value = cls._get_value(item=item, identifier=identifier)
                value_fmt = cls._format_setting_value(value=value)

                cls.log.debug("{identifier}: {value_fmt}".format(identifier=identifier, value_fmt=value_fmt))

                if type(prop.rna_type) == bpy.types.PointerProperty:
                    cls.log.push_indent()
                    cls.log_settings(item=getattr(item, prop.identifier))
                    cls.log.pop_indent()

    @classmethod
    def update_log_setting_changed(cls, identifier: str) -> Callable[[bpy_struct, Context], None]:
        """
        Декоратор для методів оновлення властивостей. Якщо властивість було оновлено то це необхідно занотувати.

        :param identifier: Ідентифікатор властивості в класі.
        :type identifier: str
        :return: Метод оновлення.
        :rtype: Callable[[bpy_struct, Context], None]
        """
        log = cls.log

        def _log_setting_changed(self, _context: Context):
            value = AddonLogger._get_value(item=self, identifier=identifier)
            value_fmt = AddonLogger._format_setting_value(value=value)
            log.debug(f"Setting updated \'{self.bl_rna.name}.{identifier}\': {value_fmt}")

        return _log_setting_changed

    @classmethod
    def get_prop_log_level(cls):
        """
        Властивість для використання в користувацьких налаштуваннях доповнення яка встановлює рівень лоґу.
        """
        log = cls.log

        _update_log_log_level = cls.update_log_setting_changed(identifier="log_level")

        def _update_log_level(self, context: Context):
            for handle in log.handlers:
                if type(handle) == logging.StreamHandler:
                    handle.setLevel(self.log_level)

            _update_log_log_level(self, context)

        return EnumProperty(
            items=(
                (
                    logging.getLevelName(logging.DEBUG),
                    "Debug",
                    "Debug messages (low priority)",
                    0,
                    logging.DEBUG,
                ),
                (
                    logging.getLevelName(logging.INFO),
                    "Info",
                    "Informational messages",
                    0,
                    logging.INFO,
                ),
                (
                    logging.getLevelName(logging.WARNING),
                    "Warning",
                    "Warning messages (medium priority)",
                    0,
                    logging.WARNING,
                ),
                (
                    logging.getLevelName(logging.ERROR),
                    "Error",
                    "Error messages (high priority)",
                    0,
                    logging.ERROR,
                ),
                (
                    logging.getLevelName(logging.CRITICAL),
                    "Critical",
                    "Critical error messages",
                    0,
                    logging.CRITICAL,
                ),
            ),
            default=logging.getLevelName(logging.WARNING),
            update=_update_log_level,
            options={'SKIP_SAVE'},
            translation_context='BHQAB_Preferences',
            name="Log Level",
            description=(
                "The level of the log that will be output to the console. For log to file, this level value will "
                "not change"
            ),
        )

    @classmethod
    def template_ui_draw_paths(cls, layout: UILayout):
        """
        Шаблон для відображення операторів що відкриють шлях до директорії лоґів і поточного лоґу.

        :param layout: Поточний користувацький інтерфейс.
        :type layout: `UILayout`_
        """
        layout.operator(
            operator="wm.path_open",
            text="Open Log Files Directory",
            text_ctxt='BHQAB_Preferences',
        ).filepath = cls.directory

        layout.operator(
            operator="wm.path_open",
            text=pgettext("Open Log: \"{filename}\"", msgctxt='BHQAB_Preferences').format(filename=cls.filename),
        ).filepath = os.path.join(cls.directory, cls.filename)
