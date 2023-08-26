# Quick and simple scraper to pull some data from OPGG using multisearch

# Author  : ShoobyDoo
# Date    : 2023-07-05
# Edit    : 2023-08-24
# License : BSD-3-Clause

import os
import json
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from opgg.summoner import Summoner
from opgg.season import Season, SeasonInfo
from opgg.champion import ChampionStats, Champion, Spell, Passive, Skin, Price
from opgg.league_stats import LeagueStats, Tier, QueueInfo
from opgg.game import Game
from opgg.params import Region, By


__author__ = 'ShoobyDoo'
__license__ = 'BSD-3-Clause'

# ===== SETUP STR =====
if not os.path.exists('./logs'):
    os.mkdir('./logs')

logging.root.name = 'OPGG.py'

logging.basicConfig(
    filename=f'./logs/opgg_{datetime.now().strftime("%Y-%m-%d")}.log',
    filemode='a+', 
    format='[%(asctime)s][%(name)-22s][%(levelname)-7s] : %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.CRITICAL
)
# ===== SETUP END =====


class OPGG:
    """
    ### OPGG.py
    A simple library to access and structure the data from OP.GG's Website & API.
    """
    cached_page_props = None # todo: fix this later.
    
    def __init__(self, summoner_id: str | None = None, region = Region.NA) -> None:
        self._summoner_id = summoner_id
        self._region = region
        self._api_url = f"https://op.gg/api/v1.0/internal/bypass/summoners/{self.region}/{self.summoner_id}/summary"
        self._headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36" }
        self._all_champions = None
        self._all_seasons = None
        
        logging.debug(
            f"OPGG.__init__(summoner_id={self.summoner_id}, " \
            f"region={self.region}, " \
            f"api_url={self.api_url}, " \
            f"headers={self.headers}, " \
            f"all_champions={self.all_champions}, " \
            f"all_seasons={self.all_seasons})"
        )
    
    @property
    def summoner_id(self) -> str:
        """
        A `str` representing the summoner id. (Riot API)
        """
        return self._summoner_id
    
    @summoner_id.setter
    def summoner_id(self, value: str) -> None:
        self._summoner_id = value
        self.refresh_api_url()
        
    @property
    def region(self) -> str:
        """
        A `str` representing the region to search in.
        """
        return self._region
    
    @region.setter
    def region(self, value: str) -> None:
        self._region = value
        self.refresh_api_url()
        
    @property
    def api_url(self) -> str:
        """
        A `str` representing the api url to send requests to. (OPGG API)
        """
        return self._api_url
    
    @api_url.setter
    def api_url(self, value: str) -> None:
        self._api_url = value
    
    @property
    def headers(self) -> dict:
        """
        A `dict` representing the headers to send with the request.
        """
        return self._headers
    
    @headers.setter
    def headers(self, value: dict) -> None:
        self._headers = value
    
    @property
    def all_champions(self) -> list[Champion]:
        """
        A `list[Champion]` objects representing all champions in the game.
        """
        return self._all_champions
    
    @all_champions.setter
    def all_champions(self, value: list[Champion]) -> None:
        self._all_champions = value
    
    @property
    def all_seasons(self) -> list[SeasonInfo]:
        """
        A `list[SeasonInfo]` objects representing all seasons in the game.
        """
        return self._all_seasons
    
    @all_seasons.setter
    def all_seasons(self, value: list[SeasonInfo]) -> None:
        self._all_seasons = value
    
    
    def refresh_api_url(self) -> None:
        """
        A method to refresh the api url with the current summoner id and region.
        """
        self.api_url = f"https://op.gg/api/v1.0/internal/bypass/summoners/{self.region}/{self.summoner_id}/summary"
        
        logging.debug(f"self.refresh_api_url() called... self.api_url = {self.api_url}")
    
    
    def get_summoner(self) -> Summoner:
        """
        A method to get data from the OPGG API and form a Summoner object.
        
        General flow:\n
            -> Send request to OPGG API\n
            -> Parse data from request (jsonify)\n
            -> Loop through data and form the summoner object.
            
        ### Returns:
            `Summoner`: A Summoner object representing the summoner.
        """
        logging.info(f"Sending request to OPGG API... (API_URL = {self.api_url}, HEADERS = {self.headers})")
        req = requests.get(self.api_url, headers=self.headers)
        
        previous_seasons: list[Season] = []
        league_stats: list[LeagueStats] = []
        most_champions: list[ChampionStats] = []
        recent_game_stats: list[Game] = []
        
        if req.status_code == 200:
            logging.info(f"Request to OPGG API was successful, parsing data (Content Length: {len(req.text)})...")
            content = json.loads(req.text)["data"]
        else:
            req.raise_for_status()
        
        try:            
            for season in content["summoner"]["previous_seasons"]:
                tmp_season_info = None
                if self.all_seasons:
                    for _season in self.all_seasons:
                        if _season.id == season["season_id"]:
                            tmp_season_info = _season
                            break
                
                previous_seasons.append(Season(
                    season_id = tmp_season_info,
                    tier_info = Tier(
                        tier = season["tier_info"]["tier"],
                        division = season["tier_info"]["division"],
                        lp = season["tier_info"]["lp"],
                        tier_image_url = season["tier_info"]["tier_image_url"],
                        border_image_url = season["tier_info"]["border_image_url"]
                    ),
                    created_at = season["created_at"]
                ))
            
            for league in content["summoner"]["league_stats"]:
                league_stats.append(LeagueStats(
                    queue_info = QueueInfo(
                        id = league["queue_info"]["id"],
                        queue_translate = league["queue_info"]["queue_translate"],
                        game_type = league["queue_info"]["game_type"]
                    ),
                    tier_info = Tier(
                        tier = league["tier_info"]["tier"],
                        division = league["tier_info"]["division"],
                        lp = league["tier_info"]["lp"],
                        tier_image_url = league["tier_info"]["tier_image_url"],
                        border_image_url = league["tier_info"]["border_image_url"]
                    ),
                    win = league["win"],
                    lose = league["lose"],
                    is_hot_streak = league["is_hot_streak"],
                    is_fresh_blood = league["is_fresh_blood"],
                    is_veteran = league["is_veteran"],
                    is_inactive = league["is_inactive"],
                    series = league["series"],
                    updated_at = league["updated_at"]
                ))
            
            for champion in content["summoner"]["most_champions"]["champion_stats"]:
                tmp_champ = None
                if self.all_champions:
                    for _champion in self.all_champions:
                        if _champion.id == champion["id"]:
                            tmp_champ = _champion
                            break
                
                most_champions.append(ChampionStats(
                    champion = tmp_champ,
                    play = champion["play"],
                    win = champion["win"],
                    lose = champion["lose"],
                    kill = champion["kill"],
                    death = champion["death"],
                    assist = champion["assist"],
                    gold_earned = champion["gold_earned"],
                    minion_kill = champion["minion_kill"],
                    turret_kill = champion["turret_kill"],
                    neutral_minion_kill = champion["neutral_minion_kill"],
                    damage_dealt = champion["damage_dealt"],
                    damage_taken = champion["damage_taken"],
                    physical_damage_dealt = champion["physical_damage_dealt"],
                    magic_damage_dealt = champion["magic_damage_dealt"],
                    most_kill = champion["most_kill"],
                    max_kill = champion["max_kill"],
                    max_death = champion["max_death"],
                    double_kill = champion["double_kill"],
                    triple_kill = champion["triple_kill"],
                    quadra_kill = champion["quadra_kill"],
                    penta_kill = champion["penta_kill"],
                    game_length_second = champion["game_length_second"]
                ))
            
            for game in content["recent_game_stats"]:
                tmp_champ = None
                if self.all_champions:
                    for _champion in self.all_champions:
                        if _champion.id == game["champion_id"]:
                            tmp_champ = _champion
                            break
                    
                recent_game_stats.append(Game(
                    game_id = game["game_id"],
                    champion = tmp_champ,
                    kill = game["kill"],
                    death = game["death"],
                    assist = game["assist"],
                    position = game["position"],
                    is_win = game["is_win"],
                    is_remake = game["is_remake"],
                    op_score = game["op_score"],
                    op_score_rank = game["op_score_rank"],
                    is_opscore_max_in_team = game["is_opscore_max_in_team"],
                    created_at = game["created_at"]
                ))
        except Exception as e:
            logging.error(f"Error parsing summoner data... (Could be that they just come in as nulls): {e}")
            pass
        
        
        return Summoner(
            id = content["summoner"]["id"],
            summoner_id = content["summoner"]["summoner_id"],
            acct_id = content["summoner"]["acct_id"],
            puuid = content["summoner"]["puuid"],
            name = content["summoner"]["name"],
            internal_name = content["summoner"]["internal_name"],
            profile_image_url = content["summoner"]["profile_image_url"],
            level = content["summoner"]["level"],
            updated_at = content["summoner"]["updated_at"],
            renewable_at = content["summoner"]["renewable_at"],
            previous_seasons = previous_seasons,
            league_stats = league_stats,
            most_champions = most_champions,
            recent_game_stats = recent_game_stats
        )
    
    
    def search(self, summoner_names: str | list[str], region = Region.NA) -> list[Summoner]:
        """
        Search for a single or multiple summoner(s) on OPGG.

        ### Args:
            summoner_names : `str | list[str]`
                Pass either a `str` (comma seperated or single) or `str` list of summoner names.
                
            region : `Region, optional`
                Pass the region you want to search in. Defaults to "NA".

        ### Returns:
            `list[Summoner]` : A list of summoner objects.
        """
        
        if OPGG.cached_page_props:
            page_props = OPGG.cached_page_props
            logging.info("Using cached page props...")
        else:
            page_props = self.get_page_props(summoner_names, region)
            OPGG.cached_page_props = page_props
            logging.info("No cached page props found, fetching...")
        
        self.all_seasons = self.get_all_seasons(self.region, page_props)
        self.all_champions = self.get_all_champions(self.region, page_props)
        
        # todo: if more than 5 summoners are passed, break into 5s and iterate over each set
        # note: this would require calls to the refresh_api_url() method each iteration
        summoners = []
        for id in page_props['summoners']:
            self.summoner_id = id["summoner_id"]
            summoner = self.get_summoner()
            summoners.append(summoner) 
            logging.info(summoner)
            
        return summoners


    @staticmethod
    def get_page_props(summoner_names: str | list[str] = "abc", region = Region.NA) -> dict:
        """
        Get the page props from OPGG. (Contains data such as summoner info, champions, seasons, etc.)
        
        ### Parameters
            summoner_names : `str | list[str], optional`
                Pass a single or comma separated `str` or a list of summoner names.\n
                Note: Default is "abc", as this can be any valid summoner if you just want page props. (All champs, seasons, etc.)
            
            region : `Region, optional`
                Pass the region you want to search in. Default is "NA".

        ### Returns
            `dict` : Returns a dictionary with the page props.
        """
        
        if isinstance(summoner_names, list): summoner_names = ",".join(summoner_names)
        
        url = f"https://op.gg/multisearch/{region}?summoners={summoner_names}"
        headers = { 
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36" 
        }

        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        
        # One request out to OPGG is done here. 
        # Therefore, build out the all_champions and all_seasons properties here as well.
        # This will reduce the overhead of multiple requests out, and just do it all in one go.
        # TODO: Build out the champion and season objects here (?)
        
        return json.loads(soup.select_one("#__NEXT_DATA__").text)['props']['pageProps']
    
    
    @staticmethod
    def get_all_seasons(region = Region.NA, page_props: dict = None) -> list[SeasonInfo]:
        """
        Get all seasons from OPGG.

        ### Args:
            region : `Region, optional`
                Pass the region you want to search in. Defaults to "NA".
                
            page_props : `dict, optional`
                Pass the page props if the program has queried them once before.\n
                Note: Defaults to None, but if you pass them it reduces the overhead of another request out to OPGG.

        ### Returns:
            `list[SeasonInfo]` : A list of SeasonInfo objects.
        """
        
        # TODO: Revisit this caching logic, pretty sure there's a better way to do this
        if page_props is None:
            page_props = OPGG.get_page_props(region)
            OPGG.cached_page_props = page_props
        
        seasons = []
        for season in dict(page_props['seasonsById']).values():
            seasons.append(SeasonInfo(
                id = season["id"],
                value = season["value"],
                display_value = season["display_value"],
                is_preseason = season["is_preseason"]
            ))
        
        return seasons


    @staticmethod
    def get_season_by(by: By, value: int | str | list) -> SeasonInfo | list[SeasonInfo]:
        """
        Get a season by a specific metric.
        
        ### Args:
            by : `By`
                Pass a By enum to specify how you want to get the season(s).
            
            value : `int | str | list`
                Pass the value(s) you want to search by. (id, display_value, etc.)
        
        ### Returns:
            `SeasonInfo | list[SeasonInfo]` : A single or list of SeasonInfo objects.
        """
        
        all_seasons = OPGG.get_all_seasons()
        result_set = []
        
        if by == By.ID:
            if isinstance(value, list):
                for season in all_seasons:
                    for id in value:
                        if season.id == id:
                            result_set.append(season)
            else:
                for season in all_seasons:
                    if season.id == int(value):
                        result_set.append(season)
        
        # TODO: perhaps add more ways to get season objs, like by is_preseason, or display_name, etc.           
        
        return result_set if len(result_set) > 1 else result_set[0]
    
    
    @staticmethod
    def get_all_champions(region = Region.NA, page_props: dict = None) -> list[Champion]:
        """
        Get all champion info from OPGG.

        ### Args:
            region : `Region, optional`
                Pass the region you want to search in. Defaults to "NA".
                
            page_props : `dict, optional`
                Pass the page props if the program has queried them once before.\n
                Note: Defaults to None, but if you pass them it reduces the overhead of another request out to OPGG.

        Returns:
            `list[Champion]` : A list of Champion objects.
        """
        # TODO: Revisit this caching logic, pretty sure there's a better way to do this
        if page_props is None:
            # pass any valid username here, it doesnt matter.
            # we just need the page props, and we dont get them without an actual user
            page_props = OPGG.get_page_props(region)
            OPGG.cached_page_props = page_props
        
        champions = []
        
        for champion in dict(page_props["championsById"]).values():
            # reset per iteration
            _spells = []
            _skins = []
            
            for skin in champion["skins"]:
                _prices = []
                
                if skin["prices"]:
                    for price in skin["prices"]:
                        _prices.append(Price(
                            currency = price["currency"] if "RP" in price["currency"] else "BE",
                            cost = price["cost"]
                        ))
                else:
                    _prices = None
                
                _skins.append(Skin(
                    id = skin["id"],
                    name = skin["name"],
                    centered_image = skin["centered_image"],
                    skin_video_url = skin["skin_video_url"],
                    prices = _prices,
                    sales = skin["sales"]
                ))
                    
            for spell in champion["spells"]:
                _spells.append(Spell(
                    key = spell["key"],
                    name = spell["name"],
                    description = spell["description"],
                    max_rank = spell["max_rank"],
                    range_burn = spell["range_burn"],
                    cooldown_burn = spell["cooldown_burn"],
                    cost_burn = spell["cost_burn"],
                    tooltip = spell["tooltip"],
                    image_url = spell["image_url"],
                    video_url = spell["video_url"]
                ))       
              
            champions.append(Champion(
                id = champion["id"],
                key = champion["key"],
                name = champion["name"],
                image_url = champion["image_url"],
                evolve = champion["evolve"],
                passive = Passive(
                    name = champion["passive"]["name"],
                    description = champion["passive"]["description"],
                    image_url = champion["passive"]["image_url"],
                    video_url = champion["passive"]["video_url"]
                ),
                spells = _spells,
                skins = _skins
            ))            
        
        return champions
    
    
    @staticmethod
    def get_champion_by(by: By, value: int | str | list, **kwargs) -> Champion | list[Champion]:
        """
        Get a single or list of champions by a specific metric.
        
        ### Args:
            by : `By`
                Pass a By enum to specify how you want to get the champion(s).
                
            value : `int | str | list`
                Pass the value(s) you want to search by. (id, key, name, etc.)
                
            **kwargs : `any`
                Pass any additional keyword arguments to narrow down the search.\n
                Note: Currently only supports "currency" for the cost of a champion.\n
                
                Example: 
                    `get_champion_by(By.COST, 450, currency=By.BLUE_ESSENCE)`
        """
        # Currently kwargs only handles "currency" for the cost of a champion,
        # but I might introduce other metrics of getting champ objs later, idk...
        all_champs = OPGG.get_all_champions()
        result_set = []
        
        if by == By.ID:
            if isinstance(value, list):
                for champ in all_champs:
                    for id in value:
                        if champ.id == id:
                            result_set.append(champ)
            else:
                for champ in all_champs:
                    if champ.id == int(value):
                        result_set.append(champ)
                
        elif by == By.KEY:
            if isinstance(value, list):
                for champ in all_champs:
                    for key in value:
                        if champ.key == key:
                            result_set.append(champ)
            else:
                for champ in all_champs:
                    if champ.key == value:
                        result_set.append(champ)
        
        elif by == By.NAME:
            if isinstance(value, list):
                for champ in all_champs:
                    for name in value:
                        if champ.name == name:
                            result_set.append(champ)
            else:
                for champ in all_champs:
                    if champ.name == value:
                        result_set.append(champ)
        
        elif by == By.COST:
            for champ in all_champs:
                if champ.skins[0].prices:
                    for price in champ.skins[0].prices:
                        if str(kwargs["currency"]).upper() == price.currency and price.cost in value:
                            result_set.append(champ)
                
        
        # if the result set is larger than one, return the whole list, otherwise just return the object itself.
        return result_set if len(result_set) > 1 else result_set[0]