# main.py - Complete Backend System for AI-Powered RFP Processing

import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

# ============================================================================
# PHASE 1: DATA MODELS
# ============================================================================

class Product:
    """Product catalog item"""
    def __init__(self, sku: str, name: str, specs: str, price: float, stock: int):
        self.sku = sku
        self.name = name
        self.specs = specs
        self.price = price
        self.stock = stock
        self.embedding = None  # Will store vector embedding
    
    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "specs": self.specs,
            "price": self.price,
            "stock": self.stock
        }

class RFP:
    """Request for Proposal"""
    def __init__(self, rfp_id: str, client: str, content: str, date: str):
        self.rfp_id = rfp_id
        self.client = client
        self.content = content
        self.date = date
        self.status = "pending"
    
    def to_dict(self):
        return {
            "rfp_id": self.rfp_id,
            "client": self.client,
            "content": self.content,
            "date": self.date,
            "status": self.status
        }

class Bid:
    """Generated bid proposal"""
    def __init__(self, rfp: RFP, product: Product, quantity: int, 
                 pricing: Dict, confidence: float):
        self.rfp = rfp
        self.product = product
        self.quantity = quantity
        self.pricing = pricing
        self.confidence = confidence
        self.generated_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "rfp_id": self.rfp.rfp_id,
            "client": self.rfp.client,
            "product": self.product.to_dict(),
            "quantity": self.quantity,
            "pricing": self.pricing,
            "confidence": self.confidence,
            "generated_at": self.generated_at
        }

# ============================================================================
# PHASE 2: MOCK DATA GENERATION
# ============================================================================

def generate_product_catalog() -> List[Product]:
    """Generate mock product catalog"""
    products = [
        Product("PT-001", "Premium Exterior Gloss Paint", 
                "Water-resistant, high-gloss, UV protection, exterior grade", 
                45.99, 5000),
        Product("PT-002", "Industrial Anti-Corrosion Coating", 
                "High-viscosity, rust-proof, industrial grade, chemical resistant", 
                89.50, 3000),
        Product("PT-003", "Eco-Friendly Interior Paint", 
                "Low-VOC, matte finish, interior use, quick-dry", 
                38.75, 8000),
        Product("SV-001", "Heavy-Duty Industrial Solvent", 
                "Fast-evaporating, industrial grade, multi-purpose cleaner", 
                52.30, 2500),
        Product("CT-001", "Marine Grade Protective Coating", 
                "Saltwater-resistant, high-durability, weatherproof, marine grade", 
                125.00, 1500),
        Product("PT-004", "High-Gloss Automotive Paint", 
                "High-gloss, fast-dry, automotive grade, color-stable", 
                67.80, 4000),
        Product("PT-005", "Warehouse Floor Epoxy Coating", 
                "Industrial strength, chemical resistant, non-slip, heavy-traffic", 
                95.25, 2200),
        Product("SV-002", "Paint Thinner Professional Grade", 
                "Quick-dry formula, low odor, professional grade", 
                28.50, 6000),
        Product("PT-006", "Fire-Resistant Industrial Coating", 
                "Flame-retardant, high-temperature resistant, industrial grade", 
                156.00, 1200),
        Product("CT-002", "Waterproofing Membrane Coating", 
                "100% waterproof, flexible, crack-bridging, long-lasting", 
                78.90, 3500),
    ]
    return products

def generate_sample_rfps() -> List[RFP]:
    """Generate sample RFPs"""
    rfps = [
        RFP("RFP-2024-001", "Coastal Construction Ltd",
            "We require 500 liters of high-gloss exterior paint suitable for coastal conditions. "
            "Must be weather-resistant and UV protected. Delivery needed by Q3 2024.",
            "2024-12-01"),
        
        RFP("RFP-2024-002", "Marine Industries Corp",
            "Looking for 800 liters of marine-grade protective coating for ship hulls. "
            "Must be saltwater-resistant and highly durable. Budget: $100,000.",
            "2024-12-03"),
        
        RFP("RFP-2024-003", "AutoTech Manufacturing",
            "Need 1200 liters of automotive-grade high-gloss paint for production line. "
            "Fast-dry formula essential. Delivery within 30 days.",
            "2024-12-05"),
        
        RFP("RFP-2024-004", "Industrial Warehouse Solutions",
            "Require 2000 liters of epoxy floor coating for warehouse facility. "
            "Must be chemical resistant and suitable for heavy forklift traffic.",
            "2024-12-07"),
        
        RFP("RFP-2024-005", "FireSafe Construction",
            "Need 600 liters of fire-resistant coating for industrial building project. "
            "Must meet fire safety regulations and high-temperature specifications.",
            "2024-12-09"),
    ]
    return rfps

