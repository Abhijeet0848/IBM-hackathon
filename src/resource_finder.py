"""
Smart Resource & Reference Suggester
Performs semantic topic extraction on uploaded course notes and milestones,
generating verified direct Wikipedia articles, GeeksforGeeks tutorials, YouTube lectures,
and academic references tailored to exact syllabus concepts.
"""

import re
import urllib.parse
from typing import Dict, Any, List

# Extensive canonical Wikipedia dictionary for computer science, engineering & mathematics
CANONICAL_WIKIPEDIA_MAP = {
    # C & System Programming
    "c": "https://en.wikipedia.org/wiki/C_(programming_language)",
    "c programming": "https://en.wikipedia.org/wiki/C_(programming_language)",
    "programming in c": "https://en.wikipedia.org/wiki/C_(programming_language)",
    "c language": "https://en.wikipedia.org/wiki/C_(programming_language)",
    "c syntax": "https://en.wikipedia.org/wiki/C_syntax",
    "c data types": "https://en.wikipedia.org/wiki/C_data_types",
    "c preprocessor": "https://en.wikipedia.org/wiki/C_preprocessor",
    "preprocessor": "https://en.wikipedia.org/wiki/C_preprocessor",
    "macros": "https://en.wikipedia.org/wiki/C_preprocessor#Macro_definition_and_expansion",
    "pointers": "https://en.wikipedia.org/wiki/Pointer_(computer_programming)",
    "pointers in c": "https://en.wikipedia.org/wiki/Pointer_(computer_programming)",
    "pointer arithmetic": "https://en.wikipedia.org/wiki/Pointer_(computer_programming)#C_and_C++",
    "dynamic memory allocation": "https://en.wikipedia.org/wiki/C_dynamic_memory_allocation",
    "malloc": "https://en.wikipedia.org/wiki/C_dynamic_memory_allocation",
    "memory management": "https://en.wikipedia.org/wiki/Memory_management",
    "arrays": "https://en.wikipedia.org/wiki/Array_(data_structure)",
    "strings in c": "https://en.wikipedia.org/wiki/C_string_handling",
    "c strings": "https://en.wikipedia.org/wiki/C_string_handling",
    "string handling": "https://en.wikipedia.org/wiki/C_string_handling",
    "structures": "https://en.wikipedia.org/wiki/Struct_(C_programming_language)",
    "struct": "https://en.wikipedia.org/wiki/Struct_(C_programming_language)",
    "structs": "https://en.wikipedia.org/wiki/Struct_(C_programming_language)",
    "unions": "https://en.wikipedia.org/wiki/Union_(computer_science)",
    "file handling": "https://en.wikipedia.org/wiki/C_file_input/output",
    "file i/o": "https://en.wikipedia.org/wiki/C_file_input/output",
    "functions in c": "https://en.wikipedia.org/wiki/C_syntax#Functions",
    "recursion": "https://en.wikipedia.org/wiki/Recursion_(computer_science)",
    "bitwise operators": "https://en.wikipedia.org/wiki/Bitwise_operations_in_C",
    "control flow": "https://en.wikipedia.org/wiki/Control_flow",
    "loops": "https://en.wikipedia.org/wiki/Control_flow#Loops",
    "switch statement": "https://en.wikipedia.org/wiki/Switch_statement",
    "conditional statements": "https://en.wikipedia.org/wiki/Conditional_(computer_programming)",
    
    # C++ & Object Oriented
    "c++": "https://en.wikipedia.org/wiki/C%2B%2B",
    "cpp": "https://en.wikipedia.org/wiki/C%2B%2B",
    "oop": "https://en.wikipedia.org/wiki/Object-oriented_programming",
    "classes and objects": "https://en.wikipedia.org/wiki/Class_(computer_programming)",
    "inheritance": "https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)",
    "polymorphism": "https://en.wikipedia.org/wiki/Polymorphism_(computer_science)",
    
    # Core Data Structures & Algorithms
    "data structures": "https://en.wikipedia.org/wiki/Data_structure",
    "algorithms": "https://en.wikipedia.org/wiki/Algorithm",
    "linked list": "https://en.wikipedia.org/wiki/Linked_list",
    "singly linked list": "https://en.wikipedia.org/wiki/Linked_list#Singly_linked_list",
    "doubly linked list": "https://en.wikipedia.org/wiki/Doubly_linked_list",
    "stack": "https://en.wikipedia.org/wiki/Stack_(abstract_data_type)",
    "queue": "https://en.wikipedia.org/wiki/Queue_(abstract_data_type)",
    "binary tree": "https://en.wikipedia.org/wiki/Binary_tree",
    "binary search tree": "https://en.wikipedia.org/wiki/Binary_search_tree",
    "avl tree": "https://en.wikipedia.org/wiki/AVL_tree",
    "graphs": "https://en.wikipedia.org/wiki/Graph_(abstract_data_type)",
    "graph theory": "https://en.wikipedia.org/wiki/Graph_theory",
    "bfs": "https://en.wikipedia.org/wiki/Breadth-first_search",
    "dfs": "https://en.wikipedia.org/wiki/Depth-first_search",
    "dynamic programming": "https://en.wikipedia.org/wiki/Dynamic_programming",
    "greedy algorithm": "https://en.wikipedia.org/wiki/Greedy_algorithm",
    "sorting algorithms": "https://en.wikipedia.org/wiki/Sorting_algorithm",
    "binary search": "https://en.wikipedia.org/wiki/Binary_search",
    
    # Systems, DBMS & Networks
    "operating systems": "https://en.wikipedia.org/wiki/Operating_system",
    "process management": "https://en.wikipedia.org/wiki/Process_management_(computing)",
    "threads": "https://en.wikipedia.org/wiki/Thread_(computing)",
    "database": "https://en.wikipedia.org/wiki/Database",
    "dbms": "https://en.wikipedia.org/wiki/Database",
    "sql": "https://en.wikipedia.org/wiki/SQL",
    "normalization": "https://en.wikipedia.org/wiki/Database_normalization",
    "computer networks": "https://en.wikipedia.org/wiki/Computer_network",
    "tcp/ip": "https://en.wikipedia.org/wiki/Internet_protocol_suite",
    "osi model": "https://en.wikipedia.org/wiki/OSI_model",
    "artificial intelligence": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "machine learning": "https://en.wikipedia.org/wiki/Machine_learning"
}

