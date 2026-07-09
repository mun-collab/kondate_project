

# Create your models here.
# roulette/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ここが "RouletteHistory" になっているか確認
class RouletteHistory(models.Model):
    # ユーザーと履歴を紐付ける（ユーザーが消えたら履歴も消える設定）
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    genre_name = models.CharField(max_length=50)
    recipe_url = models.URLField(max_length=500, null=True, blank=True) # レシピリンク
    memo = models.TextField(max_length=200, null=True, blank=True)      # 一言メモ
    is_post = models.BooleanField(default=False)  # 投稿かどうかのフラグ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 誰のデータかわかるように表示を変更
        return f"{self.user.username if self.user else 'ゲスト'}: {self.genre_name}"