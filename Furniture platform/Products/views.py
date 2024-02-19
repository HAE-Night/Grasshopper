import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from Products import models
from .forms import ImageForm, LoginForm
from django.contrib import messages, auth
from django.db.models import Q
from django.http import FileResponse
from pathlib import Path
import os
import cv2
import numpy
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import shutil

response_data = {}


def copy_file(src_path, dest_path):
    try:
        if os.path.exists(dest_path):
            os.remove(dest_path)
            shutil.copy(src_path, dest_path)
            print(f"文件 '{src_path}' 已成功复制到 '{dest_path}'")
    except Exception as e:
        print(f"复制文件时发生错误: {e}")


class Image_Matching:
    """图片比较类"""

    def __init__(self, img_path):
        self.img_path = img_path

    def calculate(self, image1, image2):
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    def classify_hist_with_split(self, image1, image2, size=(256, 256)):
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        image1_ = cv2.resize(image1, size)
        image2_ = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1_)
        sub_image2 = cv2.split(image2_)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    def multiple_image_matching(self, list_image2):
        img1 = cv2.imread(self.img_path)
        sort_list = []
        for image2 in list_image2:
            if os.path.exists(image2) and os.path.isfile(image2):
                img2 = cv2.imread(image2)
                similarity = self.classify_hist_with_split(img1, img2)
                if type(similarity) == numpy.ndarray:
                    similarity = similarity[0]
                sort_list.append(similarity)
            else:
                sort_list.append(0)

        return sort_list


