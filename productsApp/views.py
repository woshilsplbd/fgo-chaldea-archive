import time

from django.http import JsonResponse
from django.shortcuts import render


ATLAS_SERVANT_SEARCH_URL = 'https://api.atlasacademy.io/nice/JP/servant/search'
ATLAS_SERVANT_DETAIL_URL = 'https://api.atlasacademy.io/nice/JP/servant/{}'
MAX_LIMIT = 30
CACHE_SECONDS = 600

BASIC_CLASS_NAMES = (
    'saber',
    'archer',
    'lancer',
    'rider',
    'caster',
    'assassin',
    'berserker',
)
EXTRA_CLASS_NAMES = (
    'shielder',
    'ruler',
    'avenger',
    'moonCancer',
    'alterEgo',
    'foreigner',
    'pretender',
    'beast',
)
ALL_CLASS_NAMES = BASIC_CLASS_NAMES + EXTRA_CLASS_NAMES
CLASS_ALIASES = {
    'all': 'all',
    'saber': 'saber',
    'archer': 'archer',
    'lancer': 'lancer',
    'rider': 'rider',
    'caster': 'caster',
    'assassin': 'assassin',
    'berserker': 'berserker',
    'extra': 'extra',
}
_servant_cache = {}
_servant_detail_cache = {}


def _display_class_name(class_name):
    names = {
        'moonCancer': 'Moon Cancer',
        'alterEgo': 'Alter Ego',
        'shielder': 'Shielder',
        'ruler': 'Ruler',
        'avenger': 'Avenger',
        'foreigner': 'Foreigner',
        'pretender': 'Pretender',
        'beast': 'Beast',
    }
    if not class_name:
        return 'Unknown'
    return names.get(class_name, class_name[:1].upper() + class_name[1:])


def _find_first_image(value):
    if isinstance(value, str) and value.startswith('http'):
        return value
    if isinstance(value, list):
        for item in value:
            image = _find_first_image(item)
            if image:
                return image
    if isinstance(value, dict):
        for item in value.values():
            image = _find_first_image(item)
            if image:
                return image
    return ''


def _request_atlas(class_name):
    try:
        import requests

        response = requests.get(
            ATLAS_SERVANT_SEARCH_URL,
            params={'className': class_name},
            timeout=8,
        )
        response.raise_for_status()
        return response.json()
    except ImportError:
        import json
        from urllib.parse import urlencode
        from urllib.request import Request, urlopen

        url = '{}?{}'.format(
            ATLAS_SERVANT_SEARCH_URL,
            urlencode({'className': class_name}),
        )
        request = Request(url, headers={'User-Agent': 'ChaldeaArchive/1.0'})
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode('utf-8'))


def _request_atlas_detail(servant_id):
    detail_url = ATLAS_SERVANT_DETAIL_URL.format(servant_id)
    try:
        import requests

        response = requests.get(detail_url, params={'lore': 'true'}, timeout=8)
        response.raise_for_status()
        return response.json()
    except ImportError:
        import json
        from urllib.parse import urlencode
        from urllib.request import Request, urlopen

        url = '{}?{}'.format(detail_url, urlencode({'lore': 'true'}))
        request = Request(url, headers={'User-Agent': 'ChaldeaArchive/1.0'})
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode('utf-8'))


def _fetch_atlas_servants_by_class(class_name):
    now = time.time()
    cached = _servant_cache.get(class_name)
    if cached and now - cached['time'] < CACHE_SECONDS:
        return cached['data']

    data = _request_atlas(class_name)
    if not isinstance(data, list):
        data = []

    _servant_cache[class_name] = {
        'time': now,
        'data': data,
    }
    return data


def _fetch_atlas_servant_detail(servant_id):
    now = time.time()
    cached = _servant_detail_cache.get(servant_id)
    if cached and now - cached['time'] < CACHE_SECONDS:
        return cached['data']

    data = _request_atlas_detail(servant_id)
    if not isinstance(data, dict):
        data = {}

    _servant_detail_cache[servant_id] = {
        'time': now,
        'data': data,
    }
    return data


def _requested_classes(class_name):
    normalized = CLASS_ALIASES.get((class_name or 'all').strip().lower(), 'all')
    if normalized == 'all':
        return ALL_CLASS_NAMES
    if normalized == 'extra':
        return EXTRA_CLASS_NAMES
    return (normalized,)


def _servant_image(servant):
    extra_assets = servant.get('extraAssets') or {}

    image = _find_first_image(extra_assets.get('faces') or {})
    if image:
        return image

    for key in ('face', 'image', 'icon', 'thumbnail'):
        image = _find_first_image(servant.get(key))
        if image:
            return image

    return _find_first_image(extra_assets.get('image') or {})


