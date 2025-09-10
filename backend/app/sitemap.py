import logging
from datetime import datetime

from flask import Blueprint, Response, url_for

from .models import Product

bp = Blueprint('sitemap', __name__)
logger = logging.getLogger(__name__)


@bp.route('/sitemap.xml', methods=('GET',))
def sitemap():
    try:
        pages = []

        # Статические страницы
        static_pages = (
            'main.index', 'main.products', 'main.about', 'main.contacts'
        )
        for page in static_pages:
            pages.append({
                'loc': url_for(page, _external=True),
                'lastmod': datetime.now().date()
            })

        # Динамические страницы продуктов
        for product in Product.query.all():
            pages.append({
                'loc': url_for(
                    'main.product_detail',
                    product_id=product.id,
                    _external=True
                ),
                'lastmod': datetime.now().date()
            })

        # Генерация XML
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += (
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        )

        for page in pages:
            sitemap_xml += f"""  <url>
            <loc>{page['loc']}</loc>
            <lastmod>{page['lastmod']}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>
        """

        sitemap_xml += '</urlset>'

        return Response(sitemap_xml, mimetype='application/xml')
    except Exception as e:
        logger.error('Ошибка генерации sitemap.xml: %s', e)