# Django form表单测试
def loginform(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid username or password!'
        else:
            msg = 'An error ocurred!.'

    return render(request, "HTML/login1.html", {"form": form, "msg": msg})


# Create your views here.
@login_required(login_url="/accounts/login/")
def Product_list(request):
    # 获取产品信息
    Products_obj_list = models.Products.objects.all()
    curuser = request.session.get('curuser', '')
    return render(request, 'HTML/Product.html', {"Products_obj_list": Products_obj_list, "curuser": curuser})


@login_required(login_url="/accounts/login/")
def ProductsAdd(request):
    # 添加产品
    if request.method == 'POST':
        data = request.POST
        upload_image = request.FILES['ITEM_PHOTO']
        last_id = models.Products.objects.latest('ID').ID
        extension = str(upload_image.name).split(".")[-1]
        file_Path = default_storage.save(f'static/Photos/{last_id + 1}.{extension}', ContentFile(upload_image.read()))
        attributes = {
            "CATEGORY": data['CATEGORY'],
            "ROOM_AREA": data['ROOM_AREA'],
            "SIZE_DIMENSION": data['SIZE_DIMENSION'],
            "ITEM": data['ITEM'],
            "DESCRIPTION": data['DESCRIPTION'],
            "LENGTH_MM": data['LENGTH_MM'],
            "WIDTH_MM": data['WIDTH_MM'],
            "HEIGHT_MM": data['HEIGHT_MM'],
            "QTY": data['QTY'],
            "UNIT": data['UNIT'],
            "UNIT_PRICE_AED": data['UNIT_PRICE_AED'],
            "INQUIRY_CODE": data['INQUIRY_CODE'],
            "ITEM_PHOTO": "/".join(file_Path.split("/")[1:])
        }
        if models.Products.objects.filter(**attributes).exists():  # 判断添加的数据是否存在
            messages.error(request, 'Product already exists!', extra_tags="warning")
            return redirect('Products:Products_add')
        try:
            # 创建产品
            new_product = models.Products.objects.create(**attributes)
            new_product.save()
            return redirect('Products:Products_list')
        except Exception as e:
            messages.success(request, 'There was an error during the creation!', extra_tags="danger")
            return redirect('Products:Products_add')

    else:
        form = ImageForm()
        context = {
            'form': form
        }
    return render(request, "HTML/Products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsUpdate(request, ID):
    # 产品更新
    if request.method == 'GET':
        try:
            product = models.Products.objects.get(ID=ID)
        except Exception as e:
            messages.success(
                request, 'There was an error trying to get the product!', extra_tags="danger")
            return redirect('Products:Products_list')

        context = {
            'product': product
        }
        return render(request, "HTML/Products_update.html", context=context)

    elif request.method == 'POST':
        data = request.POST
        attributes = {
            "CATEGORY": data['CATEGORY'],
            "ROOM_AREA": data['ROOM_AREA'],
            "SIZE_DIMENSION": data['SIZE_DIMENSION'],
            "ITEM": data['ITEM'],
            "DESCRIPTION": data['DESCRIPTION'],
            "LENGTH_MM": data['LENGTH_MM'],
            "WIDTH_MM": data['WIDTH_MM'],
            "HEIGHT_MM": data['HEIGHT_MM'],
            "QTY": data['QTY'],
            "UNIT": data['UNIT'],
            "UNIT_PRICE_AED": data['UNIT_PRICE_AED'],
            "INQUIRY_CODE": data['INQUIRY_CODE'],
            # "ITEM_PHOTO": "/".join(file_Path.split("/")[1:])
        }
        product = models.Products.objects.get(ID=ID)
        new_item_photo = request.FILES.get('new_item_photo')  # 获取上传的图片
        if new_item_photo is not None:
            if os.path.isfile(f'static/{str(product.ITEM_PHOTO)}'):
                os.remove(f'static/{str(product.ITEM_PHOTO)}')
            extension = str(new_item_photo.name).split(".")[1]
            Photo_Path = default_storage.save(f'static/Photos/{product.ID}.{extension}',
                                              ContentFile(new_item_photo.read()))
            item_photo = {
                "ITEM_PHOTO": "/".join(Photo_Path.split("/")[1:])
            }
            models.Products.objects.filter(ID=ID).update(**item_photo)

        if models.Products.objects.filter(**attributes).exists():
            messages.error(request, 'Product already exists!', extra_tags="warning")
            return redirect('Products:Products_list')
        models.Products.objects.filter(ID=ID).update(**attributes)  # 更新产品信息
        messages.success(request, 'Product: ' +
                         ' updated successfully!', extra_tags="success")
        return redirect('Products:Products_list')


@login_required(login_url="/accounts/login/")
def ProductsDelete(request, ID):
    # 删除产品
    try:
        print(ID)
        product = models.Products.objects.get(ID=ID)
        if os.path.isfile(f'static/{str(product.ITEM_PHOTO)}'):
            os.remove(f'static/{str(product.ITEM_PHOTO)}')  # 删除旧图片
        product.delete()
        messages.success(request, 'Product: ' + product.ITEM +
                         ' deleted successfully!', extra_tags="success")
        return redirect('Products:Products_list')

    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        return redirect('Products:Products_list')


@login_required(login_url="/accounts/login/")
def Productsearch(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        field_name = request.POST.get('field', 'all')

        query = Q()
        if field_name != 'all':
            query |= Q(**{f'{field_name}__icontains': keyword})
        else:
            fields = models.Products._meta.fields
            for field in fields:
                if field.get_internal_type() in ['CharField', 'TextField']:
                    query |= Q(**{f'{field.name}__icontains': keyword})
        items = models.Products.objects.filter(query)
        upload_image = request.FILES.get('Pic')
        Photo_Path = None
        if upload_image is not None and items.count() > 0:
            suffix = upload_image.name.split('.')[-1]
            binary_string = ''.join(['{:02X}'.format(b) for b in upload_image.name.split('.')[0].encode('utf-8')])
            compare_path = f'.\\static\\Comparing_images\\{binary_string + "." + suffix}'
            if os.path.isfile(compare_path):
                os.remove(compare_path)
            file_Path = default_storage.save(f'static/Comparing_images/{binary_string + "." + suffix}',
                                             ContentFile(upload_image.read()))

            Image = Image_Matching(compare_path)
            Image_List = ["./static/" + str(item.ITEM_PHOTO) for item in items]

            Image_result_List = Image.multiple_image_matching(Image_List)
            combined_list = list(zip(items, Image_result_List))  # 两个列表根据得到的相似值排序
            sorted_combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)

            items, sorted_image_result_list = zip(*sorted_combined_list)
            Photo_Path = "/".join(file_Path.split("/")[1:])
            # os.remove(compare_path) #如果要展示图片则不能删除

        return render(request, "HTML/Products_Search_Result.html",
                      {'keyword': keyword, 'field_name': field_name, 'Products_obj_list': items,
                       'Photo_Path': Photo_Path})
    else:
        fields = models.Products._meta.fields
        return render(request, "HTML/Products_Search.html", {"fields": fields})


@login_required(login_url="/accounts/login/")
def download_file(request):
    file_path = r'D:\System_File\Downloads\组织架构1.pptx'
    file = Path(file_path)

    if file.is_file():
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        return response
    else:
        return HttpResponse("文件不存在")


@login_required(login_url="/accounts/login/")
def shooping_cart(request):
    if request.method == 'GET':
        if 'product_ID' in request.session:
            list_productId = request.session['product_ID']
        else:
            list_productId = []
        list_product = []
        for i in list(set(list_productId)):
            product = models.Products.objects.get(ID=i)
            list_product.append(product)
        return render(request, "HTML/Shopping_cart.html", {'Products_obj_list': list_product})
    else:
        product_data = json.loads(request.POST.get('product_data'))
        product_list = list(product_data['product_list'])
        file_path = f"static/excel/Demonstration_template.xlsx"
        new_file_path = f"static/excel/excel.xlsx"
        copy_file(file_path, new_file_path)

        for product in product_list:
            product_id = product[0]
            product_num = product[1]
            product_discount = product[2]
            product_data = models.Products.objects.get(ID=product_id)
            print(product_data.ID)
        return JsonResponse({'status': 'success', 'message': 'Products received successfully'})


@login_required(login_url="/accounts/login/")
def cart_add(request, ID):
    # 向session里面添加商品ID
    if request.method == 'POST':
        ID = request.POST['productId']
        if 'product_ID' not in request.session:
            request.session['product_ID'] = []

        request.session['product_ID'] += ID
        # 返回弹窗提醒数据添成功
        # 返回JSON响应，用于前端处理成功提示
        response_data = {'status': 'success', 'message': 'Product added successfully!'}
        return JsonResponse(response_data)

    return HttpResponse('')


@login_required(login_url="/accounts/login/")
def cart_delete(request, ID):
    # 删除session里面的商品ID
    if request.method == 'POST':
        ID = request.POST['productId']
        list_productId = list(set(request.session['product_ID']))
        list_productId.remove(ID)
        request.session['product_ID'] = list_productId
        # 返回弹窗提醒数据添成功
        # 返回JSON响应，用于前端处理成功提示
        response_data = {'status': 'success', 'message': 'Product deleted successfully!'}
        return JsonResponse(response_data)

    return HttpResponse('')
