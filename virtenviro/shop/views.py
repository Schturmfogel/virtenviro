#~*~ coding: utf-8 ~*~
import urllib2
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import Http404
from django.conf import settings
from lxml import etree
from forms import SimpleXmlImportForm
from models import *
from virtenviro.shop.navigation import Navigation
from virtenviro.utils import id_generator, handle_uploads, sha256

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))


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


def import_simple_xml(request):
    if request.method == 'POST':
        form = SimpleXmlImportForm(request.POST, request.FILES)
        if form.is_valid():
            saved_file = handle_uploads(request, ['xml_file',])['xml_file']
            xml_import(init_tree(saved_file))
    else:
        form = SimpleXmlImportForm()

    return render(request, 'virtenviro/shop/xmlimport.html', {'form': form,})


def init_tree(xml_file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(xml_file, parser)


def xml_import(tree):
    for xml_product in tree.findall('.//product'):
        xml_name = xml_product.find('name').text
        try:
            xml_category = xml_product.find('category').text
        except:
            xml_category = ''
        try:
            xml_description = xml_product.find('description').text
        except:
            xml_description = ''
        try:
            xml_manufacturer = xml_product.find('manufacturer').text
        except:
            xml_manufacturer = ''
        try:
            xml_articul = xml_product.find('articul').text
        except:
            xml_articul = id_generator(15)

        unique_code_string = '%s%s%s' % (xml_name, xml_manufacturer, xml_articul)
        unique_code = sha256(unique_code_string)

        if not xml_manufacturer == '':
            manufacturer, created = Manufacturer.objects.get_or_create(name=xml_manufacturer)
        else:
            manufacturer = None

        if not xml_category == '':
            category, created = Category.objects.get_or_create(name=xml_category, defaults={
                'parent': None
            })
        else:
            category = None
        '''
        product, created = Product.objects.get_or_create(unique_code=unique_code, defaults={
            'name': xml_name,
            'description': xml_description,
            'category': category,
            'manufacturer': manufacturer,
            'articul': xml_articul
        })
        for xml_image in xml_product.findall('photo'):
            xml_image_attribs = xml_image.attrib
            if xml_image_attribs.get('type', False):
                image_type, created = ImageType.objects.get_or_create(name=xml_image_attribs['type'])
            else:
                image_type = None
            if not category is None:
                image_type_category, created = ImageTypeCategoryRelation.objects.get_or_create(
                    image_type=image_type,
                    category=category,
                    defaults={
                        'max_count': 4
                    }
                )
            image = Image()
            image.name = product.name
            image.image = xml_image.text
            image.image_type = image_type
            image.product = product
            image.is_main = False if product.has_main_image() else True
            image.save()
        #todo: import properties
        for xml_property in xml_product.findall('property'):
            if xml_property.text:
                xml_property_attribs = xml_property.attrib
                property_type, created = PropertyType.objects.get_or_create(name=xml_property_attribs['name'], defults={
                    'data_type': xml_property_attribs.get('type', -3)
                })
                if category:
                    property_type_category_relation = PropertyTypeCategoryRelation.objects.get_or_create(
                        property_type=property_type,
                        category=category,
                        defaults={
                            'max_count': 1,
                        }
                    )

                property, created = Property.objects.get_or_create(
                    property_type=property_type,
                    value=xml_property.text,
                    product=product
                )
        '''

'''
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
'''
