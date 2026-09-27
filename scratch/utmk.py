# -*- coding: utf-8 -*-
"""Naver/Daum UTM-K -> WGS84 변환 (순수 파이썬, 표준 Snyder 역변환 + Bessel→WGS84 3파라미터).

UTM-K: TM lat0=38N, lon0=127.5E, k=0.9996, x0=1,000,000m, y0=2,000,000m, Bessel 1841.
Datum shift: towgs84 = 115.8, 474.99, 407.16 (한국 측지계 표준 3파라미터, 자전·축 스케일 0).
검증: 사당역 인근 남현동 지점 UTM-K (14135517.41, 4505507.14) → 서울 관악구 (약 37.48N, 126.99E) 기대.
"""
import math

A = 6377397.155          # Bessel 1841 semi-major
RF = 299.1528128
K0 = 0.9996
LAT0 = math.radians(38.0)
LON0 = math.radians(127.5)
X0 = 1000000.0
Y0 = 2000000.0
F = 1.0 / RF
B = A * (1.0 - F)                       # semi-minor
EP2 = (A * A - B * B) / (B * B)         # e'^2
E2 = F * (2.0 - F)                      # e^2
EP1 = E2 / (1.0 - E2)

DX, DY, DZ = 115.8, 474.99, 407.16
AW = 6378137.0; BW = 6356752.314245


def _ecef_to_geo(x, y, z, a, b):
    e2 = (a * a - b * b) / (a * a)
    ep2 = (a * a - b * b) / (b * b)
    p = math.hypot(x, y)
    th = math.atan2(z * a, p * b)
    lat = math.atan2(z + ep2 * b * math.sin(th) ** 3, p - e2 * a * math.cos(th) ** 3)
    lon = math.atan2(y, x)
    n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    alt = p / math.cos(lat) - n
    return lat, lon, alt


def _geo_to_ecef(lat, lon, h, a, b):
    e2 = (a * a - b * b) / (a * a)
    n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    return ((n + h) * math.cos(lat) * math.cos(lon),
            (n + h) * math.cos(lat) * math.sin(lon),
            (n * (1 - e2) + h) * math.sin(lat))


def tm_to_geo_bessel(x, y):
    """UTM-K (m) -> (lat, lon) radians on Bessel."""
    x -= X0
    y -= Y0
    M = y / K0
    e1 = (1 - math.sqrt(1 - E2)) / (1 + math.sqrt(1 - E2))
    mu = M / (B * (1 - E2 / 4 - 3 * E2 ** 2 / 64 - 5 * E2 ** 3 / 256))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + 151 * e1 ** 3 / 96 * math.sin(6 * mu)
            + 1097 * e1 ** 4 / 512 * math.sin(8 * mu))
    n1 = A / math.sqrt(1 - E2 * math.sin(phi1) ** 2)
    t1 = math.tan(phi1) ** 2
    c1 = EP2 * math.cos(phi1) ** 2
    r1 = A * (1 - E2) / (1 - E2 * math.sin(phi1) ** 2) ** 1.5
    d = x / (n1 * K0)
    lat = phi1 - (n1 * math.tan(phi1) / r1) * (
        d * d / 2
        - (5 + 3 * t1 + 10 * c1 - 4 * c1 * c1 - 9 * EP2) * d ** 4 / 24
        + (61 + 90 * t1 + 298 * c1 + 45 * t1 * t1 - 252 * EP2 - 3 * c1 * c1) * d ** 6 / 720)
    lon = LON0 + (d - (1 + 2 * t1 + c1) * d ** 3 / 6
                  + (5 - 2 * c1 + 28 * t1 - 3 * c1 * c1 + 8 * EP2 + 24 * t1 * t1) * d ** 5 / 120) / math.cos(phi1)
    return lat, lon


def utmk_to_wgs84(x, y):
    lat, lon = tm_to_geo_bessel(x, y)
    bx, by, bz = _geo_to_ecef(lat, lon, 0.0, A, B)
    lat2, lon2, _ = _ecef_to_geo(bx + DX, by + DY, bz + DZ, AW, BW)
    return math.degrees(lat2), math.degrees(lon2)


if __name__ == '__main__':
    # 검증 1: 코스 출발지(사당역 인근 남현동) — 서울 관악구 기대
    la, lo = utmk_to_wgs84(14135517.4118472, 4505507.1429765)
    print('P1(사당능선 기점): %.6f, %.6f' % (la, lo))
    # 검증 2: 관악로 1 (서울대입구역 인근 기대, 약 37.481, 126.953)
    la, lo = utmk_to_wgs84(14132222.1656766, 4502080.5075838)
    print('P2(관악로1): %.6f, %.6f' % (la, lo))
    # 검증 3: 서울 시청 WGS84(37.5666805,126.9784147) → 대략 (14131658, 4506640) 근방이어야
    la, lo = utmk_to_wgs84(14131658.0, 4506640.0)
    print('P3(시청 역산): %.6f, %.6f' % (la, lo))
