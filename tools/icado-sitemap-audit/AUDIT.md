# ICADO crawl and sitemap audit

- Research date: 2026-08-15T23:04:49+07:00
- Start URL: https://icado.vn/
- Crawled URLs: 245
- Indexable URLs in sitemap: 227
- Crawl duration: 88.8 seconds
- Existing `/robots.txt` and sitemap endpoints: rendered as site HTML/soft 404 during initial inspection

## Indexable URLs by inferred type

- article-index: 1
- category-or-landing: 105
- corporate: 5
- detail: 2
- home: 1
- policy: 6
- product: 107

## HTTP status summary

- 200: 233
- 404: 12

## Metadata findings

- Missing title: 0
- Missing meta description: 1
- Missing H1: 104
- Multiple H1: 2
- Missing canonical: 16
- Conflicting canonical: 0
- URLs participating in duplicate-title groups: 8
- Fetch errors: 12

### Missing title samples

- Không có

### Missing description samples

- https://icado.vn/ho-tro/quy-che-hoat-dong

### Missing H1 samples

- https://icado.vn/
- https://icado.vn/dai-ly
- https://icado.vn/gioi-thieu
- https://icado.vn/gym
- https://icado.vn/hit-tho-dung-cach-khi-tap-yoga-va-nhung-loi-ich-an-sau-do
- https://icado.vn/hop-tac-kinh-doanh
- https://icado.vn/ket-hop-tap-gym-va-tap-yoga
- https://icado.vn/nam
- https://icado.vn/new
- https://icado.vn/nu
- https://icado.vn/phu-kien
- https://icado.vn/pickleball
- https://icado.vn/running
- https://icado.vn/tap-yoga-nhung-van-de-thuong-gap-va-cach-khac-phuc
- https://icado.vn/tennis
- https://icado.vn/the-thao
- https://icado.vn/trekking
- https://icado.vn/yoga
- https://icado.vn/chan-thuong-tay-khi-tap-gym
- https://icado.vn/nhung-luu-y-khi-tap-hit-tho-yoga

### Conflicting canonical samples

- Không có

### Missing canonical samples

- https://icado.vn/
- https://icado.vn/dai-ly
- https://icado.vn/ebook
- https://icado.vn/ebook/5-bi-quyet-chon-do-the-thao
- https://icado.vn/ebook/khoi-nghiep-voi-do-the-thao
- https://icado.vn/gioi-thieu
- https://icado.vn/ho-tro/chinh-sach-bao-hanh
- https://icado.vn/ho-tro/chinh-sach-bao-mat
- https://icado.vn/ho-tro/chinh-sach-doi-tra
- https://icado.vn/ho-tro/giao-hang-va-thanh-toan
- https://icado.vn/ho-tro/huong-dan-mua-hang
- https://icado.vn/ho-tro/quy-che-hoat-dong
- https://icado.vn/hop-tac-kinh-doanh
- https://icado.vn/lien-he
- https://icado.vn/tin-tuc
- https://icado.vn/xuong-san-xuat

### Duplicate title groups

- `ICADO - Premium Sportswear`: https://icado.vn/dai-ly, https://icado.vn/ebook, https://icado.vn/ebook/5-bi-quyet-chon-do-the-thao, https://icado.vn/ebook/khoi-nghiep-voi-do-the-thao, https://icado.vn/hop-tac-kinh-doanh, https://icado.vn/lien-he
- `Áo Polo Nam | ICADO`: https://icado.vn/ao-polo-nam, https://icado.vn/ao-polo

### Fetch error samples

- https://icado.vn/ao-bra-the-thao-nu-icado-ht103
- https://icado.vn/ao-thun-the-thao-nam-icado-ht101
- https://icado.vn/ao-polo-the-thao-nam-high-class-icado-ht110
- https://icado.vn/ao-khoac-the-thao-nam-icado-at3
- https://icado.vn/ao-thun-the-thao-nu-icado-ht101
- https://icado.vn/chan-vay-the-thao-2-lop-nu-icado-ht101
- https://icado.vn/ao-polo-the-thao-nam-icado-ht102
- https://icado.vn/ao-thun-the-thao-nam-vien-vai-icado-at11
- https://icado.vn/quan-dui-the-thao-2-lop-nam-icado-at31
- https://icado.vn/quan-dui-the-thao-nam-2-lop-icado-at27
- https://icado.vn/ao-croptop-the-thao-tay-dai-nu-icado-ht103
- https://icado.vn/quan-legging-dai-the-thao-nu-icado-ht103

## Sitemap inclusion rules

Included only URLs that:

- returned HTTP 200;
- returned HTML;
- did not declare `noindex`;
- were not detected as soft 404;
- were self-canonical or had no canonical declaration;
- had no query parameters;
- were not auth, cart, checkout, account, API, static asset, PDF, or media URLs.

## Recommended deployment

1. Serve `sitemap.xml` at `https://icado.vn/sitemap.xml` with `application/xml`.
2. Add `Sitemap: https://icado.vn/sitemap.xml` to a real plain-text `robots.txt`.
3. Generate sitemap dynamically from active products/categories/articles so inventory changes are reflected automatically.
4. Use actual database `updated_at` values for `<lastmod>` instead of crawl date when implementing dynamically.
5. Keep filtered, sorted, searched, account, cart, and checkout URLs out of the sitemap.
