---
id: 2
title: Revise Project Constitution to v2.0.0
stage: constitution
date: 2025-12-05
surface: agent
model: gemini
feature: none
branch: main
user: User
command: /sp.constitution
labels: [constitution, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  []
---

## Prompt

/sp.constitution
# Constitution: Physical AI & Humanoid Robotics Program

## 1. Purpose
To formally define the academic, technical, and operational framework for training students in Physical AI — AI systems capable of sensing, understanding, and acting within real-world physics using humanoid robotic platforms.

## 2. Scope
This constitution applies to:
- Digital Twin Robotics
- Humanoid AI Systems
- Edge Robotics (Jetson Orin)
- ROS 2-based locomotion and manipulation
- NVIDIA Isaac-based simulation and perception
- Vision-Language-Action systems

## 3. Definition of Physical AI
Physical AI refers to embodied machine intelligence that:
- Perceives the world using multimodal sensors (RGB-D, IMU, VSLAM)
- Interprets language, gestures, object context
- Learns through active interaction and movement
- Actuates decisions using biped locomotion & manipulation controllers

AI exists not only in **brain-space** (software) but in **body-space** (mechatronics, locomotion, gravity, torque, inertia).

---

## 4. Academic Pillars

| Layer | Domain | Technology |
|-------|--------|------------|
| Cognitive Brain | LLM + VLA | GPT, Whisper, Planner Models |
| Nervous System | Control Middleware | ROS 2 (Humble/Iron) |
| Body Physics | Environment Simulation | Isaac Sim, Gazebo, Unity |
| Perception | World Understanding | Depth, VSLAM, Object Pose |
| Action | Motor Control | Nav2, Manipulation, MoveIt |

---

## 5. Learning Mandate
Students must be able to:
1. Interpret language-based tasks
2. Convert tasks → robotic action graph
3. Simulate movement & collisions correctly
4. Execute grasping, balancing, navigation
5. Communicate robot reasoning clearly

The program produces **embodied intelligence developers**, not just coders.

---

## 6. Platform Requirements

### Core Software
- ROS 2 Humble / Iron
- Isaac Sim & Isaac ROS
- Gazebo Fortress / Garden
- Unity for high-fidelity visualization

### Edge Hardware
- Jetson Orin Nano or NX (AI inference)
- RealSense D435i (depth + IMU)
- Microphone array for VLA voice integration

---

## 7. Capstone Requirement

A humanoid robot must:
- Receive natural voice input
- Convert to action via planner model
- Navigate obstacles in simulation
- Identify & manipulate an object
- Verbally confirm task completion

**Voice → Plan → Navigate → Detect → Manipulate → Explain**

---

## 8. Safety Charter
All robotics activity follows:

- ROS Rep-201 safety recommendations
- NVIDIA Isaac teleop lock boundaries
- No autonomous uncontrolled biped testing
- No adversarial or weaponized intent coding

Robot behavior must remain:
Predictable • Explainable • Verifiable.

---

## 9. Governance
Any module update requires:
- Technical validation (ROS / Isaac)
- Curriculum alignment
- Safety compliance review

---

## 10. Revision Cycle
This constitution is revised annually based on:
- RTX simulation driver updates
- Isaac platform evolution
- Humanoid locomotion research maturity

---

## Response snapshot

I have updated the project constitution to version 2.0.0 based on your input. This involved a complete rewrite of the document to focus on the academic and technical framework for Physical AI and humanoid robotics.

I also updated the `plan-template.md` to align its 'Constitution Check' section with the new principles.

Finally, I have created this Prompt History Record to document the changes.

- **New Version**: 2.0.0 (major bump due to complete rewrite)
- **Updated Files**:
  - `.specify/memory/constitution.md`
  - `.specify/templates/plan-template.md`
- **Suggested Commit Message**: `docs(constitution): amend constitution to v2.0.0 and update templates`

## Outcome

- ✅ Impact: {{OUTCOME_IMPACT}}
- 🧪 Tests: {{TESTS_SUMMARY}}
- 📁 Files: {{FILES_SUMMARY}}
- 🔁 Next prompts: {{NEXT_PROMPTS}}
- 🧠 Reflection: {{REFLECTION_NOTE}}

## Evaluation notes (flywheel)

- Failure modes observed: {{FAILURE_MODES}}
- Graders run and results (PASS/FAIL): {{GRADER_RESULTS}}
- Prompt variant (if applicable): {{PROMPT_VARIANT_ID}}
- Next experiment (smallest change to try): {{NEXT_EXPERIMENT}}
