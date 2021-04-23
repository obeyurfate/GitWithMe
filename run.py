# -*- coding: utf-8 -*-
import os

from app import app


app.run(port=os.environ.get("PORT", 5000))
