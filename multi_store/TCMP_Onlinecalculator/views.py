from django.http import JsonResponse
from django.shortcuts import render, redirect
import pandas as pd
from .models import Medicine
from .forms import UploadFileForm
# Create your views here.
from .forms import UploadFileForm
from decimal import Decimal

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

def search_medicine(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('term'):
        term = request.GET.get('term')
        medicines = Medicine.objects.filter(name__icontains=term)
        results = [medicine.name for medicine in medicines]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def calculate_price(request):
    # 初始化 session 中的 calculations 列表
    if 'calculations' not in request.session:
        request.session['calculations'] = []

    if request.method == 'POST':
        # 获取用户输入的通用名和数量
        name = request.POST.get('name')
        quantity = Decimal(request.POST.get('quantity', 0))

        # 从数据库中搜索通用名
        medicine = Medicine.objects.filter(name__icontains=name).first()

        if medicine:
            # 计算价格
            sales_amount = Decimal(medicine.sales_amount)
            sales_quantity = Decimal(medicine.sales_quantity)
            price = (sales_amount / (sales_quantity * Decimal(1000))) * quantity

            # 更新 session 中的 calculations 列表
            calculations = request.session['calculations']
            calculations.append({
                'name': medicine.name,
                'quantity': float(quantity),
                'price': float(round(price, 2))  # 存储时将 Decimal 转换回 float 并四舍五入
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

    return render(request, 'calculate.html', {
        'calculations': calculations,
        'total_price': round(total_price, 2)
    })

def clear_calculations(request):
    if 'calculations' in request.session:
        del request.session['calculations']
        request.session.modified = True  # 标记 session 已被修改
    return redirect('calculate_price')