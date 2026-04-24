import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Count
from .models import RouletteHistory

# --- 会員登録・ユーザー認証系 ---

class SignUpView(generic.CreateView):
    """会員登録画面"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- メイン機能系 ---

def index(request):
    """ルーレット画面（トップページ）"""
    return render(request, 'roulette/index.html')

def save_result(request):
    """
    保存用ビュー（ルーレットからも投稿からもここを使う）
    is_postフラグで履歴と投稿を分ける
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            genre = data.get('genre')
            recipe_url = data.get('recipe_url', "")
            memo = data.get('memo', "")
            
            # 手動投稿の場合は True、ルーレットからの自動保存なら False になるようにする
            # JavaScript側から送るデータに is_post を含めるか、
            # recipe_url や memo があれば投稿とみなす処理に設定します。
            is_manual_post = True if (recipe_url or memo) else False

            if genre:
                user = request.user if request.user.is_authenticated else None
                RouletteHistory.objects.create(
                    user=user, 
                    genre_name=genre,
                    recipe_url=recipe_url,
                    memo=memo,
                    is_post=is_manual_post # ここでフラグを保存！
                )
                return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)           
    return JsonResponse({'status': 'error'}, status=400)

def post_list(request):
    """投稿一覧：日付検索を正しく適用"""
    if request.user.is_authenticated:
        # 1. 投稿データのみ取得
        posts = RouletteHistory.objects.filter(user=request.user, is_post=True).order_by('-created_at')
        
        # 2. キーワード検索
        query = request.GET.get('search')
        if query:
            # Qオブジェクトを使ってジャンル名かメモから検索
            from django.db.models import Q
            posts = posts.filter(Q(genre_name__icontains=query) | Q(memo__icontains=query))
            
        # 3. 日付検索（ここがズレていたポイントです）
        date_query = request.GET.get('date')
        if date_query:
            posts = posts.filter(created_at__date=date_query)
            
        return render(request, 'roulette/post_list.html', {'posts': posts})
    return redirect('login')

def history_list(request):
    """履歴一覧：is_post=False のもの（ルーレット結果）だけを表示"""
    if request.user.is_authenticated:
        # 1. 基礎データ取得（ルーレット履歴のみに絞り込む）
        base_histories = RouletteHistory.objects.filter(user=request.user, is_post=False)
        
        # 2. ランキングの計算 (上位3件)
        ranking = base_histories.values('genre_name') \
                    .annotate(count=Count('genre_name')) \
                    .order_by('-count')[:3]

        # 3. 検索機能
        histories = base_histories.order_by('-created_at')
        
        # キーワード検索
        query = request.GET.get('search')
        if query:
            histories = histories.filter(genre_name__icontains=query)
            
        # 日付検索（ここを整理しました）
        date_query = request.GET.get('date')
        if date_query:
            # historiesに対してフィルターをかける
            histories = histories.filter(created_at__date=date_query)
        
        return render(request, 'roulette/history.html', {'histories': histories, 'ranking': ranking})
    else:
        return redirect('login')

def post_meal(request):
    """投稿画面を表示する"""
    return render(request, 'roulette/post_meal.html')

@require_POST
def delete_history(request, history_id):
    """履歴または投稿の削除"""
    history = get_object_or_404(RouletteHistory, id=history_id)
    # 削除後、投稿なら投稿リスト、履歴なら履歴リストに戻る
    redirect_url = 'post_list' if history.is_post else 'history_list'
    history.delete()
    return redirect(redirect_url)

# views.py の末尾などに追加
def privacy(request):
    return render(request, 'roulette/privacy.html')