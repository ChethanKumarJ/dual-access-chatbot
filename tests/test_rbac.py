"""RBAC tests - the whole point is customer can NEVER see internal"""
from src.retrieval import retrieve_context, PUBLIC_INDEXES, INTERNAL_INDEXES

def test_customer_only_public():
    ctx = retrieve_context("paystub for john", "customer")
    sources = [c["source"] for c in ctx]
    # customer should never see internal indexes
    for s in sources:
        assert s in PUBLIC_INDEXES
    assert not any("internal" in s for s in sources)

def test_owner_sees_all():
    ctx = retrieve_context("paystub for john", "owner")
    sources = [c["source"] for c in ctx]
    assert "internal-paystubs" in sources