def _servant_large_image(servant):
    extra_assets = servant.get('extraAssets') or {}
    chara_graph = extra_assets.get('charaGraph') or {}
    ascension = chara_graph.get('ascension') if isinstance(chara_graph, dict) else {}

    if isinstance(ascension, dict):
        for key in sorted(ascension.keys(), reverse=True):
            image = _find_first_image(ascension.get(key))
            if image:
                return image

    for key in ('charaGraph', 'charaFigure', 'image'):
        image = _find_first_image(extra_assets.get(key) or {})
        if image:
            return image

    return _servant_image(servant)


def _normalize_servant(servant):
    class_name = servant.get('className') or servant.get('classType') or ''
    if isinstance(class_name, dict):
        class_name = class_name.get('name') or class_name.get('id') or ''

    image = _servant_image(servant)
    return {
        'id': servant.get('id') or '',
        'name': servant.get('name') or servant.get('originalName') or '',
        'className': class_name,
        'classType': class_name,
        'displayClassName': _display_class_name(class_name),
        'rarity': servant.get('rarity') or 0,
        'rarityStars': '★' * int(servant.get('rarity') or 0) if servant.get('rarity') else '未记录',
        'face': image,
        'image': image,
        'collectionNo': servant.get('collectionNo') or servant.get('id') or '',
    }


def _servant_description(servant):
    profile = servant.get('profile') or {}
    comments = profile.get('comments') if isinstance(profile, dict) else []
    if isinstance(comments, list):
        for item in comments:
            comment = item.get('comment') if isinstance(item, dict) else ''
            if comment:
                return comment
    return '暂无简介。'


def _normalize_noble_phantasms(servant):
    noble_phantasms = servant.get('noblePhantasms') or []
    results = []
    for noble_phantasm in noble_phantasms:
        if not isinstance(noble_phantasm, dict):
            continue
        name = noble_phantasm.get('name') or noble_phantasm.get('originalName') or '未记录'
        results.append({
            'name': name,
            'rank': noble_phantasm.get('rank') or '未记录',
            'card': noble_phantasm.get('card') or '',
            'detail': noble_phantasm.get('detail') or noble_phantasm.get('unmodifiedDetail') or '',
        })
    return results


def _normalize_skills(servant):
    skills = servant.get('skills') or []
    results = []
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        results.append({
            'name': skill.get('name') or skill.get('originalName') or '未记录',
            'rank': skill.get('rank') or '未记录',
            'icon': skill.get('icon') or '',
            'detail': skill.get('detail') or '',
        })
    return results


def _normalize_servant_detail(servant):
    summary = _normalize_servant(servant)
    summary.update({
        'largeImage': _servant_large_image(servant),
        'noblePhantasms': _normalize_noble_phantasms(servant),
        'skills': _normalize_skills(servant),
        'description': _servant_description(servant),
    })
    return summary


def _parse_positive_int(value, default):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def servants_api(request):
    class_name = request.GET.get('className', 'All')
    search = (request.GET.get('search') or '').strip().lower()
    page = _parse_positive_int(request.GET.get('page'), 1)
    limit = min(_parse_positive_int(request.GET.get('limit'), MAX_LIMIT), MAX_LIMIT)

    try:
        raw_servants = []
        for atlas_class in _requested_classes(class_name):
            raw_servants.extend(_fetch_atlas_servants_by_class(atlas_class))
    except Exception:
        return JsonResponse({
            'ok': False,
            'message': '英灵资料加载失败，请检查网络或 requests 依赖',
            'results': [],
        }, status=502)

    servants_by_id = {}
    for servant in raw_servants:
        servant_id = servant.get('collectionNo') or servant.get('id')
        if servant_id:
            servants_by_id[servant_id] = servant

    normalized_servants = [_normalize_servant(servant) for servant in servants_by_id.values()]
    if search:
        normalized_servants = [
            servant for servant in normalized_servants
            if search in servant['name'].lower()
        ]

    normalized_servants.sort(key=lambda servant: int(servant['collectionNo'] or 0))

    total = len(normalized_servants)
    total_pages = max((total + limit - 1) // limit, 1)
    if page > total_pages:
        page = total_pages

    start = (page - 1) * limit
    end = start + limit

    return JsonResponse({
        'ok': True,
        'results': normalized_servants[start:end],
        'page': page,
        'limit': limit,
        'total': total,
        'totalPages': total_pages,
        'hasPrev': page > 1,
        'hasNext': page < total_pages,
        'className': class_name,
        'search': search,
    })


def products(request, productName):
    return render(request, 'productList.html', {
        'active_menu': 'products',
        'sub_menu': productName,
        'productName': '英灵资料',
    })


def servant_detail(request, id):
    try:
        servant = _normalize_servant_detail(_fetch_atlas_servant_detail(id))
    except Exception:
        servant = None

    return render(request, 'productDetail.html', {
        'active_menu': 'products',
        'servant': servant,
    })


def productDetail(request, id):
    return servant_detail(request, id)
