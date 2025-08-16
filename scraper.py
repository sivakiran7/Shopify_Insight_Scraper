import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from models import Product, FAQ, BrandContext


class ShopifyScraper:

    def __init__(self, base_url: str):
        if not base_url.startswith("http"):
            base_url = "https://" + base_url
        self.base_url = base_url.rstrip("/")

    def fetch_html(self, path: str = "") -> BeautifulSoup:
        url = urljoin(self.base_url, path)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")

    def fetch_json(self, path: str):
        url = urljoin(self.base_url, path)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_products(self) -> list[Product]:
        try:
            data = self.fetch_json("/products.json")
            products = []
            for p in data.get("products", []):
                products.append(Product(
                    title=p.get("title"),
                    handle=p.get("handle"),
                    price=(p.get("variants", [{}])[0].get("price")),
                    image=(p.get("images", [{}])[0].get("src")),
                    url=urljoin(self.base_url, f"/products/{p.get('handle')}")
                ))
            return products
        except Exception:
            return []

    def get_hero_products(self) -> list[Product]:
        try:
            soup = self.fetch_html("/")
            products = []
            for a in soup.select("a[href*='/products/']")[:10]:
                title = a.get_text(strip=True)
                href = urljoin(self.base_url, a["href"])
                products.append(Product(title=title, handle=None, price=None, image=None, url=href))
            return products
        except Exception:
            return []

    def extract_text_from_page(self, path: str) -> str | None:
        try:
            soup = self.fetch_html(path)
            return soup.get_text(" ", strip=True)
        except Exception:
            return None

    def get_policies(self):
        return {
            "privacy_policy": self.extract_text_from_page("/policies/privacy-policy"),
            "return_refund_policy": self.extract_text_from_page("/policies/refund-policy")
        }

    def get_faqs(self) -> list[FAQ]:
        try:
            soup = self.fetch_html("/pages/faq")
            faqs = []
            for q in soup.find_all(["h2", "h3"]):
                answer = q.find_next("p")
                if answer:
                    faqs.append(FAQ(question=q.get_text(strip=True), answer=answer.get_text(strip=True)))
            return faqs
        except Exception:
            return []

    def get_social_handles(self) -> list[str]:
        soup = self.fetch_html("/")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        socials = [l for l in links if any(s in l for s in ["facebook", "instagram", "tiktok", "twitter", "youtube"])]
        return socials

    def get_contact_details(self) -> list[str]:
        soup = self.fetch_html("/pages/contact")
        text = soup.get_text(" ", strip=True)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        phones = re.findall(r"\+?\d[\d\-\s]{7,}\d", text)
        return list(set(emails + phones))

    def get_about(self) -> str | None:
        return self.extract_text_from_page("/pages/about")

    def get_important_links(self) -> list[str]:
        soup = self.fetch_html("/")
        return [urljoin(self.base_url, a["href"]) for a in soup.find_all("a", href=True)
                if any(x in a["href"].lower() for x in ["contact", "blog", "track", "about"])]

    def get_brand_name(self) -> str | None:
        soup = self.fetch_html("/")
        if soup.title:
            return soup.title.string.strip()
        return None

    def get_brand_context(self) -> BrandContext:
        policies = self.get_policies()
        return BrandContext(
            brand_name=self.get_brand_name(),
            products=self.get_products(),
            hero_products=self.get_hero_products(),
            privacy_policy=policies["privacy_policy"],
            return_refund_policy=policies["return_refund_policy"],
            faqs=self.get_faqs(),
            social_handles=self.get_social_handles(),
            contact_details=self.get_contact_details(),
            about=self.get_about(),
            important_links=self.get_important_links()
        )
