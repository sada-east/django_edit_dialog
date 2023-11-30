from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .forms import CoordsForm
from .models import Spot


class SpotListView(ListView):
    '''スポット一覧画面
    '''
    model = Spot
    template_name = 'app/spot_list.html'


class CoordsEditor(FormView):
    '''座標編集画面
    '''
    template_name = 'app/coords_edit.html'
    form_class = CoordsForm

    def get_object(self):
        '''編集対象のスポットを取得する
        '''
        if not hasattr(self, 'object'):
            id = self.kwargs.get('pk')
            self.object = get_object_or_404(Spot, id=id)
        return self.object

    def get_initial(self):
        '''フォームに与える初期値を取得する
        '''
        spot = self.get_object()
        return {
            'latitude': spot.coords['latitude'],
            'longitude': spot.coords['longitude'],
        }

    def get_context_data(self, **kwargs):
        '''テンプレートに渡すデータを取得する
        '''
        context = super().get_context_data(**kwargs)

        # 編集の対象となるスポットの id と name
        spot = self.get_object()
        context['spot_id'] = spot.pk        # URL 生成や呼び出し元の判定用
        context['spot_name'] = spot.name    # スポット名の表示用

        # GET パラメタを参照できるようにする
        context['success'] = self.request.GET.get('success')  # 保存成功後か
        context['close'] = self.request.GET.get('close')      # 閉じるか

        # メッセージ配信で指定するためのオリジン
        referer = self.request.META.get('HTTP_REFERER', '')
        if referer:
            parsed_url = urlparse(referer)
            origin = parsed_url.scheme + "://" + parsed_url.netloc
            context['origin'] = origin

        return context

    def get_success_url(self) -> str:
        # POST 処理が正常終了したら、GET パラメタを付けて同じページを再表示する
        url = self.request.path + '?success=1'

        # 「保存して閉じる」(close=1) だったら閉じるための GET パラメタを付ける
        close = self.request.GET.get('close')
        if (close):
            url += '&close=1'

        return url

    def form_valid(self, form):
        spot = self.get_object()
        spot.coords = {
            'latitude': form.cleaned_data['latitude'],
            'longitude': form.cleaned_data['longitude']
        }
        spot.save()
        return super().form_valid(form)
