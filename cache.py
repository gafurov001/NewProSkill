import time
import threading

class Cache:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()  # Thread-safe qilish uchun

    def set(self, key, value, ttl):
        """
        Cache'ga qiymat qo'shish.
        :param key: Kalit
        :param value: Qiymat
        :param ttl: Necha sekund saqlanishi kerak
        """
        expire_time = time.time() + ttl
        with self.lock:
            self.store[key] = (value, expire_time)
        threading.Thread(target=self._expire_key, args=(key, ttl)).start()

    def get(self, key):
        """
        Cache'dan qiymat olish.
        :param key: Kalit
        :return: Qiymat yoki None
        """
        with self.lock:
            if key in self.store:
                value, expire_time = self.store[key]
                if time.time() < expire_time:
                    return value
                else:
                    del self.store[key]  # Muddati o'tgan qiymatni o'chirish
        return None

    def _expire_key(self, key, ttl):
        """
        Belgilangan vaqtdan so'ng kalitni avtomatik o'chirish.
        :param key: Kalit
        :param ttl: Necha sekunddan keyin o'chishi kerak
        """
        time.sleep(ttl)
        with self.lock:
            if key in self.store:
                _, expire_time = self.store[key]
                if time.time() >= expire_time:  # Agar TTL tugagan bo'lsa
                    del self.store[key]

    def delete(self, key):
        """
        Kalitni qo'lda o'chirish.
        :param key: Kalit
        """
        with self.lock:
            if key in self.store:
                del self.store[key]
