#!/usr/bin/env python3
"""
COMPREHENSIVE PROFESSIONAL SALES BROCHURE SCRAPER
Extracts maximum high-quality data for creating detailed sales brochures
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
from typing import Dict, List, Set, Optional
import time
from collections import defaultdict

# ============================================
# CONFIGURATION
# ============================================
TARGET_URL = "https://www.apple.com/in/store?afid=p240%7Cgo~cmp-11116556120~adg-109516736379~ad-780589622285_kwd-10778630~dev-c~ext-~prd-~mca-~nt-search&cid=aos-in-kwgo-txt-brand-brand--"
MAX_PAGES = 10  # Increased for more comprehensive scraping
OUTPUT_FILE = "comprehensive_brochure_data.json"
DELAY_BETWEEN_REQUESTS = 1  # seconds
# ============================================

class ComprehensiveBrochureScraper:
    def __init__(self, url: str):
        self.base_url = url
        self.domain = urlparse(url).netloc
        self.data = {
            # Company Identity
            'company_identity': {
                'company_name': '',
                'legal_name': '',
                'taglines': [],
                'brand_statements': [],
                'logo_url': '',
                'alternative_logos': [],
                'favicon': '',
                'year_founded': '',
                'headquarters': ''
            },
            
            # Visual Assets
            'visual_assets': {
                'hero_images': [],
                'banner_images': [],
                'background_images': [],
                'product_images': [],
                'team_photos': [],
                'office_images': [],
                'infographics': [],
                'all_high_quality_images': []
            },
            
            # Company Story & About
            'about_company': {
                'company_overview': [],
                'detailed_description': '',
                'company_story': '',
                'history': [],
                'mission_statements': [],
                'vision_statements': [],
                'core_values': [],
                'company_culture': [],
                'philosophy': [],
                'commitments': []
            },
            
            # Products & Services
            'offerings': {
                'services': [],
                'products': [],
                'solutions': [],
                'industries_served': [],
                'specializations': [],
                'service_categories': [],
                'product_lines': []
            },
            
            # Unique Selling Propositions
            'competitive_advantages': {
                'unique_selling_points': [],
                'differentiators': [],
                'benefits': [],
                'why_choose_us': [],
                'competitive_edges': [],
                'guarantees': [],
                'promises': []
            },
            
            # Numbers & Statistics
            'metrics_and_stats': {
                'key_statistics': [],
                'achievements': [],
                'milestones': [],
                'growth_numbers': [],
                'performance_metrics': [],
                'market_presence': []
            },
            
            # People & Team
            'team_and_leadership': {
                'executives': [],
                'leadership_team': [],
                'board_members': [],
                'key_personnel': [],
                'team_size': '',
                'expertise_areas': []
            },
            
            # Credibility & Trust
            'credibility': {
                'awards': [],
                'certifications': [],
                'accreditations': [],
                'recognitions': [],
                'partnerships': [],
                'affiliations': [],
                'compliance': [],
                'quality_standards': []
            },
            
            # Social Proof
            'social_proof': {
                'client_testimonials': [],
                'customer_reviews': [],
                'case_studies': [],
                'success_stories': [],
                'client_list': [],
                'portfolio_items': [],
                'project_highlights': []
            },
            
            # Technology & Innovation
            'technology': {
                'technologies_used': [],
                'innovations': [],
                'research_development': [],
                'patents': [],
                'proprietary_solutions': [],
                'technical_capabilities': []
            },
            
            # Market Position
            'market_presence': {
                'markets_served': [],
                'geographic_coverage': [],
                'office_locations': [],
                'service_areas': [],
                'global_presence': [],
                'market_position': []
            },
            
            # Process & Methodology
            'how_we_work': {
                'process_steps': [],
                'methodology': [],
                'approach': [],
                'workflow': [],
                'best_practices': []
            },
            
            # Features & Capabilities
            'features_capabilities': {
                'key_features': [],
                'capabilities': [],
                'specialties': [],
                'expertise': [],
                'service_highlights': []
            },
            
            # Pricing & Plans (if available)
            'pricing_info': {
                'pricing_models': [],
                'plans': [],
                'packages': [],
                'pricing_features': []
            },
            
            # Resources & Support
            'support_resources': {
                'support_options': [],
                'resources': [],
                'documentation': [],
                'training': [],
                'community': []
            },
            
            # Contact & Communication
            'contact_information': {
                'primary_email': '',
                'department_emails': [],
                'phone_numbers': [],
                'fax_numbers': [],
                'toll_free_numbers': [],
                'support_contacts': [],
                'sales_contacts': [],
                'addresses': [],
                'office_hours': [],
                'contact_forms': []
            },
            
            # Digital Presence
            'online_presence': {
                'website_url': url,
                'social_media': {},
                'professional_networks': {},
                'review_platforms': {},
                'app_links': {},
                'online_stores': []
            },
            
            # Media & Press
            'media': {
                'press_releases': [],
                'news_mentions': [],
                'media_coverage': [],
                'publications': [],
                'featured_in': [],
                'press_kit': []
            },
            
            # Call to Actions
            'calls_to_action': {
                'primary_cta': '',
                'secondary_ctas': [],
                'contact_ctas': [],
                'demo_trial_ctas': [],
                'download_ctas': []
            },
            
            # Additional Content
            'additional_content': {
                'faqs': [],
                'key_messages': [],
                'slogans': [],
                'brand_voice': [],
                'content_themes': []
            }
        }
        
        self.visited_urls = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage with error handling"""
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"⚠ Error fetching {url}: {str(e)[:100]}")
            return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ''
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = text.strip()
        return text
    
    def extract_all_text_by_headings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract all text content organized by headings"""
        content = []
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get all headings with their content
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = self.clean_text(heading.get_text())
            if not heading_text or len(heading_text) < 3:
                continue
            
            # Get all text until next heading
            content_parts = []
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if sibling.name in ['p', 'ul', 'ol', 'div', 'section']:
                    text = self.clean_text(sibling.get_text())
                    if text and len(text) > 20:
                        content_parts.append(text)
            
            if content_parts:
                content.append({
                    'heading': heading_text,
                    'level': heading.name,
                    'content': ' '.join(content_parts),
                    'content_length': len(' '.join(content_parts))
                })
        
        return content
    
    def extract_company_identity(self, soup: BeautifulSoup):
        """Extract comprehensive company identity information"""
        # Company name from multiple sources
        logo_img = soup.find('img', {'alt': re.compile(r'logo', re.I)})
        if logo_img:
            name = logo_img.get('alt', '').replace(' logo', '').replace(' Logo', '')
            if name:
                self.data['company_identity']['company_name'] = name
        
        # From title tag
        if soup.title:
            title_parts = soup.title.string.split('|')
            if not self.data['company_identity']['company_name'] and title_parts:
                self.data['company_identity']['company_name'] = title_parts[0].strip()
        
        # Logo URLs
        logos = soup.find_all('img', {'alt': re.compile(r'logo', re.I)})
        logos += soup.find_all('img', {'class': re.compile(r'logo', re.I)})
        for logo in logos[:5]:
            logo_url = urljoin(self.base_url, logo.get('src', ''))
            if logo_url and logo_url not in self.data['company_identity']['alternative_logos']:
                if not self.data['company_identity']['logo_url']:
                    self.data['company_identity']['logo_url'] = logo_url
                else:
                    self.data['company_identity']['alternative_logos'].append(logo_url)
        
        # Favicon
        favicon = soup.find('link', {'rel': re.compile(r'icon', re.I)})
        if favicon and favicon.get('href'):
            self.data['company_identity']['favicon'] = urljoin(self.base_url, favicon['href'])
        
        # Taglines and brand statements
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content')
            self.data['company_identity']['taglines'].append(desc)
        
        # Look for taglines in hero sections
        hero_sections = soup.find_all(['section', 'div'], class_=re.compile(r'hero|banner|jumbotron', re.I))
        for hero in hero_sections:
            tagline_elem = hero.find(['h1', 'h2', 'p'], class_=re.compile(r'tagline|subtitle|headline', re.I))
            if tagline_elem:
                tagline = self.clean_text(tagline_elem.get_text())
                if tagline and len(tagline) < 200 and tagline not in self.data['company_identity']['taglines']:
                    self.data['company_identity']['taglines'].append(tagline)
        
        # Year founded
        year_patterns = [
            r'(?:founded|established|since)\s+(?:in\s+)?(\d{4})',
            r'(\d{4})\s+(?:-\s+present|to\s+present)',
        ]
        text = soup.get_text()
        for pattern in year_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                self.data['company_identity']['year_founded'] = match.group(1)
                break
    
    def extract_visual_assets(self, soup: BeautifulSoup):
        """Extract all high-quality images for brochure"""
        all_images = soup.find_all('img')
        
        for img in all_images:
            src = img.get('src', '') or img.get('data-src', '') or img.get('data-lazy-src', '')
            if not src:
                continue
            
            full_url = urljoin(self.base_url, src)
            alt = self.clean_text(img.get('alt', ''))
            title = self.clean_text(img.get('title', ''))
            
            # Determine image type and categorize
            img_data = {
                'url': full_url,
                'alt': alt,
                'title': title,
                'context': ''
            }
            
            # Check parent elements for context
            parent = img.find_parent(['section', 'div', 'article'])
            if parent:
                parent_class = ' '.join(parent.get('class', [])).lower()
                parent_id = parent.get('id', '').lower()
                img_data['context'] = parent_class + ' ' + parent_id
            
            # Categorize images
            context_lower = img_data['context'].lower() + ' ' + alt.lower()
            
            if re.search(r'hero|banner|header|main-banner', context_lower):
                self.data['visual_assets']['hero_images'].append(img_data)
            elif re.search(r'product|item|catalog', context_lower):
                self.data['visual_assets']['product_images'].append(img_data)
            elif re.search(r'team|staff|employee|person|member', context_lower):
                self.data['visual_assets']['team_photos'].append(img_data)
            elif re.search(r'office|building|location|facility', context_lower):
                self.data['visual_assets']['office_images'].append(img_data)
            elif re.search(r'banner|slide|carousel', context_lower):
                self.data['visual_assets']['banner_images'].append(img_data)
            
            # Add to all images if high quality (not icons/logos)
            if 'logo' not in alt.lower() and 'icon' not in alt.lower():
                if img_data not in self.data['visual_assets']['all_high_quality_images']:
                    self.data['visual_assets']['all_high_quality_images'].append(img_data)
    
    def extract_about_content(self, soup: BeautifulSoup):
        """Extract comprehensive about/company information"""
        # Company overview
        about_keywords = ['about', 'company', 'who we are', 'overview', 'introduction']
        
        for keyword in about_keywords:
            sections = soup.find_all(['section', 'div'], class_=re.compile(keyword.replace(' ', '[-_]?'), re.I))
            sections += soup.find_all(['section', 'div'], id=re.compile(keyword.replace(' ', '[-_]?'), re.I))
            
            for section in sections:
                # Get all paragraphs
                paragraphs = section.find_all('p')
                for p in paragraphs:
                    text = self.clean_text(p.get_text())
                    if text and len(text) > 100:
                        if text not in self.data['about_company']['company_overview']:
                            self.data['about_company']['company_overview'].append(text)
                
                # Get complete section text
                section_text = self.clean_text(section.get_text())
                if section_text and len(section_text) > 200:
                    if not self.data['about_company']['detailed_description']:
                        self.data['about_company']['detailed_description'] = section_text
        
        # Mission
        mission_keywords = ['mission', 'our mission']
        for keyword in mission_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for elem in elements:
                parent = elem.find_parent(['div', 'section', 'p', 'article'])
                if parent:
                    text = self.clean_text(parent.get_text())
                    if text and 50 < len(text) < 1000:
                        if text not in self.data['about_company']['mission_statements']:
                            self.data['about_company']['mission_statements'].append(text)
        
        # Vision
        vision_keywords = ['vision', 'our vision']
        for keyword in vision_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for elem in elements:
                parent = elem.find_parent(['div', 'section', 'p', 'article'])
                if parent:
                    text = self.clean_text(parent.get_text())
                    if text and 50 < len(text) < 1000:
                        if text not in self.data['about_company']['vision_statements']:
                            self.data['about_company']['vision_statements'].append(text)
        
        # Values
        values_sections = soup.find_all(['section', 'div'], class_=re.compile(r'values|principles|beliefs', re.I))
        values_sections += soup.find_all(['section', 'div'], id=re.compile(r'values|principles', re.I))
        
        for section in values_sections:
            # Get list items
            items = section.find_all('li')
            for item in items:
                value_text = self.clean_text(item.get_text())
                if value_text and 10 < len(value_text) < 500:
                    if value_text not in self.data['about_company']['core_values']:
                        self.data['about_company']['core_values'].append(value_text)
            
            # Get divs/cards
            cards = section.find_all(['div', 'article'], class_=re.compile(r'value|principle|item', re.I))
            for card in cards:
                value_text = self.clean_text(card.get_text())
                if value_text and 20 < len(value_text) < 500:
                    if value_text not in self.data['about_company']['core_values']:
                        self.data['about_company']['core_values'].append(value_text)
        
        # Company culture
        culture_sections = soup.find_all(['section', 'div'], class_=re.compile(r'culture|workplace|environment', re.I))
        for section in culture_sections:
            text = self.clean_text(section.get_text())
            if text and len(text) > 100:
                self.data['about_company']['company_culture'].append(text)
        
        # History and story
        history_sections = soup.find_all(['section', 'div'], class_=re.compile(r'history|story|journey|timeline', re.I))
        for section in history_sections:
            items = section.find_all(['div', 'li', 'article'])
            for item in items:
                text = self.clean_text(item.get_text())
                if text and 50 < len(text) < 1000:
                    self.data['about_company']['history'].append(text)
    
    def extract_offerings(self, soup: BeautifulSoup):
        """Extract all services, products, and solutions"""
        # Services
        service_sections = soup.find_all(['section', 'div'], class_=re.compile(r'service|solution|offering|what-we-do', re.I))
        service_sections += soup.find_all(['section', 'div'], id=re.compile(r'service|solution|offering', re.I))
        
        seen_services = set()
        for section in service_sections:
            # Get service items
            items = section.find_all(['div', 'li', 'article'], class_=re.compile(r'item|card|service|solution|feature', re.I))
            
            for item in items:
                title_elem = item.find(['h2', 'h3', 'h4', 'h5', 'strong', 'b'])
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    
                    if title and title not in seen_services and len(title) < 200:
                        seen_services.add(title)
                        
                        # Get full description
                        desc_parts = []
                        for p in item.find_all('p'):
                            desc_parts.append(self.clean_text(p.get_text()))
                        
                        description = ' '.join(desc_parts) if desc_parts else self.clean_text(item.get_text())
                        
                        # Get icon/image
                        icon = item.find('img')
                        icon_url = urljoin(self.base_url, icon['src']) if icon and icon.get('src') else ''
                        
                        # Get link if available
                        link_elem = item.find('a', href=True)
                        link = urljoin(self.base_url, link_elem['href']) if link_elem else ''
                        
                        service_data = {
                            'title': title,
                            'description': description[:1000],  # More content
                            'icon': icon_url,
                            'link': link
                        }
                        
                        # Categorize
                        if 'product' in item.get('class', []) or 'product' in str(item).lower():
                            self.data['offerings']['products'].append(service_data)
                        elif 'solution' in item.get('class', []) or 'solution' in str(item).lower():
                            self.data['offerings']['solutions'].append(service_data)
                        else:
                            self.data['offerings']['services'].append(service_data)
        
        # Product sections
        product_sections = soup.find_all(['section', 'div'], class_=re.compile(r'product|catalog|showcase', re.I))
        
        seen_products = set()
        for section in product_sections:
            products = section.find_all(['div', 'article', 'li'], class_=re.compile(r'product|item|card', re.I))
            
            for product in products:
                title_elem = product.find(['h2', 'h3', 'h4'])
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    
                    if title and title not in seen_products and len(title) < 200:
                        seen_products.add(title)
                        
                        # Get image
                        img = product.find('img')
                        img_url = urljoin(self.base_url, img['src']) if img and img.get('src') else ''
                        
                        # Get description
                        desc_elem = product.find('p')
                        description = self.clean_text(desc_elem.get_text()) if desc_elem else ''
                        
                        # Get price
                        price_elem = product.find(['span', 'div'], class_=re.compile(r'price', re.I))
                        price = self.clean_text(price_elem.get_text()) if price_elem else ''
                        
                        # Get features
                        features = []
                        feature_list = product.find(['ul', 'ol'])
                        if feature_list:
                            for li in feature_list.find_all('li'):
                                features.append(self.clean_text(li.get_text()))
                        
                        product_data = {
                            'name': title,
                            'description': description,
                            'image': img_url,
                            'price': price,
                            'features': features
                        }
                        
                        if product_data not in self.data['offerings']['products']:
                            self.data['offerings']['products'].append(product_data)
        
        # Industries served
        industry_sections = soup.find_all(['section', 'div'], class_=re.compile(r'industr|sector|vertical', re.I))
        for section in industry_sections:
            items = section.find_all(['li', 'div'], class_=re.compile(r'industr|sector|item', re.I))
            for item in items:
                text = self.clean_text(item.get_text())
                if text and 5 < len(text) < 200:
                    if text not in self.data['offerings']['industries_served']:
                        self.data['offerings']['industries_served'].append(text)
    
    def extract_usps_and_benefits(self, soup: BeautifulSoup):
        """Extract unique selling points and competitive advantages"""
        usp_keywords = [
            'why choose', 'why us', 'benefits', 'advantages', 'what makes us', 
            'differentiator', 'competitive edge', 'unique', 'better', 'guarantee'
        ]
        
        for keyword in usp_keywords:
            sections = soup.find_all(['section', 'div'], class_=re.compile(keyword.replace(' ', '[-_]?'), re.I))
            sections += soup.find_all(['section', 'div'], id=re.compile(keyword.replace(' ', '[-_]?'), re.I))
            
            for section in sections:
                items = section.find_all(['li', 'div', 'article', 'p'])
                
                for item in items:
                    # Get title if exists
                    title_elem = item.find(['h3', 'h4', 'h5', 'strong', 'b'])
                    title = self.clean_text(title_elem.get_text()) if title_elem else ''
                    
                    # Get full text
                    text = self.clean_text(item.get_text())
                    
                    if text and 30 < len(text) < 800:
                        usp_data = {
                            'title': title if title else text[:100] + '...' if len(text) > 100 else text,
                            'description': text,
                            'category': keyword
                        }
                        
                        # Categorize by keyword
                        if 'benefit' in keyword:
                            if usp_data not in self.data['competitive_advantages']['benefits']:
                                self.data['competitive_advantages']['benefits'].append(usp_data)
                        elif 'guarantee' in keyword:
                            if usp_data not in self.data['competitive_advantages']['guarantees']:
                                self.data['competitive_advantages']['guarantees'].append(usp_data)
                        elif 'why' in keyword:
                            if usp_data not in self.data['competitive_advantages']['why_choose_us']:
                                self.data['competitive_advantages']['why_choose_us'].append(usp_data)
                        else:
                            if usp_data not in self.data['competitive_advantages']['unique_selling_points']:
                                self.data['competitive_advantages']['unique_selling_points'].append(usp_data)
    
    def extract_statistics_and_achievements(self, soup: BeautifulSoup):
        """Extract impressive numbers, statistics, and achievements"""
        # Stats sections
        stat_sections = soup.find_all(['section', 'div'], class_=re.compile(r'stat|number|counter|achievement|metric|milestone', re.I))
        
        for section in stat_sections:
            items = section.find_all(['div', 'li', 'article'], class_=re.compile(r'stat|number|counter|achievement|metric', re.I))
            
            for item in items:
                # Look for number
                number_elem = item.find(['span', 'h2', 'h3', 'strong'], class_=re.compile(r'number|count|value|stat', re.I))
                if not number_elem:
                    number_elem = item.find(['span', 'h2', 'h3', 'div'])
                
                # Look for label
                label_elem = item.find(['p', 'span', 'div'], class_=re.compile(r'label|title|description|text', re.I))
                
                if number_elem:
                    number = self.clean_text(number_elem.get_text())
                    label = self.clean_text(label_elem.get_text()) if label_elem else self.clean_text(item.get_text())
                    
                    # Check if contains numbers
                    if re.search(r'[\d,+%]', number):
                        stat_data = {
                            'value': number,
                            'label': label,
                            'full_text': self.clean_text(item.get_text())
                        }
                        
                        if stat_data not in self.data['metrics_and_stats']['key_statistics']:
                            self.data['metrics_and_stats']['key_statistics'].append(stat_data)
        
        # Achievements and milestones
        achievement_sections = soup.find_all(['section', 'div'], class_=re.compile(r'achievement|milestone|accomplishment|success', re.I))
        
        for section in achievement_sections:
            items = section.find_all(['li', 'div', 'article'])
            for item in items:
                text = self.clean_text(item.get_text())
                if text and 20 < len(text) < 500:
                    if text not in self.data['metrics_and_stats']['achievements']:
                        self.data['metrics_and_stats']['achievements'].append(text)
    
    def extract_team_and_leadership(self, soup: BeautifulSoup):
        """Extract comprehensive team information"""
        team_sections = soup.find_all(['section', 'div'], class_=re.compile(r'team|leadership|management|staff|people|executive', re.I))
        
        seen_names = set()
        for section in team_sections:
            members = section.find_all(['div', 'article', 'li'], class_=re.compile(r'member|person|profile|team-member|executive|leader', re.I))
            
            for member in members:
                name_elem = member.find(['h2', 'h3', 'h4', 'h5', 'strong', 'b'])
                if name_elem:
                    name = self.clean_text(name_elem.get_text())
                    
                    if name and name not in seen_names and len(name) < 100:
                        seen_names.add(name)
                        
                        # Get role
                        role_elem = member.find(['span', 'p', 'div'], class_=re.compile(r'role|title|position|designation|job', re.I))
                        role = self.clean_text(role_elem.get_text()) if role_elem else ''
                        
                        # Get photo
                        img = member.find('img')
                        photo_url = urljoin(self.base_url, img['src']) if img and img.get('src') else ''
                        
                        # Get bio
                        bio_elem = member.find('p', class_=re.compile(r'bio|description|about', re.I))
                        if not bio_elem:
                            bio_elem = member.find('p')
                        bio = self.clean_text(bio_elem.get_text()) if bio_elem else ''
                        
                        # Get social links
                        social_links = {}
                        linkedin = member.find('a', href=re.compile(r'linkedin', re.I))
                        if linkedin:
                            social_links['linkedin'] = linkedin['href']
                        
                        member_data = {
                            'name': name,
                            'role': role,
                            'photo': photo_url,
                            'bio': bio,
                            'social_links': social_links
                        }
                        
                        # Categorize by role
                        role_lower = role.lower()
                        if any(title in role_lower for title in ['ceo', 'cto', 'cfo', 'coo', 'president', 'founder']):
                            self.data['team_and_leadership']['executives'].append(member_data)
                        elif any(title in role_lower for title in ['director', 'vp', 'vice president', 'head']):
                            self.data['team_and_leadership']['leadership_team'].append(member_data)
                        elif 'board' in role_lower:
                            self.data['team_and_leadership']['board_members'].append(member_data)
                        else:
                            self.data['team_and_leadership']['key_personnel'].append(member_data)
    
    def extract_credibility_markers(self, soup: BeautifulSoup):
        """Extract awards, certifications, partnerships"""
        # Awards
        award_sections = soup.find_all(['section', 'div'], class_=re.compile(r'award|recognition|accolade', re.I))
        
        for section in award_sections:
            items = section.find_all(['div', 'li', 'article'])
            for item in items:
                text = self.clean_text(item.get_text())
                if text and 10 < len(text) < 300:
                    # Get image/badge
                    img = item.find('img')
                    badge_url = urljoin(self.base_url, img['src']) if img and img.get('src') else ''
                    
                    award_data = {
                        'title': text,
                        'badge': badge_url,
                        'year': re.search(r'\b(19|20)\d{2}\b', text).group() if re.search(r'\b(19|20)\d{2}\b', text) else ''
                    }
                    
                    if award_data not in self.data['credibility']['awards']:
                        self.data['credibility']['awards'].append(award_data)
        
        # Certifications
        cert_sections = soup.find_all(['section', 'div'], class_=re.compile(r'certification|accreditation|compliance|standard', re.I))
        
        for section in cert_sections:
            items = section.find_all(['div', 'li', 'img'])
            for item in items:
                cert_data = None  # ✅ CRITICAL FIX

                if item.name == 'img':
                    cert_data = {
                        'title': self.clean_text(item.get('alt', '')),
                        'badge': urljoin(self.base_url, item.get('src', ''))
                    }
                else:
                    text = self.clean_text(item.get_text())
                    if text and 5 < len(text) < 200:
                        cert_data = {
                            'title': text,
                            'badge': ''
                        }

                # ✅ safe check
                if cert_data and cert_data.get('title') and cert_data not in self.data['credibility']['certifications']:
                    self.data['credibility']['certifications'].append(cert_data)        
        # Partnerships
        partner_sections = soup.find_all(['section', 'div'], class_=re.compile(r'partner|alliance|collaboration', re.I))
        
        for section in partner_sections:
            items = section.find_all(['div', 'li', 'img'])
            for item in items:
                if item.name == 'img':
                    partner_name = self.clean_text(item.get('alt', ''))
                    partner_logo = urljoin(self.base_url, item.get('src', ''))
                else:
                    partner_name = self.clean_text(item.get_text())
                    partner_logo = ''
                
                if partner_name and len(partner_name) < 100:
                    partner_data = {
                        'name': partner_name,
                        'logo': partner_logo
                    }
                    if partner_data not in self.data['credibility']['partnerships']:
                        self.data['credibility']['partnerships'].append(partner_data)
    
    def extract_social_proof(self, soup: BeautifulSoup):
        """Extract testimonials, reviews, case studies"""
        # Testimonials
        testimonial_sections = soup.find_all(['section', 'div'], class_=re.compile(r'testimonial|review|feedback|client-say|customer-say', re.I))
        
        for section in testimonial_sections:
            items = section.find_all(['div', 'blockquote', 'article'], class_=re.compile(r'testimonial|review|quote|feedback', re.I))
            
            for item in items:
                # Get quote
                quote_elem = item.find(['p', 'blockquote', 'q'])
                if quote_elem:
                    quote = self.clean_text(quote_elem.get_text())
                    
                    if quote and 30 < len(quote) < 1000:
                        # Get author
                        author_elem = item.find(['cite', 'span', 'strong', 'h4', 'h5'], class_=re.compile(r'author|name|client|customer', re.I))
                        author = self.clean_text(author_elem.get_text()) if author_elem else 'Anonymous'
                        
                        # Get role/company
                        role_elem = item.find(['span', 'p'], class_=re.compile(r'role|title|company|position|organization', re.I))
                        role = self.clean_text(role_elem.get_text()) if role_elem else ''
                        
                        # Get photo
                        img = item.find('img')
                        photo_url = urljoin(self.base_url, img['src']) if img and img.get('src') else ''
                        
                        # Get rating if available
                        rating_elem = item.find(['div', 'span'], class_=re.compile(r'rating|stars', re.I))
                        rating = self.clean_text(rating_elem.get_text()) if rating_elem else ''
                        
                        testimonial_data = {
                            'quote': quote,
                            'author': author,
                            'role': role,
                            'photo': photo_url,
                            'rating': rating
                        }
                        
                        if testimonial_data not in self.data['social_proof']['client_testimonials']:
                            self.data['social_proof']['client_testimonials'].append(testimonial_data)
        
        # Case studies
        case_sections = soup.find_all(['section', 'div'], class_=re.compile(r'case-stud|success-stor|portfolio|project', re.I))
        
        for section in case_sections:
            cases = section.find_all(['div', 'article'], class_=re.compile(r'case|study|story|project|portfolio', re.I))
            
            for case in cases:
                title_elem = case.find(['h2', 'h3', 'h4'])
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    
                    # Get summary/description
                    summary_parts = []
                    for p in case.find_all('p'):
                        summary_parts.append(self.clean_text(p.get_text()))
                    summary = ' '.join(summary_parts)
                    
                    # Get image
                    img = case.find('img')
                    img_url = urljoin(self.base_url, img['src']) if img and img.get('src') else ''
                    
                    # Get client
                    client_elem = case.find(['span', 'strong'], class_=re.compile(r'client|company|customer', re.I))
                    client = self.clean_text(client_elem.get_text()) if client_elem else ''
                    
                    # Get results/metrics
                    results = []
                    result_elems = case.find_all(['li', 'span'], class_=re.compile(r'result|metric|outcome', re.I))
                    for elem in result_elems:
                        results.append(self.clean_text(elem.get_text()))
                    
                    if title:
                        case_data = {
                            'title': title,
                            'client': client,
                            'summary': summary[:1000],
                            'image': img_url,
                            'results': results
                        }
                        
                        if case_data not in self.data['social_proof']['case_studies']:
                            self.data['social_proof']['case_studies'].append(case_data)
        
        # Client logos/list
        client_sections = soup.find_all(['section', 'div'], class_=re.compile(r'client|customer|partner|trusted-by', re.I))
        
        for section in client_sections:
            # Get logos
            logos = section.find_all('img')
            for logo in logos:
                client_name = self.clean_text(logo.get('alt', ''))
                if client_name and len(client_name) < 100:
                    if client_name not in self.data['social_proof']['client_list']:
                        self.data['social_proof']['client_list'].append(client_name)
    
    def extract_contact_information(self, soup: BeautifulSoup):
        """Extract comprehensive contact information"""
        text = soup.get_text()
        
        # Emails - categorized
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        for email in emails:
            email_lower = email.lower()
            if any(keyword in email_lower for keyword in ['contact', 'info', 'hello', 'mail']):
                if not self.data['contact_information']['primary_email']:
                    self.data['contact_information']['primary_email'] = email
            elif 'sales' in email_lower:
                self.data['contact_information']['sales_contacts'].append(email)
            elif 'support' in email_lower:
                self.data['contact_information']['support_contacts'].append(email)
            else:
                if email not in self.data['contact_information']['department_emails']:
                    self.data['contact_information']['department_emails'].append(email)
        
        # Phone numbers - all formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}',
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            for phone in phones:
                if phone not in self.data['contact_information']['phone_numbers']:
                    self.data['contact_information']['phone_numbers'].append(phone)
        
        # Addresses
        contact_sections = soup.find_all(['section', 'div', 'footer'], class_=re.compile(r'contact|address|location|office', re.I))
        
        for section in contact_sections:
            addr_elem = section.find(['p', 'address', 'div'], class_=re.compile(r'address|location', re.I))
            if addr_elem:
                addr_text = self.clean_text(addr_elem.get_text())
                if addr_text and 20 < len(addr_text) < 500:
                    if addr_text not in self.data['contact_information']['addresses']:
                        self.data['contact_information']['addresses'].append(addr_text)
    
    def extract_social_media(self, soup: BeautifulSoup):
        """Extract all social media and online presence"""
        social_patterns = {
            'LinkedIn': r'linkedin\.com/(company|in|showcase)/[\w\-]+',
            'Facebook': r'facebook\.com/[\w\-\.]+',
            'Twitter': r'(twitter|x)\.com/[\w\-]+',
            'Instagram': r'instagram\.com/[\w\-\.]+',
            'YouTube': r'youtube\.com/(channel|c|user|@)[\w\-]+',
            'GitHub': r'github\.com/[\w\-]+',
            'Medium': r'medium\.com/@?[\w\-]+',
            'Pinterest': r'pinterest\.com/[\w\-]+',
            'TikTok': r'tiktok\.com/@[\w\-]+',
            'WhatsApp': r'(wa\.me|api\.whatsapp\.com)',
        }
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href, re.I):
                    if platform not in self.data['online_presence']['social_media']:
                        self.data['online_presence']['social_media'][platform] = href
    
    def extract_calls_to_action(self, soup: BeautifulSoup):
        """Extract all CTAs"""
        cta_elements = soup.find_all(['a', 'button'], class_=re.compile(r'cta|call-to-action|btn|button|primary', re.I))
        
        for cta in cta_elements:
            text = self.clean_text(cta.get_text())
            if text and 3 < len(text) < 100:
                if not self.data['calls_to_action']['primary_cta']:
                    self.data['calls_to_action']['primary_cta'] = text
                elif text not in self.data['calls_to_action']['secondary_ctas']:
                    self.data['calls_to_action']['secondary_ctas'].append(text)
    
    def extract_additional_content(self, soup: BeautifulSoup):
        """Extract FAQs and other content"""
        # FAQs
        faq_sections = soup.find_all(['section', 'div'], class_=re.compile(r'faq|question|q-?a', re.I))
        
        for section in faq_sections:
            questions = section.find_all(['div', 'dt', 'h3', 'h4'], class_=re.compile(r'question|q', re.I))
            
            for q in questions:
                question_text = self.clean_text(q.get_text())
                
                # Get answer
                answer_elem = q.find_next_sibling(['div', 'dd', 'p'])
                answer_text = self.clean_text(answer_elem.get_text()) if answer_elem else ''
                
                if question_text:
                    faq_data = {
                        'question': question_text,
                        'answer': answer_text
                    }
                    if faq_data not in self.data['additional_content']['faqs']:
                        self.data['additional_content']['faqs'].append(faq_data)
    
    def get_comprehensive_links(self, soup: BeautifulSoup) -> Set[str]:
        """Get all relevant internal links"""
        links = set()
        
        # More comprehensive relevant keywords
        relevant_keywords = [
            'about', 'service', 'product', 'solution', 'team', 'contact',
            'testimonial', 'case', 'portfolio', 'award', 'leadership',
            'partner', 'client', 'customer', 'success', 'story',
            'who-we-are', 'what-we-do', 'why', 'how', 'work',
            'industr', 'sector', 'offering', 'feature', 'benefit'
        ]
        
        for link in soup.find_all('a', href=True):
            url = urljoin(self.base_url, link['href'])
            if urlparse(url).netloc == self.domain:
                clean_url = url.split('#')[0].split('?')[0]
                
                # Check if URL is relevant
                if any(keyword in clean_url.lower() for keyword in relevant_keywords):
                    if clean_url not in self.visited_urls:
                        links.add(clean_url)
        
        return links
    
    def scrape(self, max_pages: int = 50):
        """Main comprehensive scraping orchestrator"""
        print(f"\n{'='*80}")
        print(f"  COMPREHENSIVE PROFESSIONAL SALES BROCHURE SCRAPER")
        print(f"{'='*80}")
        print(f"🎯 Target: {self.base_url}")
        print(f"📄 Max Pages: {max_pages}")
        print(f"⏱️  Delay: {DELAY_BETWEEN_REQUESTS}s between requests")
        print(f"{'='*80}\n")
        
        to_visit = {self.base_url}
        pages_scraped = 0
        
        while to_visit and pages_scraped < max_pages:
            url = to_visit.pop()
            if url in self.visited_urls:
                continue
            
            print(f"📍 [{pages_scraped + 1:3d}/{max_pages}] Scraping: {url[:70]}...")
            soup = self.get_page(url)
            
            if not soup:
                continue
            
            self.visited_urls.add(url)
            pages_scraped += 1
            
            # Extract ALL data types
            print(f"    └─ Extracting data...")
            
            if pages_scraped == 1:
                self.extract_company_identity(soup)
            
            self.extract_visual_assets(soup)
            self.extract_about_content(soup)
            self.extract_offerings(soup)
            self.extract_usps_and_benefits(soup)
            self.extract_statistics_and_achievements(soup)
            self.extract_team_and_leadership(soup)
            self.extract_credibility_markers(soup)
            self.extract_social_proof(soup)
            self.extract_contact_information(soup)
            self.extract_social_media(soup)
            self.extract_calls_to_action(soup)
            self.extract_additional_content(soup)
            
            # Get more pages
            new_links = self.get_comprehensive_links(soup)
            to_visit.update(new_links)
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        self._clean_and_deduplicate()
        
        print(f"\n{'='*80}")
        print("✅ COMPREHENSIVE SCRAPING COMPLETE!")
        print(f"{'='*80}\n")
        self._print_comprehensive_summary()
        
        return self.data
    
    def _clean_and_deduplicate(self):
        """Clean and remove duplicates from all data"""
        # Helper function to dedupe list of dicts
        def dedupe_list_of_dicts(items, key):
            seen = set()
            unique = []
            for item in items:
                if isinstance(item, dict) and item.get(key):
                    if item[key] not in seen:
                        seen.add(item[key])
                        unique.append(item)
                elif isinstance(item, str):
                    if item not in seen:
                        seen.add(item)
                        unique.append(item)
            return unique
        
        # Deduplicate all sections
        self.data['company_identity']['taglines'] = list(set(self.data['company_identity']['taglines']))
        self.data['about_company']['company_overview'] = list(set(self.data['about_company']['company_overview']))
        self.data['about_company']['core_values'] = list(set(self.data['about_company']['core_values']))
        
        self.data['offerings']['services'] = dedupe_list_of_dicts(self.data['offerings']['services'], 'title')
        self.data['offerings']['products'] = dedupe_list_of_dicts(self.data['offerings']['products'], 'name')
        self.data['offerings']['industries_served'] = list(set(self.data['offerings']['industries_served']))
        
        self.data['metrics_and_stats']['key_statistics'] = dedupe_list_of_dicts(self.data['metrics_and_stats']['key_statistics'], 'value')
        self.data['social_proof']['client_testimonials'] = dedupe_list_of_dicts(self.data['social_proof']['client_testimonials'], 'quote')
        self.data['social_proof']['case_studies'] = dedupe_list_of_dicts(self.data['social_proof']['case_studies'], 'title')
        
        self.data['contact_information']['phone_numbers'] = list(set(self.data['contact_information']['phone_numbers']))
        self.data['contact_information']['department_emails'] = list(set(self.data['contact_information']['department_emails']))
    
    def _print_comprehensive_summary(self):
        """Print detailed extraction summary"""
        print("📊 COMPREHENSIVE DATA EXTRACTION SUMMARY:\n")
        
        print("🏢 COMPANY IDENTITY:")
        print(f"   Company Name: {self.data['company_identity']['company_name'] or 'Not found'}")
        print(f"   Taglines: {len(self.data['company_identity']['taglines'])}")
        print(f"   Logos: {1 if self.data['company_identity']['logo_url'] else 0} + {len(self.data['company_identity']['alternative_logos'])} alternatives")
        
        print("\n🖼️  VISUAL ASSETS:")
        print(f"   Hero Images: {len(self.data['visual_assets']['hero_images'])}")
        print(f"   Product Images: {len(self.data['visual_assets']['product_images'])}")
        print(f"   Team Photos: {len(self.data['visual_assets']['team_photos'])}")
        print(f"   All High-Quality Images: {len(self.data['visual_assets']['all_high_quality_images'])}")
        
        print("\n📖 ABOUT COMPANY:")
        print(f"   Overview Paragraphs: {len(self.data['about_company']['company_overview'])}")
        print(f"   Mission Statements: {len(self.data['about_company']['mission_statements'])}")
        print(f"   Vision Statements: {len(self.data['about_company']['vision_statements'])}")
        print(f"   Core Values: {len(self.data['about_company']['core_values'])}")
        print(f"   History Items: {len(self.data['about_company']['history'])}")
        
        print("\n💼 OFFERINGS:")
        print(f"   Services: {len(self.data['offerings']['services'])}")
        print(f"   Products: {len(self.data['offerings']['products'])}")
        print(f"   Solutions: {len(self.data['offerings']['solutions'])}")
        print(f"   Industries Served: {len(self.data['offerings']['industries_served'])}")
        
        print("\n⭐ COMPETITIVE ADVANTAGES:")
        print(f"   USPs: {len(self.data['competitive_advantages']['unique_selling_points'])}")
        print(f"   Benefits: {len(self.data['competitive_advantages']['benefits'])}")
        print(f"   Why Choose Us: {len(self.data['competitive_advantages']['why_choose_us'])}")
        
        print("\n📊 METRICS & STATS:")
        print(f"   Key Statistics: {len(self.data['metrics_and_stats']['key_statistics'])}")
        print(f"   Achievements: {len(self.data['metrics_and_stats']['achievements'])}")
        
        print("\n👥 TEAM & LEADERSHIP:")
        print(f"   Executives: {len(self.data['team_and_leadership']['executives'])}")
        print(f"   Leadership Team: {len(self.data['team_and_leadership']['leadership_team'])}")
        print(f"   Key Personnel: {len(self.data['team_and_leadership']['key_personnel'])}")
        
        print("\n🏆 CREDIBILITY:")
        print(f"   Awards: {len(self.data['credibility']['awards'])}")
        print(f"   Certifications: {len(self.data['credibility']['certifications'])}")
        print(f"   Partnerships: {len(self.data['credibility']['partnerships'])}")
        
        print("\n💬 SOCIAL PROOF:")
        print(f"   Client Testimonials: {len(self.data['social_proof']['client_testimonials'])}")
        print(f"   Case Studies: {len(self.data['social_proof']['case_studies'])}")
        print(f"   Client List: {len(self.data['social_proof']['client_list'])}")
        
        print("\n📞 CONTACT INFORMATION:")
        print(f"   Primary Email: {'✓' if self.data['contact_information']['primary_email'] else '✗'}")
        print(f"   Phone Numbers: {len(self.data['contact_information']['phone_numbers'])}")
        print(f"   Addresses: {len(self.data['contact_information']['addresses'])}")
        
        print("\n🌐 ONLINE PRESENCE:")
        print(f"   Social Media Links: {len(self.data['online_presence']['social_media'])}")
        
        print("\n💡 ADDITIONAL:")
        print(f"   FAQs: {len(self.data['additional_content']['faqs'])}")
        print(f"   CTAs: {1 if self.data['calls_to_action']['primary_cta'] else 0} + {len(self.data['calls_to_action']['secondary_ctas'])} secondary")
        
        print(f"\n{'='*80}")
        print(f"📄 Total Pages Scraped: {len(self.visited_urls)}")
        print(f"{'='*80}\n")
    
    def save(self, filename: str):
        """Save comprehensive data to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"💾 Comprehensive data saved to: {filename}")
        print(f"📏 File size: {len(json.dumps(self.data)) / 1024:.2f} KB\n")
        return filename


# ============================================
# MAIN EXECUTION
# ============================================
# if __name__ == "__main__":
#     scraper = ComprehensiveBrochureScraper(TARGET_URL)
#     data = scraper.scrape(max_pages=MAX_PAGES)
#     scraper.save(OUTPUT_FILE)
    
#     print("✨ READY FOR PROFESSIONAL SALES BROCHURE CREATION!")
#     print(f"📁 All comprehensive data saved in '{OUTPUT_FILE}'\n")
#     print("💡 TIP: This data includes everything you need for a detailed, professional sales brochure:")
#     print("   - Complete company story and background")
#     print("   - All products, services, and solutions")
#     print("   - Team information with photos")
#     print("   - Client testimonials and case studies")
#     print("   - Statistics and achievements")
#     print("   - Awards and certifications")
#     print("   - Contact information and social media")
#     print("   - High-quality images for visual appeal\n")

import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scraper.py <url> <output_file>")
        sys.exit(1)

    target_url = sys.argv[1]
    output_file = sys.argv[2]

    scraper = ComprehensiveBrochureScraper(target_url)
    data = scraper.scrape(max_pages=20)

    print(f"Data saved to {output_file}")



