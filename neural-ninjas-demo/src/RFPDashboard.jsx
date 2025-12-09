import React, { useState, useEffect, useRef } from 'react';
import { FileText, Search, DollarSign, CheckCircle, XCircle, AlertCircle, Loader, ChevronRight, Download, Terminal } from 'lucide-react';

const RFPProcessorSystem = () => {
    const [activeRFP, setActiveRFP] = useState(null);
    const [processing, setProcessing] = useState(false);
    const [agentLogs, setAgentLogs] = useState([]);
    const [matchedProducts, setMatchedProducts] = useState([]);
    const [finalBid, setFinalBid] = useState(null);
    const [showApproval, setShowApproval] = useState(false);
    const logsEndRef = useRef(null);

    // Auto-scroll logs
    useEffect(() => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [agentLogs]);

    // Mock Product Catalog
    const productCatalog = [
        { sku: "CT-001", name: "Marine Grade Protective Coating", specs: "Saltwater-resistant, high-durability, weatherproof, marine grade", price: 125.00, stock: 1500 },
        { sku: "PT-001", name: "Premium Exterior Gloss Paint", specs: "Water-resistant, high-gloss, UV protection, exterior grade", price: 45.99, stock: 5000 },
        { sku: "PT-002", name: "Industrial Anti-Corrosion Coating", specs: "High-viscosity, rust-proof, industrial grade, chemical resistant", price: 89.50, stock: 3000 },
    ];

    // Mock RFPs
    const mockRFPs = [
        {
            id: "RFP-2024-001",
            client: "Coastal Construction Ltd",
            content: "We require 500 liters of high-gloss exterior paint suitable for coastal conditions. Must be weather-resistant and UV protected. Delivery needed by Q3 2024.",
            date: "2024-12-01",
            status: "pending"
        },
        {
            id: "RFP-2024-002",
            client: "Marine Industries Corp",
            content: "Looking for 800 liters of marine-grade protective coating for ship hulls. Must be saltwater-resistant and highly durable. Budget: $100,000.",
            date: "2024-12-03",
            status: "pending"
        },
        {
            id: "RFP-2024-003",
            client: "AutoTech Manufacturing",
            content: "Need 1200 liters of automotive-grade high-gloss paint for production line. Fast-dry formula essential. Delivery within 30 days.",
            date: "2024-12-05",
            status: "pending"
        }
    ];

    const [rfpList, setRfpList] = useState(mockRFPs);

    // Simulate semantic matching
    const semanticMatch = (rfpContent, products) => {
        const keywords = rfpContent.toLowerCase();
        const matches = products.map(product => {
            let score = 0;
            const specs = product.specs.toLowerCase();
            if (keywords.includes('marine') && specs.includes('marine')) score += 55; // Match screenshot example
            if (keywords.includes('exterior') && specs.includes('exterior')) score += 30;
            return { ...product, confidence: score };
        }).filter(p => p.confidence > 0).sort((a, b) => b.confidence - a.confidence);
        return matches.slice(0, 1); // Just show top match for cleaner UI like screenshot
    };

    const extractQuantity = (content) => {
        const match = content.match(/(\d+)\s*(liters|litres|L)/i);
        return match ? parseInt(match[1]) : 500;
    };

    const calculatePricing = (product, quantity) => {
        const basePrice = product.price * quantity;
        let discount = 0;
        if (quantity > 500) discount = 0.05;
        const discountAmount = basePrice * discount;
        const total = basePrice - discountAmount;
        return { basePrice, discount: discount * 100, discountAmount, total };
    };

    const processRFP = async (rfp) => {
        setActiveRFP(rfp);
        setProcessing(true);
        setAgentLogs([]);
        setMatchedProducts([]);
        setFinalBid(null);
        setShowApproval(false);

        const addLog = (agent, message) => {
            setAgentLogs(prev => [...prev, { agent, message, timestamp: new Date().toLocaleTimeString('en-US', { hour12: true, hour: 'numeric', minute: '2-digit', second: '2-digit' }) }]);
        };

        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        await delay(500);
        addLog('Sales Agent', `Received RFP ${rfp.id} from ${rfp.client}`);

        await delay(800);
        addLog('Sales Agent', 'Extracting requirements and specifications...');

        await delay(800);
        const quantity = extractQuantity(rfp.content);
        addLog('Technical Agent', `Identified requirement: ${quantity} liters`);

        await delay(800);
        addLog('Technical Agent', 'Initiating semantic search in product database...');

        await delay(1000);
        const matches = semanticMatch(rfp.content, productCatalog);
        addLog('Technical Agent', `Found ${matches.length} matching products with confidence > 20%`);
        setMatchedProducts(matches);

        await delay(800);
        addLog('Pricing Agent', 'Calculating costs and applying volume discounts...');

        await delay(800);
        if (matches.length > 0) {
            const topMatch = matches[0];
            const pricing = calculatePricing(topMatch, quantity);

            addLog('Pricing Agent', `Base cost: $${pricing.basePrice.toFixed(2)}`);
            addLog('Pricing Agent', `Volume discount applied: ${pricing.discount}% ($${pricing.discountAmount.toFixed(2)})`);
            addLog('Pricing Agent', `Final bid total: $${pricing.total.toFixed(2)}`);

            setFinalBid({
                rfpId: rfp.id,
                client: rfp.client,
                product: topMatch,
                quantity,
                pricing,
                confidence: topMatch.confidence
            });
            setShowApproval(true);
        }
        setProcessing(false);
    };

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-200 p-6 font-sans">
            <div className="max-w-7xl mx-auto space-y-6">

                {/* Header */}
                <div className="bg-[#1e293b] border border-slate-700/50 rounded-xl p-6 shadow-lg">
                    <h1 className="text-3xl font-bold text-white mb-1">AI-Powered RFP Processing System</h1>
                    <p className="text-slate-400">Multi-Agent System for Industrial Manufacturing Bids</p>
                </div>

                {/* Incoming RFPs */}
                <div className="bg-[#1e293b] border border-slate-700/50 rounded-xl p-6 shadow-lg">
                    <div className="flex items-center gap-2 mb-4">
                        <FileText className="w-5 h-5 text-slate-300" />
                        <h2 className="text-xl font-bold text-white">Incoming RFPs</h2>
                    </div>
                    <div className="space-y-3">
                        {rfpList.map(rfp => (
                            <div
                                key={rfp.id}
                                onClick={() => !processing && processRFP(rfp)}
                                className={`p-4 rounded-lg border transition-all cursor-pointer ${activeRFP?.id === rfp.id
                                        ? 'bg-blue-900/20 border-blue-500/50'
                                        : 'bg-[#334155]/30 border-slate-700 hover:bg-[#334155]/50'
                                    }`}
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <div>
                                        <span className="text-white font-bold block">{rfp.id}</span>
                                        <span className="text-slate-300 text-sm">{rfp.client}</span>
                                    </div>
                                    <span className="bg-[#422006] text-[#facc15] text-xs px-2 py-1 rounded border border-[#facc15]/20">
                                        {rfp.status}
                                    </span>
                                </div>
                                <p className="text-slate-400 text-sm">{rfp.content}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Live Agent Activity */}
                <div className="bg-[#1e293b] border border-slate-700/50 rounded-xl p-6 shadow-lg">
                    <div className="flex items-center gap-2 mb-4">
                        <AlertCircle className="w-5 h-5 text-slate-300" />
                        <h2 className="text-xl font-bold text-white">Live Agent Activity</h2>
                    </div>
                    <div className="bg-[#0f172a] rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm border border-slate-700/50">
                        {agentLogs.length === 0 ? (
                            <div className="text-slate-500 text-center mt-20">Select an RFP to start processing...</div>
                        ) : (
                            <div className="space-y-1.5">
                                {agentLogs.map((log, idx) => (
                                    <div key={idx} className="flex gap-3">
                                        <span className="text-blue-400 shrink-0">{log.timestamp}</span>
                                        <div className="flex gap-2">
                                            <span className={`font-bold shrink-0 ${log.agent === 'Sales Agent' ? 'text-purple-400' :
                                                    log.agent === 'Technical Agent' ? 'text-green-400' :
                                                        log.agent === 'Pricing Agent' ? 'text-yellow-400' : 'text-blue-400'
                                                }`}>
                                                [{log.agent}]:
                                            </span>
                                            <span className="text-slate-300">{log.message}</span>
                                        </div>
                                    </div>
                                ))}
                                <div ref={logsEndRef} />
                            </div>
                        )}
                    </div>
                </div>

                {/* Matched Products */}
                {matchedProducts.length > 0 && (
                    <div className="bg-[#1e293b] border border-slate-700/50 rounded-xl p-6 shadow-lg">
                        <div className="flex items-center gap-2 mb-4">
                            <Search className="w-5 h-5 text-slate-300" />
                            <h2 className="text-xl font-bold text-white">Matched Products</h2>
                        </div>
                        {matchedProducts.map((product, idx) => (
                            <div key={idx} className="bg-[#334155]/30 border border-slate-700 rounded-lg p-4 flex justify-between items-center">
                                <div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-white font-bold text-lg">{product.name}</span>
                                        <span className="text-slate-400 text-sm">({product.sku})</span>
                                    </div>
                                    <p className="text-slate-400 text-sm mt-1">{product.specs}</p>
                                    <div className="text-green-400 font-bold mt-2">${product.price}/liter</div>
                                </div>
                                <div className="text-right">
                                    <span className="bg-blue-900/50 text-blue-200 px-3 py-1 rounded text-sm border border-blue-500/30">
                                        {product.confidence}% match
                                    </span>
                                    <div className="text-slate-400 text-sm mt-2">Stock: {product.stock}L</div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Generated Bid */}
                {showApproval && finalBid && (
                    <div className="bg-[#1e293b] border border-slate-700/50 rounded-xl p-6 shadow-lg">
                        <div className="flex items-center gap-2 mb-4">
                            <DollarSign className="w-5 h-5 text-slate-300" />
                            <h2 className="text-xl font-bold text-white">Generated Bid - Awaiting Approval</h2>
                        </div>

                        <div className="bg-[#2d2a4a]/30 border border-purple-500/30 rounded-xl overflow-hidden">
                            <div className="p-6 grid grid-cols-2 gap-y-6 gap-x-12">
                                <div>
                                    <div className="text-slate-400 text-sm mb-1">RFP ID</div>
                                    <div className="text-white font-bold text-lg">{finalBid.rfpId}</div>
                                </div>
                                <div>
                                    <div className="text-slate-400 text-sm mb-1">Client</div>
                                    <div className="text-white font-bold text-lg">{finalBid.client}</div>
                                </div>
                                <div>
                                    <div className="text-slate-400 text-sm mb-1">Product</div>
                                    <div className="text-white font-bold text-lg">{finalBid.product.name}</div>
                                </div>
                                <div>
                                    <div className="text-slate-400 text-sm mb-1">Quantity</div>
                                    <div className="text-white font-bold text-lg">{finalBid.quantity} liters</div>
                                </div>
                            </div>

                            <div className="border-t border-slate-700/50 p-6 bg-[#1e293b]/50">
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-slate-400">Base Price:</span>
                                    <span className="text-white font-mono">${finalBid.pricing.basePrice.toFixed(2)}</span>
                                </div>
                                {finalBid.pricing.discount > 0 && (
                                    <div className="flex justify-between items-center mb-4">
                                        <span className="text-green-400">Volume Discount ({finalBid.pricing.discount}%):</span>
                                        <span className="text-green-400 font-mono">-${finalBid.pricing.discountAmount.toFixed(2)}</span>
                                    </div>
                                )}
                                <div className="flex justify-between items-center pt-4 border-t border-slate-700/50">
                                    <span className="text-white text-xl font-bold">Total Bid:</span>
                                    <span className="text-green-400 text-2xl font-bold font-mono">${finalBid.pricing.total.toFixed(2)}</span>
                                </div>
                            </div>

                            <div className="p-4 bg-[#1e293b] flex gap-4">
                                <button className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg flex items-center justify-center gap-2 transition-colors">
                                    <CheckCircle className="w-5 h-5" />
                                    Approve Bid
                                </button>
                                <button className="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-3 rounded-lg flex items-center justify-center gap-2 transition-colors">
                                    <XCircle className="w-5 h-5" />
                                    Reject
                                </button>
                                <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors">
                                    <Download className="w-5 h-5" />
                                    PDF
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default RFPProcessorSystem;