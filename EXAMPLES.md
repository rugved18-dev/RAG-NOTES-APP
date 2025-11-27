# Example Usage & Sample Prompts

## 📝 How to Get the Most Out of Chat with Your Notes

This document provides example use cases and sample prompts to help you get the best results.

## 🎓 Academic Use Cases

### Case 1: Learning New Material

**Scenario**: You just attended a biology lecture and have lecture notes.

**Sample Prompts**:
```
1. "Summarize the main concepts from today's lecture"
2. "What are the key definitions I need to memorize?"
3. "Can you explain photosynthesis in simple terms?"
4. "What are the steps of cellular respiration?"
5. "Give me study tips based on this material"
```

**Temperature Setting**: 0.5 (Balanced - accurate but clear explanations)

---

### Case 2: Test Preparation

**Scenario**: You have multiple textbook chapters to study for an exam.

**Sample Prompts**:
```
1. "Create a study guide for chapters 3-4"
2. "What are the most important formulas I need to know?"
3. "Compare and contrast concept A and concept B"
4. "What are common exam questions about this topic?"
5. "Explain this concept as if I'm 5 years old"
```

**Temperature Setting**: 0.3 (Precise - focuses on facts for exam prep)

---

### Case 3: Research & Synthesis

**Scenario**: You have multiple papers or research documents.

**Sample Prompts**:
```
1. "What's the relationship between these three papers?"
2. "Summarize the methodology used across all documents"
3. "What are the main findings and conclusions?"
4. "How do these documents support or contradict each other?"
5. "What are the gaps in research this identifies?"
```

**Temperature Setting**: 0.7 (Analytical - good for synthesis)

---

## 💼 Professional Use Cases

### Case 1: Documentation Reference

**Scenario**: You have API documentation or technical manuals.

**Sample Prompts**:
```
1. "How do I authenticate with this API?"
2. "What are all the available endpoints?"
3. "Explain the error codes and their meanings"
4. "What are best practices for rate limiting?"
5. "Show me an example request for this endpoint"
```

**Temperature Setting**: 0.2 (Very precise - no creativity needed)

---

### Case 2: Policy & Compliance

**Scenario**: Company policies, compliance documents, or standards.

**Sample Prompts**:
```
1. "Summarize the data privacy policy"
2. "What are my responsibilities under this policy?"
3. "What are the penalties for non-compliance?"
4. "How does this relate to GDPR requirements?"
5. "Can you create a compliance checklist?"
```

**Temperature Setting**: 0.3 (Precise - critical for compliance)

---

### Case 3: Meeting Notes

**Scenario**: Meeting transcripts or decision documents.

**Sample Prompts**:
```
1. "What action items were assigned to me?"
2. "Summarize the key decisions made"
3. "What were the main discussion points?"
4. "Who is responsible for what deliverables?"
5. "What's the timeline for implementation?"
```

**Temperature Setting**: 0.4 (Factual but conversational)

---

## 🔬 Advanced Techniques

### Technique 1: Multi-Document Comparison

**Setup**: Upload 2-3 related documents

**Sample Prompts**:
```
1. "Compare the approaches in Document A vs Document B"
2. "How do these sources agree or disagree?"
3. "Synthesize the information across all documents"
4. "What's unique to each document?"
5. "Create a unified summary combining all sources"
```

---

### Technique 2: Follow-up Questions

**Initial Question**:
```
"Explain quantum entanglement"
```

**Follow-up Questions**:
```
1. "Can you explain that more simply?"
2. "Give me a real-world example"
3. "How is this different from quantum superposition?"
4. "Why is this important in quantum computing?"
5. "What are the implications of this principle?"
```

💡 **Tip**: The AI remembers context, so you can ask progressively deeper questions!

---

### Technique 3: Extraction & Structuring

**Sample Prompts**:
```
1. "List all equations from this chapter in a table"
2. "Create a timeline of events described in these documents"
3. "Organize the main points into categories"
4. "Extract all definitions in glossary format"
5. "Create a concept map showing relationships"
```

---

### Technique 4: Creative Problem Solving

**Temperature Setting**: 0.8 (Highly creative)

**Sample Prompts**:
```
1. "Based on these principles, what new applications could exist?"
2. "How could we apply this concept to solve problem X?"
3. "What are potential future developments in this field?"
4. "Generate questions a journalist would ask about this topic"
5. "Create a teaching example to explain this concept"
```

---

## 🎯 Prompt Engineering Best Practices

### 1. Be Specific

❌ Bad:
```
"Tell me about the book"
```

✅ Good:
```
"Summarize Chapter 3, focusing on the main characters and plot developments"
```

---

### 2. Provide Context

❌ Bad:
```
"What does this mean?"
```

✅ Good:
```
"In the context of this physics textbook, explain what 'quantum entanglement' means"
```

---