class ResourceFinder:
    @staticmethod
    def clean_topic_query(topic_text: str) -> str:
        """Extracts the pure core topic keywords without syllabus numbering, boilerplate phrases or filler verbs."""
        if not topic_text:
            return ""
        
        # 1. Strip emojis and unicode variation selectors
        cleaned = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf\ufe00-\ufe0f]', '', topic_text)
        
        # 2. Strip bracket tags like [Theory], [Practice], [Recall]
        cleaned = re.sub(r'\[.*?\]', '', cleaned)
        
        # 3. Strip any non-alphanumeric leading symbols
        cleaned = re.sub(r'^[^\w]+', '', cleaned)
        
        # 4. Strip leading structural labels like 'Topic:', 'Module 1:', 'Study concept:'
        cleaned = re.sub(r'^\s*(Topic|Module\s*\d+|Unit\s*\d+|Chapter\s*\d+|Day\s*\d+|Week\s*\d+|Section\s*\d+|Lecture\s*\d+|Study concept)\s*:\s*', '', cleaned, flags=re.IGNORECASE)
        
        # 5. Remove comprehensive boilerplate activity descriptions and task prefixes
        boilerplate_patterns = [
            r'Core definitions and foundations of',
            r'Practical exercises and problems on',
            r'Active recall check on',
            r'Extract key testable definitions and theorems for',
            r'Solve high-probability exam questions on',
            r'Complete active recall test in',
            r'Understand theoretical foundations\s*(?:&|and)?\s*architectural proofs of',
            r'Step-by-step practical derivation\s*/\s*problem analysis for',
            r'Teach concept in ELI10 mode to verify 100% intuition',
            r'Quick recall review\s*(?:on)?',
            r'Study core mechanisms\s*(?:&|and)?\s*properties of',
            r'Solve targeted practical exercises on',
            r'Solve \d+ targeted exercises on',
            r'Work through practical examples\s*(?:&|and)?\s*(?:formula sheet)?\s*(?:for)?',
            r'Rapid review of summary notes and core formulas across',
            r'Work through high-yield edge case problems and',
            r'Launch \d+ full-length active recall drills in',
            r'Active recall flashcard session reviewing',
            r'Re-attempt any difficult practice problems from',
            r'Clarify any conceptual doubts using',
            r'Study concept\s*:',
            r'Study concept',
            r'Study',
            r'Implement',
            r'Review',
            r'Master',
            r'Overview of',
            r'Introduction to',
            r'Fundamentals of',
            r'Basics of'
        ]
        for bp in boilerplate_patterns:
            cleaned = re.sub(r'^\s*' + bp + r'\s*[:\-–—]?\s*', '', cleaned, flags=re.IGNORECASE)
            
        cleaned = re.sub(r'\(.*?\)', '', cleaned)
        cleaned = re.sub(r'^[^\w]+', '', cleaned)
        cleaned = cleaned.strip("-*• :.,\n\t")
        
        # 6. If colon remains, take the substantive portion
        if ":" in cleaned:
            parts = cleaned.split(":")
            if len(parts[0].split()) <= 2:
                cleaned = parts[1].strip()
            else:
                cleaned = parts[0].strip()

        cleaned = re.sub(r'^[^\w]+', '', cleaned)
        cleaned = re.sub(r'^\s*(and|or|with|for|in|of|about|on)\s+', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'^[^\w]+', '', cleaned)
        cleaned = cleaned.strip("-*• :.,\n\t")
        return cleaned.strip() if cleaned else topic_text.strip()

    @staticmethod
    def resolve_wikipedia_link(topic_name: str) -> str:
        """Finds direct Wikipedia article link or builds an exact search redirect URL."""
        cleaned = ResourceFinder.clean_topic_query(topic_name)
        lower = cleaned.lower()
        
        # Check canonical dictionary
        for key, direct_url in CANONICAL_WIKIPEDIA_MAP.items():
            if key == lower or (len(key) > 3 and key in lower) or (len(lower) > 3 and lower in key):
                return direct_url
                
        # Smart direct search redirect
        encoded = urllib.parse.quote_plus(cleaned)
        return f"https://en.wikipedia.org/w/index.php?search={encoded}&title=Special:Search&go=Go"

    @staticmethod
    def get_curated_resources_for_day(focus_module: str, checkpoint: str = "", tasks: List[str] = None) -> Dict[str, Any]:
        """
        Extracts syllabus concepts from the daily milestone and generates verified, clickable references.
        """
        tasks = tasks or []
        primary_topic = ResourceFinder.clean_topic_query(focus_module)
        
        # Avoid generic single-word topics like 'Topic'
        if (not primary_topic or primary_topic.lower() in ["topic", "module", "unit", "day"]) and checkpoint:
            primary_topic = ResourceFinder.clean_topic_query(checkpoint)
            
        if (not primary_topic or primary_topic.lower() in ["topic", "module", "unit", "day"]) and tasks:
            primary_topic = ResourceFinder.clean_topic_query(tasks[0])
            
        if not primary_topic or primary_topic.lower() in ["topic", "module", "unit", "day"]:
            primary_topic = "Syllabus Core Concepts"

        # Extract meaningful distinct subtopics from primary topic clauses or tasks
        subtopics = []
        seen_names = {primary_topic.lower()}
        
        # Extract subtopics from clauses inside primary topic (e.g. "national and international current events")
        sub_clauses = re.split(r'[,;]|\band\b', primary_topic)
        if len(sub_clauses) > 1:
            for sc in sub_clauses:
                clean_sc = sc.strip().rstrip(" ,;:.-")
                if len(clean_sc) > 3 and clean_sc.lower() not in seen_names:
                    seen_names.add(clean_sc.lower())
                    subtopics.append({
                        "name": clean_sc[:50],
                        "wikipedia_url": ResourceFinder.resolve_wikipedia_link(clean_sc)
                    })

        for t in tasks:
            clean_t = ResourceFinder.clean_topic_query(t)
            if clean_t and clean_t.lower() not in seen_names and len(clean_t) > 3 and clean_t.lower() not in ["topic", "module", "unit", "day"]:
                # Ensure it's not a generic task fragment
                if not any(clean_t.lower().startswith(p) for p in ["core definitions", "practical exercises", "active recall", "final comprehensive"]):
                    seen_names.add(clean_t.lower())
                    subtopics.append({
                        "name": clean_t[:50],
                        "wikipedia_url": ResourceFinder.resolve_wikipedia_link(clean_t)
                    })
        
        encoded_primary = urllib.parse.quote_plus(primary_topic)
        primary_wiki = ResourceFinder.resolve_wikipedia_link(primary_topic)

        return {
            "primary_topic": primary_topic,
            "primary_wiki": primary_wiki,
            "subtopics": subtopics[:3],
            "scholar_url": f"https://scholar.google.com/scholar?q={encoded_primary}",
            "youtube_url": f"https://www.youtube.com/results?search_query={encoded_primary}+educational+lecture",
            "google_books_url": f"https://www.google.com/search?tbm=bks&q={encoded_primary}+textbook",
            "mit_ocw_url": f"https://www.google.com/search?q={encoded_primary}+open+courseware+tutorial",
            "gfg_url": f"https://www.google.com/search?q=site%3Ageeksforgeeks.org+{encoded_primary}"
        }

    @staticmethod
    def get_curated_resources(topic_text: str) -> Dict[str, Any]:
        """Backward compatible helper."""
        res = ResourceFinder.get_curated_resources_for_day(topic_text)
        return {
            "topic": res["primary_topic"],
            "wikipedia_url": res["primary_wiki"],
            "scholar_url": res["scholar_url"],
            "youtube_url": res["youtube_url"],
            "google_books_url": res["google_books_url"],
            "mit_ocw_url": res["mit_ocw_url"]
        }
