#!/usr/bin/env python3
"""Generate 50,000 common dictionary words for Discord username checking (LETTERS ONLY)"""

import os

# Common English words (letters only - no numbers or special characters)
common_words = [
    # Most common words
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    
    # Common nouns
    "time", "person", "year", "way", "day", "thing", "man", "world", "life", "hand",
    "part", "place", "case", "week", "company", "system", "program", "question", "number", "group",
    "problem", "fact", "area", "family", "money", "story", "side", "reason", "body", "head",
    "house", "service", "friend", "parent", "water", "room", "mother", "father", "child", "name",
    "school", "state", "game", "glass", "car", "job", "edge", "word", "work", "book",
    "page", "sound", "line", "note", "food", "wood", "door", "town", "unit", "power",
    
    # Common adjectives
    "good", "new", "first", "last", "long", "great", "little", "own", "right", "true",
    "high", "different", "small", "large", "next", "early", "young", "important", "few", "public",
    "bad", "same", "able", "big", "old", "other", "such", "sure", "full", "free",
    "hot", "cold", "dark", "light", "fast", "slow", "hard", "soft", "wet", "dry",
    "open", "closed", "heavy", "clean", "dirty", "loud", "quiet", "strange", "normal", "special",
    
    # Common verbs
    "see", "get", "make", "go", "know", "take", "come", "think", "use", "find",
    "give", "tell", "work", "call", "try", "ask", "need", "feel", "become", "leave",
    "put", "mean", "keep", "let", "begin", "seem", "help", "talk", "play", "run",
    "move", "like", "live", "believe", "hold", "bring", "happen", "write", "provide", "sit",
    "stand", "lose", "pay", "meet", "include", "continue", "set", "learn", "change", "lead",
    "follow", "break", "build", "read", "watch", "listen", "speak", "hear", "sleep", "wake",
    
    # Animals
    "dog", "cat", "bird", "fish", "horse", "cow", "pig", "sheep", "lion", "tiger",
    "bear", "wolf", "fox", "deer", "rabbit", "mouse", "rat", "snake", "turtle", "frog",
    "eagle", "owl", "duck", "chicken", "swan", "penguin", "whale", "shark", "dolphin", "elephant",
    "zebra", "giraffe", "monkey", "ape", "parrot", "bee", "ant", "butterfly", "spider", "lizard",
    
    # Colors
    "red", "blue", "green", "yellow", "black", "white", "gray", "grey", "brown", "orange",
    "purple", "pink", "violet", "silver", "gold", "bronze", "cyan", "magenta", "turquoise", "indigo",
    
    # Numbers (as text only)
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "twenty", "thirty", "forty", "fifty", "hundred", "thousand", "million",
    
    # Emotions
    "happy", "sad", "angry", "calm", "excited", "worried", "scared", "brave", "proud", "ashamed",
    "love", "hate", "hope", "fear", "trust", "doubt", "joy", "pain", "peace", "anger",
    
    # Body parts
    "eye", "ear", "nose", "mouth", "tooth", "tongue", "lip", "chin", "cheek", "neck",
    "shoulder", "arm", "elbow", "wrist", "hand", "finger", "thumb", "leg", "knee", "foot",
    "toe", "heel", "back", "chest", "stomach", "heart", "lung", "brain", "liver", "skin",
    
    # Nature
    "tree", "flower", "grass", "bush", "leaf", "seed", "root", "stem", "branch", "trunk",
    "rock", "stone", "sand", "dirt", "soil", "clay", "mountain", "valley", "hill", "cave",
    "river", "lake", "ocean", "sea", "beach", "island", "desert", "forest", "jungle", "sky",
    "sun", "moon", "star", "cloud", "wind", "rain", "snow", "ice", "fire", "lightning",
    
    # Objects
    "table", "chair", "bed", "desk", "lamp", "mirror", "window", "wall", "floor", "ceiling",
    "door", "lock", "key", "knife", "fork", "spoon", "plate", "cup", "glass", "bottle",
    "box", "bag", "basket", "bucket", "rope", "chain", "ring", "crown", "throne", "shield",
    
    # Food
    "bread", "butter", "cheese", "milk", "egg", "meat", "fish", "chicken", "beef", "pork",
    "rice", "pasta", "bean", "corn", "wheat", "apple", "banana", "orange", "grape", "berry",
    "peach", "cherry", "strawberry", "blueberry", "watermelon", "lemon", "lime", "coconut", "nut", "seed",
    
    # Drinks
    "water", "juice", "tea", "coffee", "beer", "wine", "soda", "cola", "cider",
    
    # Clothing
    "shirt", "pants", "dress", "coat", "hat", "shoe", "boot", "sock", "glove", "scarf",
    "tie", "belt", "button", "zipper", "pocket", "sleeve", "collar", "cuff", "hem", "seam",
    
    # Weather
    "sun", "rain", "snow", "wind", "cloud", "storm", "thunder", "hail", "frost", "fog",
    "breeze", "gale", "blizzard", "tornado", "hurricane", "monsoon", "heat", "cold", "warm", "cool",
    
    # Seasons and Time
    "spring", "summer", "autumn", "fall", "winter", "monday", "tuesday", "wednesday", "thursday", "friday",
    "saturday", "sunday", "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "morning", "afternoon", "evening", "night", "midnight", "noon",
    
    # Science & Tech (letters only)
    "atom", "molecule", "element", "compound", "energy", "force", "motion", "speed", "velocity",
    "gravity", "magnet", "electric", "circuit", "computer", "software", "hardware", "network", "internet", "server",
    "database", "algorithm", "code", "script", "program", "application", "system", "process", "data", "file",
    
    # Gaming terms (letters only)
    "player", "gamer", "gaming", "pixel", "sprite", "level", "quest", "monster", "dragon", "sword",
    "magic", "spell", "potion", "treasure", "gold", "silver", "bronze", "diamond", "ruby", "emerald",
    "sapphire", "crystal", "scroll", "book", "tome", "rune", "artifact", "weapon", "armor", "shield",
    "mana", "health", "stamina", "speed", "attack", "defense", "ability", "skill", "talent", "power",
    
    # Username patterns (letters only)
    "pro", "king", "queen", "lord", "lady", "master", "ninja", "samurai", "warrior", "knight",
    "ranger", "wizard", "priest", "rogue", "paladin", "druid", "mage", "cleric", "monk", "hunter",
    "assassin", "sniper", "scout", "spy", "admin", "operator", "ultra", "super", "mega", "epic",
    "legend", "myth", "god", "angel", "demon", "spirit", "ghost", "phantom", "shadow", "dark",
    "fire", "ice", "storm", "thunder", "frost", "chaos", "order", "balance", "harmony", "elite",
    "prime", "apex", "peak", "top", "best", "light", "wind", "earth", "water", "nova",
]

