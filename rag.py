import json

sections_graph = {
    "Section3_2": {"text": "Process documentation is required."},
    "Section5_1": {"text": "Data validation is required."},
    "RiskMgmt": {"text": "Risk management steps are expected to be followed."}
} 

links = [
    {"from": "Section5_1", "to": "RiskMgmt", "type": "requires"}
]

def search_sections(question):
    found = []
    words = question.lower().split()
    for name, sec in sections_graph.items():
        if any(w in sec["text"].lower() for w in words):
            found.append(name)
    return found

def update_section(name, new_text):
    if name not in sections_graph:
        return None, []
    sections_graph[name]["text"] = new_text
    affected_links = [l for l in links if l["from"] == name or l["to"] == name]
    return name, affected_links

def handle_request(req):
    action = req.get("action")
    if action == "modify":
        section = req.get("node_id")
        new_text = req.get("new_details")
        updated, affected = update_section(section, new_text)
        status = "Updated ok" if updated else "Section missing"
        return {
            "answer": None,
            "source_sections": [],
            "updated_section": updated,
            "status": status,
            "affected_links": affected,
            "visualization": "/graph/view/policy_doc_v2"
        }

    question = req.get("query", "")
    matches = search_sections(question)
    answer = "Found info in: " + ", ".join(matches) if matches else "Nothing relevant"
    return {
        "answer": answer,
        "source_sections": matches,
        "updated_section": None,
        "status": "OK",
        "affected_links": [],
        "visualization": "/graph/view/policy_doc_v1"
    }

if __name__ == "__main__":
    q_req = {"document": "policy_document.pdf", "query": "compliance requirements"}
    print(json.dumps(handle_request(q_req), indent=2))

    m_req = {
        "action": "modify",
        "node_id": "Section5_1",
        "new_details": "Now includes risk-based checks and periodic reviews."
    }
    print(json.dumps(handle_request(m_req), indent=2))
