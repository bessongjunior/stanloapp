# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present juniorbesong
"""

from shop import create_app

app = create_app()

if __name__=='__main__':
    app.run(debug=True)