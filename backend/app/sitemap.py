from datetime import datetime

from flask import Blueprint, Response, url_for

from .models import Product

bp = Blueprint('sitemap', __name__)


@bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []

    # Статические страницы
    static_pages = ['main.index', 'main.products', 'main.about', 'main.contacts']
    for page in static_pages:
        pages.append({
            'loc': url_for(page, _external=True),
            'lastmod': datetime.now().date()
        })

    # Динамические страницы продуктов
    for product in Product.query.all():
        pages.append({
            'loc': url_for('product_detail', product_id=product.id, _external=True),
            'lastmod': datetime.now().date()
        })

    # 3. Генерация XML
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        sitemap_xml += f'  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        sitemap_xml += f'    <changefreq>monthly</changefreq>\n'
        sitemap_xml += f'    <priority>0.8</priority>\n'
        sitemap_xml += f'  </url>\n'

    sitemap_xml += '</urlset>'

    return Response(sitemap_xml, mimetype='application/xml')
