# -*- coding: utf-8 -*-
"""
Created on Tuesday October8 2024

@author: JMM
"""
from pydantic import BaseModel
from fastapi import Form, File, UploadFile

# 1. Class which describes the Titanic API form parameters


class Titanic(BaseModel):
    username: str
    password: str
    select_model: str
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        select_model: str = Form(...),
        file: UploadFile = File(...)
    ):
        return cls(
            username=username,
            password=password,
            select_model=select_model,
            file=file
        )
