import character
import enemy
import random


class Event:
    def __init__(self):
        pass


class Battle(Event):
    def __init__(self, player: character.Character, enemy: enemy.Enemy):
        #  super.__init__(self)
        self.p = player
        self.e = enemy
        pass

    def combat(self):
        while self.p.hp.cur_hp > 0 and self.e.hp.cur_hp > 0:
            p_attack = self.p.attack
            e_attack = self.e.attack
            p_defense = self.p.defense
            e_defense = self.e.defense
            p_cur_hp = self.p.hp.cur_hp
            e_cur_hp = self.e.hp.cur_hp
            self.e.hp.cur_hp = e_cur_hp - (p_attack - e_defense)
            if self.e.hp.cur_hp <= 0:
                return self.p
            self.p.hp.cur_hp = p_cur_hp - (e_attack - p_defense)
            if self.p.hp.cur_hp <= 0:
                return self.e
