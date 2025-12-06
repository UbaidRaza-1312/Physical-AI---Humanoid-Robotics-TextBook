---
id: 1
title: Establish Project Constitution for AI Textbook
stage: constitution
date: 2025-12-04
surface: agent
model: gemini
feature: none
branch: master
user: unknown
command: /sp.constitution
labels: [constitution, project-setup, ai-textbook]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: Physical AI & Humanoid Robotics Textbook

Purpose:
To create a comprehensive, academically rigorous textbook covering Physical AI principles, Humanoid Robotics, and the integration of AI systems into physical environments. The book will be written using Spec-Kit Plus and Claude Code, and deployed via **Docusaurus** on **GitHub Pages** as the publishing platform.

Publishing Platform:
- Platform: Docusaurus
- Hosting: GitHub Pages
- Features: Markdown-based content, versioned docs, syntax-highlighted code, diagrams/images support, responsive web interface.

Core Principles:
- Accuracy: All technical claims, software tutorials, and hardware recommendations must be verified against primary sources (official ROS 2, NVIDIA Isaac, Gazebo, Unity documentation).
- Clarity: Content must be readable for students with a computer science or engineering background.
- Reproducibility: All code examples, simulations, and hardware instructions must be executable and replicable.
- Rigor: Prefer peer-reviewed articles, official documentation, and authoritative sources.

Key Standards:
- All factual claims must be traceable to reliable sources.
- Citation format: APA style.
- Minimum 50% of references must be peer-reviewed or official technical documentation.
- Plagiarism check: 0% tolerance.
- Writing clarity: Flesch-Kincaid grade 10–12.
- Word count: 5,000–7,000 words per module section.
- Minimum 20 sources for the complete book.
- Format: PDF with embedded citations, code snippets, diagrams, and tables where needed.

Constraints:
- Follow the weekly module breakdown:
  1. Introduction to Physical AI
  2. ROS 2 Fundamentals
  3. Robot Simulation (Gazebo & Unity)
  4. NVIDIA Isaac AI Platform
  5. Humanoid Robot Development
  6. Conversational Robotics (GPT integration)
  7. Capstone Project: Autonomous Humanoid
- Include step-by-step tutorials for ROS 2, Gazebo, Unity, NVIDIA Isaac, and GPT/VLA integration.
- Hardware requirements (RTX Workstation, Jetson Kit, sensors, robot proxies) must be documented and justified.
- Provide cloud-based alternatives where physical hardware is unavailable.
- Ensure all simulations, code examples, and voice/vision pipelines are reproducible.
- Include safety and latency considerations for cloud-to-robot deployment.

Success Criteria:
- All technical claims verified and traceable.
- Zero plagiarism detected.
- Textbook is clear, structured, and academically rigorous.
- Students can reproduce tutorials and simulations successfully.
- Capstone project instructions allow a simulated or physical humanoid robot to execute a voice command, plan a path, perceive objects, and manipulate them.

## Response snapshot

Updated the project constitution to version 1.0.0, establishing core principles (Accuracy, Clarity, Reproducibility, Rigor) and key standards for the 'Physical AI & Humanoid Robotics Textbook' project. Aligned the project's plan template with these new principles.

## Outcome

- ✅ Impact: Established a foundational governance document for the project, ensuring all future work aligns with core principles of academic and technical rigor.
- 🧪 Tests: none
- 📁 Files: 
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
- 🔁 Next prompts: none
- 🧠 Reflection: The process correctly identified the need to propagate constitution changes to dependent templates, ensuring consistency.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
