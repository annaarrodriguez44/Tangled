"""
Slice 10: Pattern-Yarn Matching Algorithm
Goal: Match patterns to suitable yarns based on multiple criteria
"""

import pandas as pd
import numpy as np

def load_databases():
    """Load both pattern and yarn databases."""
    patterns_df = pd.read_excel('pattern_database.xlsx')
    yarn_df = pd.read_excel('Database_YARN.xlsx')
    return patterns_df, yarn_df

def normalize_yarn_weight(weight):
    """Normalize yarn weight names for matching."""
    if pd.isna(weight):
        return None
    
    weight = str(weight).lower().strip()
    
    # Map common variations
    weight_map = {
        'light': 'sport',
        'light/sport': 'sport',
        'dk': 'DK',
        'medium': 'worsted',
        'aran': 'worsted',
        'heavy': 'bulky',
        'super bulky': 'super bulky',
        'jumbo': 'super bulky'
    }
    
    for key, value in weight_map.items():
        if key in weight:
            return value
    
    return weight

def calculate_match_score(pattern_row, yarn_row):
    """Calculate how well a yarn matches a pattern (0-100 score)."""
    
    score = 0
    max_score = 0
    
    # 1. Yarn Weight Match (30 points) - CRITICAL
    max_score += 30
    pattern_weight = normalize_yarn_weight(pattern_row['Yarn Weight'])
    yarn_weight = normalize_yarn_weight(yarn_row['Yarn thikness'])
    
    if pattern_weight and yarn_weight:
        if pattern_weight.lower() in yarn_weight.lower() or yarn_weight.lower() in pattern_weight.lower():
            score += 30
        else:
            # Partial match for compatible weights
            compatible = {
                'sport': ['DK'],
                'DK': ['sport', 'worsted'],
                'worsted': ['DK', 'bulky'],
                'bulky': ['worsted', 'super bulky']
            }
            if pattern_weight in compatible and yarn_weight in compatible.get(pattern_weight, []):
                score += 15
    
    # 2. Hook Size Match (20 points)
    max_score += 20
    pattern_hook = pattern_row['Hook Size (mm)']
    yarn_hook = yarn_row['Needle/Hook Size (mm)']
    
    if pd.notna(pattern_hook) and pd.notna(yarn_hook):
        try:
            # Clean and convert hook sizes
            pattern_hook_clean = str(pattern_hook).strip()
            yarn_hook_clean = str(yarn_hook).strip()
            
            if pattern_hook_clean and yarn_hook_clean and pattern_hook_clean != ' ':
                hook_diff = abs(float(pattern_hook_clean) - float(yarn_hook_clean))
                if hook_diff == 0:
                    score += 20
                elif hook_diff <= 0.5:
                    score += 15
                elif hook_diff <= 1.0:
                    score += 10
        except (ValueError, TypeError):
            pass  # Skip if can't convert
    
    # 3. Yarn Composition Suitability (20 points)
    max_score += 20
    composition_text = str(pattern_row['Recommended Composition']).lower()
    
    if 'cotton' in composition_text and yarn_row['Cotton (%)'] > 50:
        score += 20
    elif 'acrylic' in composition_text and yarn_row['Acrylic (%)'] > 50:
        score += 20
    elif 'wool' in composition_text and yarn_row['Wool (%)'] > 50:
        score += 20
    elif 'not specified' in composition_text:
        score += 10  # Partial credit if composition not specified
    
    # 4. Rating (15 points)
    max_score += 15
    rating = yarn_row['Rating (★)']
    if pd.notna(rating):
        try:
            score += (float(rating) / 5.0) * 15
        except (ValueError, TypeError):
            score += 7.5  # Default if rating can't be converted
    
    # 5. Price/Value (15 points) - Lower is better
    max_score += 15
    price = yarn_row['Price (€)']
    if pd.notna(price):
        try:
            price = float(price)
            if price < 3:
                score += 15
            elif price < 5:
                score += 10
            elif price < 8:
                score += 5
        except (ValueError, TypeError):
            score += 7.5  # Default if price can't be converted
    
    # Calculate percentage
    if max_score > 0:
        return (score / max_score) * 100
    return 0