# ============================================================================
# PHASE 3: AGENT 1 - TECHNICAL AGENT (RAG-based Semantic Search)
# ============================================================================

class TechnicalAgent:
    """Handles product matching using semantic search"""
    
    def __init__(self, products: List[Product]):
        self.products = products
        self.keyword_weights = {
            'exterior': 2.5, 'interior': 2.5, 'marine': 3.0, 'automotive': 3.0,
            'industrial': 2.0, 'gloss': 2.0, 'matte': 2.0, 'epoxy': 3.0,
            'coating': 1.5, 'paint': 1.5, 'solvent': 2.5, 'thinner': 2.5,
            'waterproof': 2.5, 'resistant': 2.0, 'fire': 3.0, 'flame': 3.0,
            'uv': 2.0, 'saltwater': 2.5, 'chemical': 2.0, 'corrosion': 2.5,
            'fast-dry': 2.0, 'quick-dry': 2.0, 'heavy-duty': 2.0,
            'warehouse': 2.0, 'floor': 2.5, 'ship': 2.5, 'hull': 2.5,
            'coastal': 2.0, 'weather': 2.0, 'high-temperature': 2.5
        }
        self.logs = []
    
    def log(self, message: str):
        """Add log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [Technical Agent]: {message}")
        print(f"[Technical Agent]: {message}")
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Perform semantic search using keyword matching with TF-IDF-like scoring
        In production, this would use ChromaDB/FAISS with actual embeddings
        """
        self.log("Initiating semantic search in product database...")
        
        query_lower = query.lower()
        matches = []
        
        for product in self.products:
            score = self._calculate_similarity(query_lower, product)
            
            if score > 0:
                matches.append({
                    'product': product,
                    'confidence': min(int(score), 95),  # Cap at 95%
                    'score': score
                })
        
        # Sort by score and return top_k
        matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matches[:top_k]
        
        self.log(f"Found {len(top_matches)} matching products with confidence > 0%")
        
        for i, match in enumerate(top_matches, 1):
            self.log(f"  Match {i}: {match['product'].name} ({match['confidence']}% confidence)")
        
        return top_matches
    
    def _calculate_similarity(self, query: str, product: Product) -> float:
        """Calculate similarity score between query and product"""
        score = 0
        product_text = f"{product.name} {product.specs}".lower()
        
        # Keyword-based scoring with weights
        for keyword, weight in self.keyword_weights.items():
            if keyword in query and keyword in product_text:
                score += weight * 10
        
        # Exact phrase matching (higher weight)
        query_words = set(re.findall(r'\b\w+\b', query))
        product_words = set(re.findall(r'\b\w+\b', product_text))
        
        # Calculate word overlap
        common_words = query_words.intersection(product_words)
        if common_words:
            score += len(common_words) * 3
        
        return score
    
    def verify_technical_specs(self, product: Product, requirements: str) -> bool:
        """Verify if product meets technical requirements"""
        self.log(f"Verifying technical specifications for {product.sku}...")
        
        # Simple verification logic
        req_lower = requirements.lower()
        specs_lower = product.specs.lower()
        
        # Check critical requirements
        critical_keywords = ['resistant', 'grade', 'proof', 'protection']
        matches = sum(1 for kw in critical_keywords if kw in req_lower and kw in specs_lower)
        
        verified = matches >= 1
        
        if verified:
            self.log(f"✓ Product {product.sku} meets technical requirements")
        else:
            self.log(f"✗ Product {product.sku} may not meet all requirements")
        
        return verified

# ============================================================================
# PHASE 4: AGENT 2 - PRICING AGENT
# ============================================================================

