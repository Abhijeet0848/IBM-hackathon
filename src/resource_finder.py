"""
Smart Resource & Reference Suggester
Generates curated YouTube lecture links, textbook recommendations, interactive simulations,
and academic paper references for any syllabus topic.
"""

import urllib.parse
from typing import Dict, Any, List

class ResourceFinder:
    @staticmethod
    def get_curated_resources(topic_text: str) -> Dict[str, Any]:
        """
        Generates direct, high-yield web reference links and curated recommendations for a topic.
        """
        # Clean topic text for query
        cleaned_topic = topic_text.replace("Study concept:", "").replace("Work through practical examples & formula sheet for", "").strip()
        cleaned_topic = cleaned_topic.strip("-*• :")
        encoded_query = urllib.parse.quote_plus(cleaned_topic)

        # YouTube video lectures
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}+lecture+tutorial"
        
        # Google Books / Textbooks
        google_books_url = f"https://www.google.com/search?tbm=bks&q={encoded_query}+textbook"

        # Academic papers / Google Scholar
        scholar_url = f"https://scholar.google.com/scholar?q={encoded_query}"

        # MIT OpenCourseWare / Khan Academy search
        mit_ocw_url = f"https://www.google.com/search?q=site%3Aocw.mit.edu+{encoded_query}"

        # Wikipedia / Academic encyclopedia
        wikipedia_url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}"

        return {
            "topic": cleaned_topic,
            "youtube_url": youtube_url,
            "google_books_url": google_books_url,
            "scholar_url": scholar_url,
            "mit_ocw_url": mit_ocw_url,
            "wikipedia_url": wikipedia_url
        }