### 3. Ask for Format

❌ Bad:
```
"Give me the formula"
```

✅ Good:
```
"List all mathematical formulas from Chapter 2 in a numbered format with explanations"
```

---

### 4. Use Follow-ups

✅ Good Sequence:
```
1. Initial: "Summarize renewable energy"
2. Follow-up: "Which is most efficient?"
3. Follow-up: "How does it compare to fossil fuels?"
4. Follow-up: "What are environmental impacts?"
```

---

### 5. Control Complexity

❌ Too Complex:
```
"Compare the Renaissance and Enlightenment periods while considering their relationship to modern technology"
```

✅ Better:
```
"What are the key differences between the Renaissance and Enlightenment?"
(Follow-up: "How did these movements influence modern technology?")
```

---

## 📊 Temperature Settings Guide

| Temperature | Use Case | Example |
|------------|----------|---------|
| **0.1-0.3** | Fact-based, precise | API docs, exam prep, compliance |
| **0.4-0.6** | Informative, balanced | News articles, general learning |
| **0.7-0.8** | Creative, exploration | Brainstorming, ideation, teaching |
| **0.9-1.0** | Very creative, experimental | Fiction, creative writing, ideas |

---

## ✨ Pro Tips & Tricks

### Tip 1: Source Verification
Always click "Sources" to verify the AI found the answer in your documents!

```
Answer: "The mitochondria is the powerhouse of the cell"
Sources: [biology_textbook.pdf - Page 42]
```

### Tip 2: Multi-Document Queries
Upload textbook chapters as separate files, then query:
```
"How does Chapter 2 build on concepts from Chapter 1?"
```

### Tip 3: Citation Studies
Use for citation gathering:
```
"List all authors mentioned in this research paper"
"What sources does the author cite most frequently?"
```

### Tip 4: Quick Glossary
Extract definitions:
```
"Create a glossary of all scientific terms in these documents"
```

### Tip 5: Concept Trees
Build understanding:
```
1. "What is photosynthesis?"
2. "Break that down into simpler components"
3. "How does each component work?"
4. "How do they connect?"
```

---

## ⚠️ Common Mistakes & How to Avoid Them

### Mistake 1: Unclear Questions
**Problem**: "What should I know?" → Vague results
**Solution**: "Summarize the 5 key concepts from Chapter 1"

### Mistake 2: Assuming AI Knows Context
**Problem**: "Explain this formula" (without context)
**Solution**: "In the physics chapter on mechanics, explain F=ma"

### Mistake 3: Not Verifying Sources
**Problem**: Accepting answer without checking sources
**Solution**: Always expand "Sources" section

### Mistake 4: Not Using Temperature
**Problem**: Getting too creative/not creative enough
**Solution**: Adjust temperature slider for use case

### Mistake 5: Single Large PDF
**Problem**: Uploading 500-page textbook without chunking
**Solution**: Split large PDFs by chapter for better results

---

## 🔄 Workflow Examples

### Example 1: Study Session

```
1. Upload: biology_chapter3.pdf
2. Ask: "Summarize this chapter"
3. Temperature: 0.5
4. Ask: "What are key terms?"
5. Ask: "Create study questions"
6. Ask: "Explain concept X in simple terms"
7. Ask: "How does this relate to Chapter 2?"
```

### Example 2: Research Project

```
1. Upload: paper1.pdf, paper2.pdf, paper3.pdf
2. Ask: "What's the research question across these papers?"
3. Ask: "Compare their methodologies"
4. Ask: "Summarize findings from each"
5. Ask: "What gaps remain?"
6. Temperature: 0.7
7. Ask: "What new research could address these gaps?"
```

### Example 3: Reference Work

```
1. Upload: manual.pdf
2. Ask: "What are the main features?"
3. Ask: "How do I set this up?"
4. Ask: "Troubleshoot error X"
5. Temperature: 0.2
6. Ask: "What's the default configuration?"
```

---

## 🎓 Learning Tips

**For Students**:
- Use for explaining difficult concepts
- Create study guides
- Generate practice questions
- Verify understanding with follow-ups

**For Professionals**:
- Quick reference for documents
- Extract key information
- Create summaries for busy colleagues
- Verify understanding of policies

**For Researchers**:
- Cross-reference multiple papers
- Find relationships between sources
- Extract methodology details
- Identify research gaps

---

## 🚀 Next Steps

1. **Start simple** - Ask one question about your document
2. **Verify sources** - Check that answers come from your PDFs
3. **Experiment** - Try different temperatures and question styles
4. **Iterate** - Use follow-up questions to refine understanding
5. **Share** - Copy answers with proper citations

---

**Happy learning! 📚✨**

For more help, see:
- README.md - General setup and features
- DEVELOPMENT.md - Architecture and customization
- QUICKSTART.md - Fast setup guide
