#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: robbertmijn
"""

from face_processor._face_processor import _process_face
import os
import argparse

def app():
   parser = argparse.ArgumentParser()
   parser.add_argument('filename', action='store')
   parser.add_argument('id', action='store', default = 999)
   parser.add_argument('sex', action='store', default = "O")
   args = parser.parse_args()

   outname = f"{args.id}_{args.sex}_probe"
   print(f"Starting {outname}")
   img = _process_face(args.filename, os.path.dirname(args.filename), outname)
