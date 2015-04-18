#~*~ coding: utf-8 ~*~
import urllib2

from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import Http404
from lxml import etree

from virtenviro.shop.models import *
from virtenviro.shop.navigation import Navigation
from virtenviro.utils import id_generator


def navigation(request, slug=None):
    production_type_pk = 21
    if slug:
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404
    else:
        product = None

    nav = Navigation(
        product=product,
        production_type_pk=production_type_pk
    )
    navigation = nav.navigation(
        nav_active_product_class='active',
        nav_top_level_class=''
    )
    context = {
        'navigation': navigation,
    }

    return render_to_response('base.html', context, context_instance = RequestContext(request))


def import_xml(request):
    from virtenviro.shop.forms import XmlImportForm
    if request.method == 'POST':
        form = XmlImportForm(request.POST, request.FILES)
        if form.is_valid():
            from virtenviro.utils import handle_uploads
            saved_file = handle_uploads(request, ['xml_file',])['xml_file']
            xml_import(
                os.path.join(settings.MEDIA_ROOT, saved_file),
                default_category=form.cleaned_data['category'],
                default_image_type=form.cleaned_data['image_type'],
                images_path=form.cleaned_data['images_path'],
                parsed_from=form.cleaned_data['parsed_path'],
                parent=form.cleaned_data['parent'])
    else:
        form = XmlImportForm()

    return render(request, 'market/xml_import.html', {'form': form,})


def xml_import(xml_file, default_category, default_image_type, images_path=None, parsed_from=None, parent=None):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_file, parser)
    
    parse_shop(tree=tree, default_category=default_category, default_image_type=default_image_type,
        root_item='.//PRODUCT', is_group=True, images_path=images_path, parsed_from=parsed_from)


def parse_shop(tree, default_category, default_image_type, root_item='.//PRODUCT', is_group=False, images_path=None, parsed_from=None):
    for xml_product in tree.findall(root_item):
        has_main_image = False
        # create category
        product = create_product(name=xml_product.find('NAME').text, parent=parent, articul=xml_product.find('ARTICUL').text, description=xml_product.find('DESCRIPTION').text, default_category=default_category)
        for xml_image in xml_product.findall('IMAGE'):
            try:
                image_link = xml_image.find('img')
                image_url = image_link.attrib['src']
                image_title = image_link.attrib['title']
                if image_url.starts_with('http'):
                    image_download = True
                else:
                    image_download = False
                create_image(url=image_url, title=image_title, product=product, image_type_name=u'DKC', download=image_download)
            except:
                pass


def create_product(name, parent, articul, description=None, default_category = None):
    """

    :param name:
    :param parent:
    :param articul:
    :param description:
    :param default_category:
    :return:
    """
    try:
        product = Product.objects.get(name=name)
    except Product.DoesNotExist:
        product = Product()
        product.name = name
    product.articul = articul
    product.description = description
    product.parent = parent

    product.save()
    return product


def create_parents(parents, default_category):
    for i in range(len(parents)):
        if i == 0:
            product = create_product(name=parents[i], parent=None, is_group=True, default_category=default_category)
        else:
            product = create_product(name=parents[i], parent=parents[i-1], is_group=True, default_category=default_category)
    return product


def create_image(url, title, product, image_type_name = None, download=False):
    try:
        image_type = ImageType.objects.get(name=image_type_name)
    except ImageType.DoesNotExist:
        image_type = ImageType()
        image_type.name = u'Сертификаты'
        image_type.save()
    image = Image()
    image.image_type = image_type
    image_upload_path = os.path.join(settings.STATIC_ROOT, 'files', 'certificate')
    if not os.path.exists(image_upload_path):
        os.makedirs(image_upload_path)
    certificate_file = os.path.join(image_upload_path, '{}.{}'.format(id_generator(12, url.split('.')[-1])))
    if download == True:
        f = open(certificate_file, 'wb')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
        response = opener.open(url)
        data = response.read()
        f.write(data)
        f.close()
    else:
        import shutil
        shutil.copyfile(url, certificate_file)
    image.image = certificate_file
    image.product = product
    image.save()
