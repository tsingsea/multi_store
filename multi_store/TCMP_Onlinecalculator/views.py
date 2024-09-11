from django.http import JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
from .models import Medicine
from .forms import UploadFileForm
# Create your views here.
from .forms import UploadFileForm
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pypinyin import lazy_pinyin, Style


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            # 解析并保存数据到数据库
            for index, row in df.iterrows():
                Medicine.objects.create(
                    name=row['通用名'],
                    sales_amount=row['销售金额'],
                    sales_quantity=row['销售数量']
                )

            return redirect('success')  # 重定向到一个成功页面
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')

# def search_medicine(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('term'):
#         term = request.GET.get('term')
#         medicines = Medicine.objects.filter(name__icontains=term)
#         results = [medicine.name for medicine in medicines]
#         return JsonResponse(results, safe=False)
#     return JsonResponse([], safe=False)
# def search_medicine(request):
#     term = request.GET.get('term', '').strip().upper()
#
#     # 搜索匹配的药品
#     if term:
#         medicines = Medicine.objects.all()
#         results = []
#         for medicine in medicines:
#             pinyin_abbr = ''.join([p[0].upper() for p in lazy_pinyin(medicine.name, style=Style.FIRST_LETTER)])
#             if pinyin_abbr.startswith(term) or medicine.name.find(term) != -1:
#                 results.append(medicine.name)
#     else:
#         results = []
#
#     return JsonResponse(results, safe=False)
def search_medicine(request):
    term = request.GET.get('term', '').strip().upper()

    if term:
        medicines = Medicine.objects.all()
        results = []
        exact_match = None

        for medicine in medicines:
            pinyin_abbr = ''.join([p[0].upper() for p in lazy_pinyin(medicine.name, style=Style.FIRST_LETTER)])

            # 精确匹配
            if pinyin_abbr == term:
                exact_match = medicine.name
                break
            # 模糊匹配
            elif pinyin_abbr.startswith(term) or medicine.name.find(term) != -1:
                results.append(medicine.name)

        # 如果有精确匹配，优先返回精确匹配结果
        if exact_match:
            return JsonResponse({'exact_match': exact_match}, safe=False)
        else:
            return JsonResponse({'results': results}, safe=False)

    return JsonResponse({'results': []}, safe=False)

def calculate_price(request):
    # 初始化 session 中的 calculations 列表
    if 'calculations' not in request.session:
        request.session['calculations'] = []

    if request.method == 'POST':
        # 获取用户输入的通用名和数量
        name = request.POST.get('name')
        try:
            quantity = Decimal(request.POST.get('quantity', 0))
        except (ValueError, InvalidOperation):
            quantity = Decimal(0)

        # 从数据库中搜索通用名
        medicine = Medicine.objects.filter(name__icontains=name).first()

        if medicine and quantity > 0:
            # 计算价格
            sales_amount = Decimal(medicine.sales_amount)
            sales_quantity = Decimal(medicine.sales_quantity)
            price = (sales_amount / (sales_quantity * Decimal(1000))) * quantity

            # 更新 session 中的 calculations 列表
            calculations = request.session['calculations']
            calculations.append({
                'name': medicine.name,
                'quantity': float(quantity),
                'price': float(price.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))  # 保留三位小数
            })
            request.session['calculations'] = calculations
            request.session.modified = True  # 标记 session 已被修改

        return redirect('calculate_price')

    elif request.method == 'GET' and 'delete' in request.GET:
        # 删除特定记录
        index = int(request.GET.get('delete'))
        calculations = request.session.get('calculations', [])
        if 0 <= index < len(calculations):
            calculations.pop(index)
            request.session['calculations'] = calculations
            request.session.modified = True  # 标记 session 已被修改
        return redirect('calculate_price')

    calculations = request.session.get('calculations', [])
    total_price = sum(item['price'] for item in calculations)

    # 获取“付数”的输入，并允许非整数输入
    try:
        num_of_doses = Decimal(request.GET.get('num_of_doses', 1))
    except (ValueError, InvalidOperation):
        num_of_doses = Decimal(1)

    total_dose_price = total_price * float(num_of_doses)

    return render(request, 'calculate.html', {
        'calculations': calculations,
        'total_price': round(total_price, 3),
        'num_of_doses': float(num_of_doses),
        'total_dose_price': round(total_dose_price, 3)
    })

def clear_calculations(request):
    if 'calculations' in request.session:
        del request.session['calculations']
        request.session.modified = True  # 标记 session 已被修改
    return redirect('calculate_price')