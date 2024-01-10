import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from butler import error, get_page, return_to_mainwindow
from misc.utils import dotless
from models import get_factory, get_player, get_region


class Factory:
    def __init__(self, id):
        self.id = id
        self.last_accessed = 0
        self.type = ""
        self.region = None
        self.owner = None
        self.level = 0
        self.wage = 0
        self.fixed_wage = False
        self.potential_wage = 0

    def set_last_accessed(self):
        self.last_accessed = time.time()

    def set_type(self, value):
        if value == "diamond":
            value = "diamonds"
        self.type = value

    def set_region(self, value):
        self.region = value

    def set_owner(self, value):
        self.owner = value

    def set_level(self, value):
        self.level = value

    def set_wage(self, value):
        self.wage = value

    def set_fixed_wage(self, value):
        self.fixed_wage = value

    def set_potential_wage(self, value):
        self.potential_wage = value

    def __str__(self):
        return str(self.id)

    def __getstate__(self):
        return {
            "id": self.id,
            "last_accessed": self.last_accessed,
            "type": self.type,
            "region": self.region.id if self.region else None,
            "owner": self.owner.id if self.owner else None,
            "level": self.level,
            "wage": self.wage,
            "fixed_wage": self.fixed_wage,
            "potential_wage": self.potential_wage,
        }

    def __setstate__(self, state):
        self.id = state["id"]
        self.last_accessed = state["last_accessed"]
        self.type = state["type"]
        self.region = get_region(state["region"]) if state["region"] else None
        self.owner = get_player(state["owner"]) if state["owner"] else None
        self.level = state["level"]
        self.wage = state["wage"]
        self.fixed_wage = state["fixed_wage"]
        self.potential_wage = state["potential_wage"]


def get_factory_info(user, id, force=False):
    try:
        factory = get_factory(id)
        if factory.last_accessed > time.time() - 3600 and not force:
            return factory
        if not get_page(user, f"factory/index/{id}"):
            return False
        data = user.driver.find_elements(
            By.CSS_SELECTOR,
            "div.float_left.margin_left_20 > div",
        )
        if "change_paper_about_target" in data[0].get_attribute("class"):
            line = data[0].text.split("\n")[0]
            factory.set_level(int(line.split(" ")[-1]))
            factory.set_type(line.split(" ")[0].lower())
        for div in data[1:]:
            if "Factory region:" in div.find_element(By.CSS_SELECTOR, "h2").text:
                pass
                factory.set_region(
                    get_region(
                        div.find_element(By.CSS_SELECTOR, "span")
                        .get_attribute("action")
                        .split("/")[-1]
                    )
                )
            elif "Owner:" in div.find_element(By.CSS_SELECTOR, "h2").text:
                factory.set_owner(
                    get_player(
                        div.find_element(By.CSS_SELECTOR, "span")
                        .get_attribute("action")
                        .split("/")[-1]
                    )
                )
            elif "Wage:" in div.find_element(By.CSS_SELECTOR, "h2").text:
                wage = div.find_element(By.CSS_SELECTOR, "div.tc > h2").text
                if "%" in wage:
                    wage = float(wage.split(" ")[0]) / 100
                else:
                    factory.set_fixed_wage(True)
                    wage = dotless(wage.split(" ")[0])
                factory.set_wage(wage)
            elif "Potential wage" in div.find_element(By.CSS_SELECTOR, "h2").text:
                factory.set_potential_wage(
                    dotless(
                        div.find_element(
                            By.CSS_SELECTOR, "div.tc > h2 > span"
                        ).text.split(" ")[0]
                    )
                )
        factory.set_last_accessed()
        return_to_mainwindow(user)
        return factory
    except NoSuchElementException:
        return_to_mainwindow(user)
        return None
    except Exception as e:
        return error(user, e, "Error getting factory info")