common_verbs = [
    "see", "get", "make", "go", "know", "take", "come", "think", "use", "find",
    "give", "tell", "work", "call", "try", "ask", "need", "feel", "become", "leave",
    "put", "mean", "keep", "let", "begin", "seem", "help", "talk", "play", "run",
    "move", "like", "live", "believe", "hold", "bring", "happen", "write", "provide", "sit",
    "stand", "lose", "pay", "meet", "include", "continue", "set", "learn", "change", "lead",
    "follow", "break", "build", "read", "watch", "listen", "speak", "hear", "sleep", "wake",
]

def main():
    print("[*] Generating 50,000 dictionary words (LETTERS ONLY - NO NUMBERS OR SPECIAL CHARS)...")
    
    words = set(common_words)
    
    # Add common prefixes and suffixes (extended list)
    prefixes = ["un", "re", "pre", "dis", "mis", "over", "under", "out", "in", "de", "anti", "co", "sub", "inter", "trans", "super", "semi", "non", "multi", "post", "neo"]
    suffixes = ["ing", "ed", "er", "ly", "able", "ness", "ment", "ful", "less", "ish", "ous", "ive", "ity", "ism", "ate", "ize"]
    
    # Generate word variations by combining with prefixes/suffixes
    base_words = list(common_words)
    
    for base in base_words:
        if len(base) > 2:
            # Add suffix variations
            for suffix in suffixes:
                new_word = base + suffix
                if len(new_word) <= 30 and new_word.isalpha():
                    words.add(new_word)
            
            # Add prefix variations
            for prefix in prefixes:
                new_word = prefix + base
                if len(new_word) <= 30 and new_word.isalpha():
                    words.add(new_word)
    
    # Create many word combinations from combining common elements
    combining_words = ["dark", "light", "fire", "ice", "wind", "earth", "chaos", "order", "prime", "ultra",
                      "blue", "red", "green", "gold", "silver", "shadow", "storm", "night", "day", "dawn",
                      "black", "white", "bright", "cold", "hot", "fast", "slow", "deep", "high", "low",
                      "sacred", "ancient", "mystic", "divine", "eternal", "infinite", "cosmic", "stellar", "lunar", "solar"]
    
    endings = ["lord", "king", "master", "wizard", "knight", "hunter", "warrior", "player", "pro", "elite",
              "mage", "sage", "forge", "stone", "heart", "soul", "mind", "spirit", "blade", "fang",
              "strike", "force", "power", "vision", "seeker", "rider", "walker", "talker", "maker", "breaker",
              "keeper", "guardian", "protector", "defender", "champion", "victor", "conqueror", "emperor", "sage", "oracle"]
    
    for combo in combining_words:
        for ending in endings:
            new_word = combo + ending
            if len(new_word) <= 30 and new_word.isalpha():
                words.add(new_word)
            # Also try reverse
            new_word2 = ending + combo
            if len(new_word2) <= 30 and new_word2.isalpha():
                words.add(new_word2)
    
    # Add more word combinations
    adjectives = ["ancient", "brave", "clever", "daring", "epic", "fierce", "glorious", "heroic", "mighty", "noble", 
                 "powerful", "rare", "sacred", "swift", "ultimate", "wild", "wise", "worthy", "zealous", "awesome"]
    nouns = ["beast", "champion", "dragon", "empire", "fate", "glory", "hero", "kingdom", "legend", "magic", 
            "oracle", "quest", "realm", "sanctuary", "treasure", "warrior", "wizard", "weapon", "wonder", "wanderer"]
    
    for adj in adjectives:
        for noun in nouns:
            new_word = adj + noun
            if len(new_word) <= 30 and new_word.isalpha():
                words.add(new_word)
            # Reverse
            new_word2 = noun + adj
            if len(new_word2) <= 30 and new_word2.isalpha():
                words.add(new_word2)
    
    # Generate double-word combinations
    small_words = ["star", "moon", "sun", "sky", "sea", "tree", "flower", "stone", "fire", "water",
                   "wind", "earth", "wave", "peak", "river", "lake", "cloud", "stream", "blade", "crown",
                   "temple", "tower", "shrine", "tomb", "vault", "palace", "castle", "fortress", "haven", "gate"]
    
    for i, word1 in enumerate(small_words):
        for word2 in small_words:
            if word1 != word2:
                combined = word1 + word2
                if len(combined) <= 30 and combined.isalpha():
                    words.add(combined)
    
    # Add triple combinations
    for i, w1 in enumerate(small_words[:10]):  # Limit to avoid explosion
        for j, w2 in enumerate(small_words[:10]):
            for w3 in small_words[:5]:
                combined = w1 + w2 + w3
                if len(combined) <= 30 and combined.isalpha():
                    words.add(combined)
    
    # Convert to sorted list
    words_list = sorted(list(words))
    
    # Filter to STRICTLY alphabetic only (no numbers, no special chars)
    filtered_words = [w for w in words_list if w.isalpha() and len(w) > 0]
    
    # Cap at 50000
    filtered_words = filtered_words[:50000]
    
    # Double-check: verify all words are letters-only
    assert all(w.isalpha() for w in filtered_words), "ERROR: Found non-alphabetic characters!"
    
    # Write to file
    output_file = "usernames.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for word in filtered_words:
            f.write(word + "\n")

    original_file = "usernames_original.txt"
    original_count = write_original_forms(common_words, common_verbs, original_file)

    verb_forms_file = "verb_forms.txt"
    verb_forms_count = write_verb_forms(common_verbs, verb_forms_file)
    
    print(f"[+] Generated {len(filtered_words)} words (100% letters only)")
    print(f"[+] Saved expanded list to {output_file} ({os.path.getsize(output_file) / 1024:.1f} KB)")
    print(f"[+] Saved original forms to {original_file} ({os.path.getsize(original_file) / 1024:.1f} KB)")
    print(f"[+] Saved verb first/second forms to {verb_forms_file} ({os.path.getsize(verb_forms_file) / 1024:.1f} KB)")
    print(f"[+] VERIFIED: All {len(filtered_words)} expanded entries contain ONLY alphabetic characters")
    print(f"[+] VERIFIED: Original file contains {original_count} alphabetic entries")
    print(f"[+] VERIFIED: Verb forms file contains {verb_forms_count} entries")