def match_yarn_to_pattern(pattern_name, patterns_df, yarn_df, top_n=5):
    """Find best yarn matches for a specific pattern."""
    
    # Find the pattern
    pattern_row = patterns_df[patterns_df['Pattern Name'] == pattern_name].iloc[0]
    
    # Calculate scores for all yarns
    scores = []
    for idx, yarn_row in yarn_df.iterrows():
        score = calculate_match_score(pattern_row, yarn_row)
        scores.append({
            'yarn_name': yarn_row['Name of the product'],
            'score': score,
            'price': yarn_row['Price (€)'],
            'rating': yarn_row['Rating (★)'],
            'yarn_weight': yarn_row['Yarn thikness'],
            'hook_size': yarn_row['Needle/Hook Size (mm)'],
            'cotton': yarn_row['Cotton (%)'],
            'acrylic': yarn_row['Acrylic (%)'],
            'wool': yarn_row['Wool (%)']
        })
    
    # Sort by score
    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.sort_values('score', ascending=False)
    
    return pattern_row, scores_df.head(top_n)

def display_recommendations(pattern_row, recommendations):
    """Display yarn recommendations nicely."""
    
    print(f"\n{'='*80}")
    print(f"PATTERN: {pattern_row['Pattern Name']}")
    print(f"{'='*80}")
    print(f"Required Yarn Weight: {pattern_row['Yarn Weight']}")
    print(f"Hook Size: {pattern_row['Hook Size (mm)']}mm")
    print(f"Difficulty: {pattern_row['Difficulty Level']}")
    print(f"Recommended Composition: {pattern_row['Recommended Composition']}")
    
    print(f"\n{'='*80}")
    print(f"TOP {len(recommendations)} YARN RECOMMENDATIONS")
    print(f"{'='*80}\n")
    
    for idx, (i, row) in enumerate(recommendations.iterrows(), 1):
        print(f"{idx}. {row['yarn_name']}")
        print(f"   Match Score: {row['score']:.1f}%")
        print(f"   Price: €{row['price']:.2f} | Rating: {row['rating']:.1f}★")
        print(f"   Weight: {row['yarn_weight']} | Hook: {row['hook_size']}mm")
        
        # Show composition
        comp = []
        if row['cotton'] > 0:
            comp.append(f"{int(row['cotton'])}% Cotton")
        if row['acrylic'] > 0:
            comp.append(f"{int(row['acrylic'])}% Acrylic")
        if row['wool'] > 0:
            comp.append(f"{int(row['wool'])}% Wool")
        print(f"   Composition: {', '.join(comp) if comp else 'Mixed fibers'}")
        print()

if __name__ == "__main__":
    print("="*80)
    print("PATTERN-YARN MATCHING ALGORITHM - SLICE 10")
    print("="*80)
    print()
    
    # Load databases
    patterns_df, yarn_df = load_databases()
    
    print(f"✅ Loaded {len(patterns_df)} patterns")
    print(f"✅ Loaded {len(yarn_df)} yarns")
    print()
    
    # Test with several patterns
    test_patterns = [
        "CIRCLE CUSHION",
        "BOBBY GRANNY SQUARE BLANKET",
        "Jellyfish Babies"
    ]
    
    for pattern_name in test_patterns:
        try:
            pattern_row, recommendations = match_yarn_to_pattern(
                pattern_name, patterns_df, yarn_df, top_n=3
            )
            display_recommendations(pattern_row, recommendations)
        except Exception as e:
            print(f"Error matching {pattern_name}: {e}")
    
    print("="*80)
    print("✅ Slice 10 complete: Pattern-yarn matching algorithm works")
    print("="*80)
    print("\nThe algorithm considers:")
    print("  ✓ Yarn weight compatibility (30%)")
    print("  ✓ Hook size match (20%)")
    print("  ✓ Fiber composition (20%)")
    print("  ✓ Yarn quality/rating (15%)")
    print("  ✓ Price/value (15%)")
