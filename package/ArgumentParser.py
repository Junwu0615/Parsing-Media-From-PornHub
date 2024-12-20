# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-18
"""
from argparse import ArgumentParser, Namespace

class AP:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def parse_args() -> Namespace:
        parse = ArgumentParser()
        parse.add_argument('-u', '--url',
                           help="give a <mdeia.m3u8> of PornHub",
                           default='', type=str)

        parse.add_argument('-p', '--path',
                           help="give a save path | ex: './media/'",
                           default='media', type=str)

        return parse.parse_args()

    def config_once(self):
        args = AP.parse_args()
        self.obj.url = args.url
        self.obj.path = args.path