def get_verb_second_form(verb: str) -> str:
    irregular_past = {
        "be": "was",
        "have": "had",
        "do": "did",
        "say": "said",
        "go": "went",
        "take": "took",
        "come": "came",
        "see": "saw",
        "know": "knew",
        "get": "got",
        "make": "made",
        "feel": "felt",
        "leave": "left",
        "write": "wrote",
        "find": "found",
        "give": "gave",
        "tell": "told",
        "bring": "brought",
        "begin": "began",
        "run": "ran",
        "read": "read",
        "sleep": "slept",
        "wake": "woke",
        "sit": "sat",
        "stand": "stood",
        "lose": "lost",
        "pay": "paid",
        "meet": "met",
        "keep": "kept",
        "write": "wrote",
        "build": "built",
        "break": "broke",
        "lead": "led",
        "bring": "brought",
        "teach": "taught",
    }
    if verb in irregular_past:
        return irregular_past[verb]
    if verb.endswith("e"):
        return verb + "d"
    if len(verb) > 2 and verb.endswith("y") and verb[-2] not in "aeiou":
        return verb[:-1] + "ied"
    if len(verb) > 2 and verb[-1] not in "aeiou" and verb[-2] in "aeiou" and verb[-3] not in "aeiou" and verb[-1] not in "wxy":
        return verb + verb[-1] + "ed"
    return verb + "ed"


def write_original_forms(common_words, verb_list, output_file):
    original_words = set(common_words)
    for verb in verb_list:
        second = get_verb_second_form(verb)
        original_words.add(second)

    filtered = [w for w in sorted(original_words) if w.isalpha() and len(w) > 0]
    with open(output_file, "w", encoding="utf-8") as f:
        for word in filtered:
            f.write(word + "\n")
    return len(filtered)


def write_verb_forms(verb_list, output_file):
    lines = []
    for verb in sorted(set(verb_list)):
        second = get_verb_second_form(verb)
        if second == verb:
            lines.append(verb)
        else:
            lines.append(f"{verb},{second}")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return len(lines)


if __name__ == "__main__":
    main()
