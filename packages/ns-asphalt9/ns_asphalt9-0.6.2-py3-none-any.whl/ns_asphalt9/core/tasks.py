import threading
from datetime import datetime

from . import actions, consts, globals
from .cache import cache
from .utils.decorator import cache_decorator
from .utils.log import logger


class Task:
    name = None
    action = None
    page = None
    # 是否自动返回模式设置的任务中
    auto_return = False

    def __init__(self, page) -> None:
        self.page = page

    def process(self):
        logger.debug(f"Call aciton func = {self.action}")
        self.action(self.page)
        if self.auto_return:
            globals.task_queue.put(globals.CONFIG["模式"])


@cache_decorator("task")
class Mp1Task(Task):
    """多人一任务"""

    name = consts.mp1_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class Mp2Task(Task):
    """多人二任务"""

    name = consts.mp2_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class Mp3Task(Task):
    """多人三任务"""

    name = consts.mp3_zh
    action = staticmethod(actions.enter_series)


@cache_decorator("task")
class CarHuntTask(Task):
    """寻车任务"""

    name = consts.car_hunt_zh
    action = staticmethod(actions.enter_carhunt)


@cache_decorator("task")
class LegendaryHuntTask(Task):
    """传奇寻车任务"""

    name = consts.legendary_hunt_zh
    action = staticmethod(actions.enter_legend_carhunt)


@cache_decorator("task")
class BeastYearTask(Task):
    """野兽年任务"""

    name = consts.beast_year_zh
    action = staticmethod(actions.enter_beast_year)


@cache_decorator("task")
class FreePackTask(Task):
    """免费抽卡任务"""

    name = consts.free_pack_zh
    action = staticmethod(actions.free_pack)
    auto_return = True


@cache_decorator("task")
class PrixPackTask(Task):
    """免费抽卡任务"""

    name = consts.prix_pack_zh
    action = staticmethod(actions.prix_pack)
    auto_return = True


@cache_decorator("task")
class RestartTask(Task):
    """重启任务"""

    name = consts.restart
    action = staticmethod(actions.restart)


@cache_decorator("task")
class ShopNotifyTask(Task):
    """商店通知任务"""

    name = consts.shop_notify
    action = staticmethod(actions.shop_notify)
    auto_return = True


class TaskManager:
    timers = []
    current_task = ""

    @classmethod
    def task_init(cls):
        if "任务" not in globals.CONFIG:
            return
        car_hunt_task = None
        for task in globals.CONFIG["任务"]:
            if task["运行"] > 0 and task["间隔"]:
                cls.task_producer(task["名称"], task["间隔"])
                if task["名称"] in [consts.car_hunt_zh, consts.legendary_hunt_zh]:
                    car_hunt_task = task["名称"]
        if car_hunt_task:
            globals.task_queue.put(car_hunt_task)
        else:
            globals.task_queue.put(globals.CONFIG["模式"])

    @classmethod
    def task_producer(cls, task, duration, skiped=False):
        if skiped:
            globals.task_queue.put(task)
        else:
            logger.info(f"Start task {task} producer, duration = {duration}min")
            skiped = True
        timer = threading.Timer(
            duration * 60, cls.task_producer, (task, duration), {"skiped": skiped}
        )
        timer.start()
        cls.timers.append(timer)

    @classmethod
    def destroy(cls):
        for t in cls.timers:
            t.cancel()

    @classmethod
    def task_dispatch(cls, page) -> bool:
        ShopNotifyProducer.run()
        if not globals.task_queue.empty() and page.name in [
            consts.world_series,
            consts.limited_series,
            consts.trial_series,
            consts.carhunt,
            consts.card_pack,
            consts.legend_pass,
            consts.legendary_hunt,
            consts.daily_events,
            consts.multi_player,
            consts.grand_prix,
            consts.career,
            consts.empty,
        ]:
            task = globals.task_queue.get()
            logger.info(f"Get {task} task from queue.")
            cls.task_enter(task, page)
            return True
        return False

    @classmethod
    def task_enter(cls, task_name, page) -> None:
        logger.info(f"Start process {task_name} task.")
        cls.current_task = task_name
        task_cls = cache.get_by_type("task", task_name)
        task_instance: Task = task_cls(page)
        task_instance.process()


class ShopNotifyProducer:
    notify_list = []

    @classmethod
    def shop_notify_status(cls) -> bool:
        for task in globals.CONFIG["任务"]:
            if task["名称"] == "商店通知" and task["运行"] > 0:
                return True
        return False

    @classmethod
    def run(cls) -> None:
        if "通知" not in globals.CONFIG or not cls.shop_notify_status():
            return
        now_utc = datetime.utcnow()
        # 北京时间17点，20点, 凌晨2点
        if now_utc.hour in [9, 12, 18] and now_utc.minute < 10:
            notify_key = f"{now_utc.month}_{now_utc.day}_{now_utc.hour}"
            if notify_key not in cls.notify_list:
                cls.notify_list.append(notify_key)
                globals.task_queue.put(consts.shop_notify)
