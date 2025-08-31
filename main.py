from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import threading
import time

class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.interval = 0.1
        self.click_thread = None
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        
    def on_key_press(self, key):
        """Обработка нажатий клавиш"""
        try:
            if key == keyboard.Key.f6:
                self.toggle_clicking()
            elif key == keyboard.Key.f7:
                self.stop()
                print("Автокликер остановлен")
            elif key == keyboard.Key.f8:
                self.increase_interval()
            elif key == keyboard.Key.f9:
                self.decrease_interval()
        except AttributeError:
            pass
    
    def on_click(self, x, y, button, pressed):
        """Обработка кликов мыши (для выбора кнопки)"""
        if pressed and button == Button.right:
            # Правый клик для выбора позиции (опционально)
            print(f"Позиция сохранена: X={x}, Y={y}")
    
    def click_loop(self):
        """Основной цикл кликов"""
        mouse_controller = mouse.Controller()
        while self.clicking:
            mouse_controller.click(Button.left)
            time.sleep(self.interval)
    
    def toggle_clicking(self):
        """Включение/выключение автокликера"""
        if not self.clicking:
            self.clicking = True
            self.click_thread = threading.Thread(target=self.click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
            print(f"Автокликер запущен! Интервал: {self.interval:.2f} сек")
        else:
            self.clicking = False
            print("Автокликер остановлен")
    
    def stop(self):
        """Остановка автокликера"""
        self.clicking = False
    
    def increase_interval(self):
        """Увеличение интервала"""
        self.interval = min(2.0, self.interval + 0.05)
        print(f"Интервал увеличен: {self.interval:.2f} сек")
    
    def decrease_interval(self):
        """Уменьшение интервала"""
        self.interval = max(0.01, self.interval - 0.05)
        print(f"Интервал уменьшен: {self.interval:.2f} сек")
    
    def start(self):
        """Запуск автокликера"""
        print("=== Автокликер запущен ===")
        print("F6 - Включить/выключить автокликер")
        print("F7 - Остановить")
        print("F8 - Увеличить интервал (+0.05 сек)")
        print("F9 - Уменьшить интервал (-0.05 сек)")
        print("Правый клик - сохранить позицию")
        print("==========================")
        
        # Запускаем слушатели
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # Держим программу активной
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
            print("\nАвтокликер завершен")

# Версия с выбором кнопки мыши
class AdvancedAutoClicker(AutoClicker):
    def __init__(self):
        super().__init__()
        self.click_button = Button.left  # кнопка по умолчанию
        self.custom_position = None
    
    def on_key_press(self, key):
        """Расширенная обработка клавиш"""
        try:
            if key == keyboard.Key.f6:
                self.toggle_clicking()
            elif key == keyboard.Key.f7:
                self.stop()
                print("Автокликер остановлен")
            elif key == keyboard.Key.f8:
                self.increase_interval()
            elif key == keyboard.Key.f9:
                self.decrease_interval()
            elif key == keyboard.Key.f10:
                self.switch_button()
            elif key == keyboard.Key.f11:
                self.save_position()
        except AttributeError:
            pass
    
    def switch_button(self):
        """Переключение кнопки мыши"""
        if self.click_button == Button.left:
            self.click_button = Button.right
            print("Кнопка изменена: ПРАВАЯ")
        else:
            self.click_button = Button.left
            print("Кнопка изменена: ЛЕВАЯ")
    
    def save_position(self):
        """Сохранение текущей позиции мыши"""
        mouse_controller = mouse.Controller()
        self.custom_position = mouse_controller.position
        print(f"Позиция сохранена: {self.custom_position}")
    
    def click_loop(self):
        """Расширенный цикл кликов"""
        mouse_controller = mouse.Controller()
        
        # Запоминаем начальную позицию
        original_position = mouse_controller.position
        
        while self.clicking:
            # Если есть сохраненная позиция - кликаем по ней
            if self.custom_position:
                mouse_controller.position = self.custom_position
            
            mouse_controller.click(self.click_button)
            
            # Возвращаем мышь на исходную позицию
            if self.custom_position:
                mouse_controller.position = original_position
            
            time.sleep(self.interval)

# Запуск программы
if __name__ == "__main__":
    print("Выберите режим:")
    print("1 - Простой автокликер")
    print("2 - Продвинутый автокликер")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "2":
        clicker = AdvancedAutoClicker()
    else:
        clicker = AutoClicker()
    
    clicker.start()