class PricingAgent:
    """Handles pricing calculations and discounts"""
    
    def __init__(self):
        self.logs = []
        self.discount_tiers = [
            (2000, 0.15),  # 15% for 2000+ liters
            (1000, 0.10),  # 10% for 1000+ liters
            (500, 0.05),   # 5% for 500+ liters
        ]
    
    def log(self, message: str):
        """Add log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [Pricing Agent]: {message}")
        print(f"[Pricing Agent]: {message}")
    
    def calculate_pricing(self, product: Product, quantity: int) -> Dict:
        """Calculate total pricing with volume discounts"""
        self.log("Calculating costs and applying volume discounts...")
        
        base_price = product.price * quantity
        self.log(f"Base cost: ${base_price:.2f} ({quantity}L × ${product.price}/L)")
        
        # Determine discount
        discount_pct = 0
        for threshold, discount in self.discount_tiers:
            if quantity >= threshold:
                discount_pct = discount
                break
        
        discount_amount = base_price * discount_pct
        total = base_price - discount_amount
        
        if discount_pct > 0:
            self.log(f"Volume discount applied: {discount_pct*100}% (${discount_amount:.2f})")
        else:
            self.log("No volume discount applicable")
        
        self.log(f"Final bid total: ${total:.2f}")
        
        return {
            'base_price': round(base_price, 2),
            'discount': round(discount_pct * 100, 1),
            'discount_amount': round(discount_amount, 2),
            'total': round(total, 2),
            'unit_price': product.price
        }
    
    def check_stock_availability(self, product: Product, quantity: int) -> bool:
        """Check if sufficient stock is available"""
        available = product.stock >= quantity
        
        if available:
            self.log(f"✓ Stock available: {product.stock}L in inventory")
        else:
            self.log(f"✗ Insufficient stock: Need {quantity}L, only {product.stock}L available")
        
        return available

# ============================================================================
# PHASE 5: AGENT 3 - SALES AGENT (NLP Parser)
# ============================================================================

class SalesAgent:
    """Handles RFP intake and requirement extraction"""
    
    def __init__(self):
        self.logs = []
    
    def log(self, message: str):
        """Add log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [Sales Agent]: {message}")
        print(f"[Sales Agent]: {message}")
    
    def process_rfp(self, rfp: RFP) -> Dict:
        """Extract requirements from RFP"""
        self.log(f"Received RFP {rfp.rfp_id} from {rfp.client}")
        self.log("Extracting requirements and specifications...")
        
        # Extract quantity
        quantity = self._extract_quantity(rfp.content)
        
        # Extract keywords/requirements
        requirements = self._extract_requirements(rfp.content)
        
        self.log(f"Identified requirement: {quantity} liters")
        self.log(f"Key specifications: {', '.join(requirements[:3])}")
        
        return {
            'quantity': quantity,
            'requirements': requirements,
            'raw_content': rfp.content
        }
    
    def _extract_quantity(self, content: str) -> int:
        """Extract quantity from RFP text"""
        # Look for patterns like "500 liters", "1200L", etc.
        patterns = [
            r'(\d+)\s*(?:liters?|litres?|L)\b',
            r'(\d+)L\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Default quantity if not found
        return 500
    
    def _extract_requirements(self, content: str) -> List[str]:
        """Extract key requirements/keywords"""
        # Simple keyword extraction
        keywords = []
        content_lower = content.lower()
        
        key_terms = [
            'exterior', 'interior', 'marine', 'automotive', 'industrial',
            'gloss', 'matte', 'coating', 'paint', 'resistant', 'waterproof',
            'fire', 'epoxy', 'warehouse', 'floor', 'uv', 'weather',
            'fast-dry', 'chemical', 'corrosion', 'saltwater'
        ]
        
        for term in key_terms:
            if term in content_lower:
                keywords.append(term)
        
        return keywords

# ============================================================================
# PHASE 6: ORCHESTRATOR AGENT (Main Coordinator)
# ============================================================================

class OrchestratorAgent:
    """Main agent that coordinates all sub-agents"""
    
    def __init__(self, products: List[Product]):
        self.sales_agent = SalesAgent()
        self.technical_agent = TechnicalAgent(products)
        self.pricing_agent = PricingAgent()
        self.logs = []
    
    def log(self, message: str):
        """Add log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [Orchestrator]: {message}")
        print(f"[Orchestrator]: {message}")
    
    def process_rfp(self, rfp: RFP) -> Optional[Bid]:
        """
        Main workflow: Process RFP through all agents
        """
        print("\n" + "="*80)
        print(f"PROCESSING RFP: {rfp.rfp_id}")
        print("="*80 + "\n")
        
        self.log("Starting RFP processing workflow...")
        
        # Step 1: Sales Agent processes RFP
        extracted_data = self.sales_agent.process_rfp(rfp)
        
        # Step 2: Technical Agent finds matching products
        matches = self.technical_agent.semantic_search(
            rfp.content, 
            top_k=3
        )
        
        if not matches:
            self.log("✗ No suitable products found")
            return None
        
        # Get best match
        best_match = matches[0]
        product = best_match['product']
        confidence = best_match['confidence']
        
        # Step 3: Verify technical specifications
        self.technical_agent.verify_technical_specs(
            product, 
            extracted_data['raw_content']
        )
        
        # Step 4: Check stock availability
        quantity = extracted_data['quantity']
        stock_available = self.pricing_agent.check_stock_availability(product, quantity)
        
        if not stock_available:
            self.log("✗ Insufficient stock for this bid")
            return None
        
        # Step 5: Calculate pricing
        pricing = self.pricing_agent.calculate_pricing(product, quantity)
        
        # Step 6: Generate bid
        bid = Bid(rfp, product, quantity, pricing, confidence)
        
        self.log("✓ Bid compilation complete. Ready for manager approval.")
        
        print("\n" + "="*80)
        print("BID GENERATION COMPLETE")
        print("="*80 + "\n")
        
        return bid
    
    def get_all_logs(self) -> List[str]:
        """Get all logs from all agents"""
        all_logs = []
        all_logs.extend(self.logs)
        all_logs.extend(self.sales_agent.logs)
        all_logs.extend(self.technical_agent.logs)
        all_logs.extend(self.pricing_agent.logs)
        return all_logs

# ============================================================================
# PHASE 7: EXPORT & UTILITY FUNCTIONS
# ============================================================================

def export_product_catalog_csv(products: List[Product], filename: str = "product_catalog.csv"):
    """Export product catalog to CSV"""
    import csv
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SKU', 'Product_Name', 'Technical_Specs', 'Unit_Price', 'Stock_Level'])
        
        for product in products:
            writer.writerow([
                product.sku,
                product.name,
                product.specs,
                product.price,
                product.stock
            ])
    
    print(f"✓ Product catalog exported to {filename}")

def export_bid_json(bid: Bid, filename: str = None):
    """Export bid to JSON"""
    if filename is None:
        filename = f"bid_{bid.rfp.rfp_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(bid.to_dict(), f, indent=2)
    
    print(f"✓ Bid exported to {filename}")

def generate_bid_summary(bid: Bid) -> str:
    """Generate human-readable bid summary"""
    summary = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           BID PROPOSAL SUMMARY                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

RFP ID:              {bid.rfp.rfp_id}
Client:              {bid.rfp.client}
Generated:           {bid.generated_at}

────────────────────────────────────────────────────────────────────────────────
PRODUCT DETAILS
────────────────────────────────────────────────────────────────────────────────
SKU:                 {bid.product.sku}
Product:             {bid.product.name}
Specifications:      {bid.product.specs}
Quantity:            {bid.quantity} liters

────────────────────────────────────────────────────────────────────────────────
PRICING BREAKDOWN
────────────────────────────────────────────────────────────────────────────────
Unit Price:          ${bid.pricing['unit_price']:.2f} per liter
Base Price:          ${bid.pricing['base_price']:,.2f}
Discount:            {bid.pricing['discount']:.1f}% (${bid.pricing['discount_amount']:,.2f})

TOTAL BID:           ${bid.pricing['total']:,.2f}
────────────────────────────────────────────────────────────────────────────────

Confidence Score:    {bid.confidence}%
Stock Available:     {bid.product.stock} liters

═════════════════════════════════════════════════════════════════════════════════
"""
    return summary

# ============================================================================
# PHASE 8: MAIN EXECUTION & DEMO
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║         AI-POWERED RFP PROCESSING SYSTEM - MULTI-AGENT FRAMEWORK             ║")
    print("║                      EY Techathon 5.0 Submission                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Initialize system
    print("📦 Initializing system components...")
    products = generate_product_catalog()
    rfps = generate_sample_rfps()
    orchestrator = OrchestratorAgent(products)
    
    print(f"✓ Loaded {len(products)} products into catalog")
    print(f"✓ Loaded {len(rfps)} pending RFPs")
    print("\n")
    
    # Export product catalog
    export_product_catalog_csv(products)
    print("\n")
    
    # Process each RFP
    generated_bids = []
    
    for i, rfp in enumerate(rfps[:3], 1):  # Process first 3 RFPs for demo
        print(f"\n{'='*80}")
        print(f"PROCESSING RFP {i}/{min(3, len(rfps))}")
        print(f"{'='*80}\n")
        
        bid = orchestrator.process_rfp(rfp)
        
        if bid:
            generated_bids.append(bid)
            print(generate_bid_summary(bid))
            export_bid_json(bid)
        else:
            print(f"\n✗ Unable to generate bid for {rfp.rfp_id}\n")
        
        print("\n")
    
    # Final summary
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                           PROCESSING COMPLETE                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"\n✓ Successfully generated {len(generated_bids)} bids")
    print(f"✓ {len(rfps) - len(generated_bids)} RFPs require manual review")
    print(f"✓ All outputs exported to current directory")
    print("\n")

if __name__ == "__main__":
    main()