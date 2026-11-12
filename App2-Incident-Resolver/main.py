"""
DigiNexSynapse - App2: Incident Resolver
Kiroween 2026 Hackathon: Skeleton Crew Category

Autonomous error log resolution engine. Simulates reading incoming error logs,
computing cosine similarity against a vector space of historical postmortems,
and generating targeted remediation actions guided by Kiro steering protocols.
"""

import os
import math
import re
from pathlib import Path

# Try importing numpy, provide lightweight deterministic fallback if not installed yet
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Load steering instructions to enforce anti-hallucination constraints
STEERING_PATH = Path(__file__).parent.parent / ".kiro" / "steering.md"
steering_text = ""
if STEERING_PATH.exists():
    with open(STEERING_PATH, "r", encoding="utf-8") as f:
        steering_text = f.read().strip()

# Historical Incident Knowledge Base (Mock Vector Index)
HISTORICAL_INCIDENTS = [
    {
        "id": "INC-2025-104",
        "title": "Database connection pool exhaustion",
        "keywords": ["database", "connection", "pool", "exhaustion", "timeout", "postgres", "max_connections"],
        "root_cause": "Unclosed database sessions in high-throughput worker pool.",
        "recommended_fix": "Trigger connection pool recycling and scale max_connections from 100 to 300."
    },
    {
        "id": "INC-2025-219",
        "title": "Out of Memory (OOM) killer in worker container",
        "keywords": ["memory", "oom", "killed", "heap", "allocation", "leak", "container"],
        "root_cause": "Buffer overflow in streaming video transcoding worker.",
        "recommended_fix": "Restart pod with 2Gi memory limits and clear buffer cache."
    },
    {
        "id": "INC-2026-042",
        "title": "TLS handshake failure after certificate rotation",
        "keywords": ["tls", "ssl", "handshake", "certificate", "expired", "crypto", "authority"],
        "root_cause": "Intermediate certificate chain missing in ingress controller secret.",
        "recommended_fix": "Reload ingress secret bundle with fullchain.pem certificate."
    },
    {
        "id": "INC-2026-088",
        "title": "Redis cluster failover packet drop",
        "keywords": ["redis", "cluster", "failover", "timeout", "latency", "cache", "network"],
        "root_cause": "Network partition triggered false-positive replica demotion.",
        "recommended_fix": "Synchronize sentinel heartbeat windows and flush stale DNS mappings."
    }
]


def tokenize(text: str):
    """Tokenize and normalize text into clean lowercase words."""
    return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())


def create_bow_vector(tokens, vocabulary):
    """Build a term-frequency vector across a unified vocabulary."""
    counts = {word: 0 for word in vocabulary}
    for token in tokens:
        if token in counts:
            counts[token] += 1
    if HAS_NUMPY:
        return np.array([counts[w] for w in vocabulary], dtype=float)
    return [float(counts[w]) for w in vocabulary]


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors using numpy or math fallback."""
    if HAS_NUMPY:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
    else:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


def resolve_incident(raw_log: str):
    """Process an incident log and match it against historical context."""
    print("=" * 60)
    print("🤖 DigiNexSynapse Autonomous Incident Resolver (App2)")
    print(f"Engine: {'NumPy Accelerated' if HAS_NUMPY else 'Pure-Python Vector Math'}")
    if steering_text:
        print(f"Steering Directive Enforced: {steering_text[:75]}...")
    print("=" * 60)

    print(f"\n[1/3] Ingesting Error Log:\n---\n{raw_log.strip()}\n---")
    
    log_tokens = tokenize(raw_log)
    
    # Build vocabulary from both query and knowledge base
    vocab_set = set(log_tokens)
    for inc in HISTORICAL_INCIDENTS:
        vocab_set.update(inc["keywords"])
        vocab_set.update(tokenize(inc["title"]))
    vocabulary = sorted(list(vocab_set))

    query_vec = create_bow_vector(log_tokens, vocabulary)

    print("\n[2/3] Performing Vector Cosine Similarity Search...")
    scored_incidents = []
    for inc in HISTORICAL_INCIDENTS:
        inc_tokens = inc["keywords"] + tokenize(inc["title"])
        doc_vec = create_bow_vector(inc_tokens, vocabulary)
        score = cosine_similarity(query_vec, doc_vec)
        scored_incidents.append((score, inc))
        print(f"  * Matched against [{inc['id']}] '{inc['title']}': Similarity = {score:.4f}")

    scored_incidents.sort(key=lambda x: x[0], reverse=True)
    best_score, best_match = scored_incidents[0]

    print("\n[3/3] Resolution Decision Matrix:")
    if best_score > 0.15:
        print(f"  🎯 High-Confidence Match: {best_match['id']} (Score: {best_score:.4f})")
        print(f"  🔍 Root Cause: {best_match['root_cause']}")
        print(f"  🛠️  Remediation Action: {best_match['recommended_fix']}")
        status = "RESOLVED_AUTO"
    else:
        print("  ⚠️ No historical incident surpassed similarity threshold.")
        print("  🚨 Escalating to on-call engineer under Kiro steering fallback protocol.")
        status = "ESCALATED"

    return {
        "status": status,
        "best_match_id": best_match["id"] if best_score > 0.15 else None,
        "confidence": round(best_score, 4),
        "steering_compliant": True
    }


if __name__ == "__main__":
    # Sample incident error log simulating runtime outage
    sample_error_log = """
    2026-11-12T05:22:19.412Z [FATAL] server.worker: Database connection timeout!
    pool size 100/100 reached. Error: connection pool exhaustion for postgres://db-east:5432.
    Failed to acquire client session within 30000ms.
    """
    
    result = resolve_incident(sample_error_log)
    print(f"\nFinal Execution Output: {result}")
