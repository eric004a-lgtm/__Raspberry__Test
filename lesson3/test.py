"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

# BaseModel 是 pydantic 的基礎類別，用來定義資料結構並自動驗證型別
# Field 用來為欄位加上預設值和說明
from pydantic import BaseModel, Field
from typing import Optional  # Optional 表示這個參數可以是 None


class Filter:
    # ── Valves：管理員可調整的設定 ──────────────────────────────
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
            # 這個 Filter 的優先順序，數字越小越先執行
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
            # 整個系統允許的最大對話輪數上限（管理員設定）
        )

    # ── UserValves：每位使用者自己可調整的設定 ───────────────────
    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
            # 使用者自己設定的最大對話輪數（不能超過 Valves 的上限）
        )

    def __init__(self):
        # 建立 Filter 實例時，初始化管理員設定（使用預設值）
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        inlet = 入口，在使用者的訊息送到 AI 之前執行。
        可以在這裡檢查、修改或拒絕請求。
        """
        print(f"inlet:{__name__}")       # 印出目前模組名稱，方便除錯
        print(f"inlet:body:{body}")      # 印出請求內容（包含對話歷史）
        print(f"inlet:user:{__user__}")  # 印出使用者資訊

        # 只對 role 是 "user" 或 "admin" 的人做檢查
        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])  # 取出目前的對話歷史列表

            # 取使用者設定和管理員設定中較小的那個值作為實際上限
            # 例如：管理員設 8，使用者設 4 → 實際上限是 4
            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)

            # 如果對話輪數超過上限，直接拋出例外，阻止這次請求
            if len(messages) > max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        return body  # 檢查通過，把（可能修改過的）請求傳給 AI

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        outlet = 出口，在 AI 回應傳回給使用者之前執行。
        可以在這裡修改或記錄 AI 的回應內容。
        """
        print(f"outlet:{__name__}")       # 印出目前模組名稱，方便除錯
        print(f"outlet:body:{body}")      # 印出 AI 的回應內容
        print(f"outlet:user:{__user__}")  # 印出使用者資訊

        return body  # 把（可能修改過的）回應傳回給使用者
