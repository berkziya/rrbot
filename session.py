import pytz
import schedule

import events
from actions.perks import upgrade_perk
from actions.regions import build_military_academy, work_state_department
from actions.status import set_money
from actions.wars import attack
from actions.work import auto_work_factory
from butler import reset_browser
from misc.logger import alert, log
from misc.utils import numba
from models.autonomy import get_autonomy_info
from models.player import get_player_info
from models.region import get_region_info
from models.state import get_state_info


def session(user):
    user.load_database()

    eventsToBeDone = [
        {"desc": "upgrade perks", "event": upgrade_perk},
        {"desc": "build military academy", "event": build_military_academy},
        {"desc": "energy drink refill", "event": events.energy_drink_refill},
        {"desc": "attack training", "event": attack},
        {
            "desc": "factory work",
            "event": auto_work_factory,
            "args": (user.factory,) if user.factory else (None,),
        },
        {"desc": "economics work", "event": events.hourly_state_gold_refill},
        {
            "desc": "work state department",
            "event": work_state_department,
            "args": (
                None,
                user.statedept,
            )
            if user.statedept
            else (None,),
        },
        {"desc": "upcoming_events", "event": events.upcoming_events},
    ]

    if get_player_info(user, force=True):
        get_region_info(user, user.player.region.id, force=True)
        get_state_info(user, user.player.region.state.id, force=True)
        log(
            user,
            f"ID: {user.player} | Level: {user.player.level} | Rating: {user.player.rating}",
        )
        log(
            user,
            f"Region: {user.player.region} | Residency: {user.player.residency}",
        )
        log(
            user,
            f"Strength: {user.player.perks['str']} | Education: {user.player.perks['edu']} | Endurance: {user.player.perks['end']}",
        )
        log(
            user,
            f"Leader: {user.player.state_leader} | Governor: {user.player.governor} | Economics: {user.player.economics} | Foreign: {user.player.foreign}",
        )
        log(user, f"Party: {user.player.party}")
    else:
        user.s.enter(10, 1, get_player_info, (user,))
        alert(user, "Error setting status, will try again in 10 seconds.")

    if set_money(user, energy=True):
        log(
            user,
            f"Money: {numba(user.player.money['money'])} | Gold: {numba(user.player.money['gold'])} | Energy: {numba(user.player.money['energy'])}",
        )
        log(
            user,
            f"TOTAL GOLD: {numba(user.player.money['energy']//10 + user.player.money['gold'])}",
        )
    else:
        user.s.enter(10, 1, set_money, (user,))
        alert(user, "Error setting money, will try again in 10 seconds.")

    if user.player.governor:
        get_autonomy_info(user, user.player.governor.id, force=True)
        get_state_info(user, user.player.governor.state.id, force=True)
        log(
            user,
            f"""Autonomy Budget:
                                Money: {numba(user.player.governor.budget['money'])}
                                Gold: {numba(user.player.governor.budget['gold'])}
                                Oil: {numba(user.player.governor.budget['oil'])}
                                Ore: {numba(user.player.governor.budget['ore'])}
                                Uranium: {numba(user.player.governor.budget['uranium'])}
                                Diamonds: {numba(user.player.governor.budget['diamonds'])}""",
        )

    if user.player.economics:
        get_state_info(user, user.player.economics.id, force=True)
        log(
            user,
            f"""State Budget:
                                Money: {numba(user.player.economics.budget['money'])}
                                Gold: {numba(user.player.economics.budget['gold'])}
                                Oil: {numba(user.player.economics.budget['oil'])}
                                Ore: {numba(user.player.economics.budget['ore'])}
                                Uranium: {numba(user.player.economics.budget['uranium'])}
                                Diamonds: {numba(user.player.economics.budget['diamonds'])}""",
        )

    user.save_database()

    events.initiate_all_events(user, eventsToBeDone)
    schedule.every(3).to(5).hours.do(events.initiate_all_events, user, eventsToBeDone)
    schedule.every().day.at("18:01", pytz.utc.zone).do(
        events.initiate_all_events, user, eventsToBeDone
    )
    schedule.every(4).to(6).hours.do(reset_browser, user)
    schedule.every(1).to(2).hours.do(user.save_database)

    def activate_scheduler():
        schedule.run_pending()
        user.s.enter(1, 1, activate_scheduler, ())

    activate_scheduler()
    user.s.run(blocking=True)
