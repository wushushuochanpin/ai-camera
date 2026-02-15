---
name: prd-standards
description: Standards for writing Product Requirement Documents (PRD) in this repo, covering file management, UX/UI detail, permissions, i18n, and technical architecture.
---

# PRD Standards (ai-camera)

Expert guidelines for creating high-quality, technically sound, and user-centric Product Requirement Documents.

## When to apply this skill

- **Drafting:** When creating a new PRD for enterprise-level features.
- **Reviewing:** When auditing PRDs for completeness, logic gaps, or technical feasibility.
- **Architecture Design:** When defining permission models (RBAC), database schemas, or internationalization strategies.
- **UI/UX Design:** When specifying interaction details, layout adaptability, and responsiveness.

## Instructions

### 1. Meta Standards (File Management)

#### Naming Convention (Recommended)
To ensure traceability, PRDs in this repo should use one of these patterns:

*   **Long-lived PRD (recommended):** `prd/<FeatureOrVersion>/PRD.md`
    *   Example: `prd/ios-ai-portrait-camera-v1.0/PRD.md`
*   **Incremental PRD notes (optional):** `prd/notes/{YYYYMMDD}_{Index}_{FeatureName}.md`
    *   **Generation Logic:**
        1.  **Scan:** Check `prd/notes/` for files starting with the current date (YYYYMMDD).
        2.  **Index:** Increment the max existing index by 1 (start at `01` if none exist).
        3.  **Naming:** Use short, semantic English (PascalCase) or Pinyin.
    *   Example:
        *   Existing: `20260215_01_GuidanceWebSocketProtocol.md`
        *   New: `20260215_02_AdminConsoleMVP.md`

### 2. Design Philosophy & Core Principles

**Principle:** Do not reinvent the wheel. Do not design carelessly.

1.  **Inheritance & Extension:** Prioritize auditing existing system capabilities. Design for compatibility and extension upon existing frameworks rather than creating new ones.
2.  **Benchmarking & Innovation:** Reuse mature industry solutions (e.g., E-commerce order flows). Borrow advanced concepts from other domains (e.g., logistics tracking) and apply them to the product.
3.  **Modularity First:** New features must be modular. Minimize hard-coded personalization to ensure component reusability.
4.  **Transparent Decision Making:** Record the rationale for key logic. List "Option A vs. Option B" and explain the trade-offs (Pros/Cons) and the final decision.

### 3. Feature Overview Requirements

*   **Feature Title:** Summarize core value in one sentence (Action + Object).
*   **Business Context:**
    *   What pain point is being solved?
    *   What are the consequences of not implementing this?
    *   *Note:* If requirements are vague, reverse engineer the User Story (e.g., "As a Supervisor, I need...").
*   **Core Flowcharts:**
    *   **Requirement:** Must include a **Business Process Diagram** (Swimlane format) defining boundaries between User, Frontend, Backend, and Third-party services.
    *   **Exception Handling:** Strictly forbidden to design only the "Happy Path." Must include closed-loop designs for failure, timeout, and rejection scenarios (e.g., login failure handling, not just success).

### 4. UX/UI Specifications & Interaction Details

**Principle:** "Details determine success; Experience determines retention."

#### 4.1 Layout Adaptability & Responsiveness
*   **Min-Width/Height Constraints:**
    *   **Global:** Define page `min-width` (e.g., 1024px) to prevent component stacking on narrow windows.
    *   **Component:** Cards and Modals must have a defined `min-height` to prevent UI collapse when content is empty.
*   **Responsive Strategy:**
    *   Define behavior for Wide Screens (1920px+) vs. Narrow Screens (1366px).
    *   *Example:* Should table columns scale proportionally or keep fixed pixel widths? Should a grid show 3 or 4 cards per row?
*   **DOM Deformation Prevention:**
    *   **Text Overflow:** Define handling for long text (Line break vs. Ellipsis `...` + Tooltip).
    *   **Media:** Lock Aspect Ratio to prevent image/video stretching.
*   **Modal Adaptation:**
    *   **Overflow:** If content exceeds Viewport Height, the scrollbar must appear within the **Modal Body**. The Header and Footer must remain visible (sticky) and never be covered.

#### 4.2 List View Design Standards
*   **Entity Classification:**
    *   **Immutable Data (Facts):** (e.g., Call Logs, Operation Logs). **Strictly prohibit modification/deletion.** Only View and Export are allowed.
    *   **Mutable Entities (Management):** (e.g., Employees, Rules). Must include full CRUD (Create, Read, Update, Delete) designs.
*   **"Create" Feature Design:**
    *   **Placement:** Standardize placement (e.g., Top right of the list or right side of the filter bar).
    *   **Permission Binding:** The "Create" button must be bound to an independent **RBAC Permission Key**. Users without permission should not see the button (Invisible), rather than just having it disabled.
*   **Filter & Search:**
    *   **Type:** Specify if the input is `Like %value%` (Fuzzy Search) or `Equal value` (Exact Search).
    *   **Persistence:** Search state (filters, pagination page number, sorting order) must be saved locally and restored upon page refresh or returning to the list.
*   **Table Interaction:**
    *   **Custom Headers:** If columns are numerous, must support column visibility toggling and ordering.
    *   **Sorting:** Header must indicate sortability. Interaction: `Ascending` -> `Descending` -> `Default`.
    *   **Operations Column:** Fixed to the far right.

#### 4.3 Form & Input Standards
*   **Mandatory Fields:** Explicitly mark with `*`.
*   **Defaults:** Auto-fill known information (e.g., current user, current date) to minimize user input cost.
*   **Validation:**
    *   Real-time validation (OnBlur).
    *   Error messages must be specific (e.g., ✅ "Format must be email" vs. ❌ "Error").
    *   Provide feedback *before* submission where possible.

#### 4.4 Deep i18n & Localization (L10n)
**Vision:** Build the world's best Customer Service System.

*   **RTL Layout Adaptation (Right-to-Left):**
    *   **Mirroring Rule:** For languages like Arabic or Hebrew, the layout must mirror physically, not just text alignment.
    *   **Specific Requirements:**
        *   Sidebar moves from Left to Right.
        *   Input cursor starts from the Right.
        *   **Directional Icon Reversal:** Icons implying direction (e.g., "Back Arrow `<`") must flip to `>`. Universal icons (e.g., "Play", "Search") generally do not flip.
        *   **CSS Logic:** Invert `margin-left`/`margin-right` and `padding-left`/`padding-right`.
*   **Contextual Transcreation:**
    *   **No Literal Translation:** Fixed text must match native terminology and industry habits.
    *   **Example:** Do not translate "Pick" (ticket) to generic "Pick up" (捡起). Use context-aware terms like "Claim" or "Assign" (领取/接入).
    *   **UI Expansion:** UI must reserve 30%-50% extra space for text expansion (German/Russian), prohibiting fixed-width text containers to prevent layout breakage.

### 5. Business Logic & RBAC Architecture

#### 5.1 Entity Lifecycle (State Machine)
*   **Requirement:** Provide a diagram defining all states (e.g., Pending -> Processing -> Done -> Closed).
*   **Transitions:** Define exactly who (Role) can trigger a transition and under what conditions (Rules).

#### 5.2 RBAC Permission Design (Role-Based Access Control)
Deconstruct every feature module using the RBAC model:

1.  **Function Permissions:**
    *   **Granularity:** Button-level control.
    *   **CRUD Separation:** `view`, `create`, `edit`, `delete`, `export` must be independent Permission Keys (e.g., `ticket:view` is separate from `ticket:edit`).
2.  **Data Permissions:**
    *   **Row-Level:** Define data scope (Self / Department / Company / Custom).
    *   **Column-Level:** Define field masking (e.g., Phone Numbers `***`) and visibility of specific dropdown options based on roles.

#### 5.3 CRUD Special Rules
*   **Delete Restrictions:** Physical deletion is prohibited in principle. Use "Disable" (soft delete) or "Archive".
*   **Dependency Check:** Before executing "Disable" or "Delete", the system must check for references.
    *   *Interaction:* If referenced, block the operation and show a modal listing the specific dependencies that must be removed first.

### 6. Data & Technical Specifications

#### 6.1 Data Architecture
*   **Structured Storage:** Prioritize relational columns over large JSON blobs to ensure query performance and extensibility.
*   **ID Rules:** Define explicit, stable generation rules (e.g., `Prefix + Timestamp + Random`).
*   **Compatibility:** Schema changes must assess impact on historical data and legacy app versions.
    *   *Migration Strategy:* If changes are drastic, use "Copy & Refactor" (create new page/table, migrate later) rather than breaking the existing live page.

#### 6.2 Interfaces & Services
*   **Public Services:** Explicitly list dependencies (e.g., File Service, Notification Center, Third-party APIs).
*   **Idempotency:** Critical interfaces (especially financial or state-changing ones) must allow for idempotent design to prevent duplicate submissions.

### 7. PRD Self-Review Checklist

Before submission, verify the PRD against this list:

- [ ] **Scenario Closed-Loop:** Are failure, exception, and no-permission flows covered?
- [ ] **Adaptability:** Are min-width/height defined? Is content overflow (scroll/tooltip) handled?
- [ ] **RTL Support:** Is UI Mirroring (layout/padding/icons) defined for Arabic/RTL regions?
- [ ] **Localization:** Is text context-aware (not machine translated)? Is UI space reserved for text expansion?
- [ ] **RBAC Permissions:** Are buttons bound to independent keys? Are immutable entities protected from modification?
- [ ] **Data Safety:** Is there a specific Dependency Check logic for deletion/disabling?
- [ ] **Interaction Details:** Are filtering, sorting, pagination, and persistence fully defined?
- [ ] **Compatibility:** Can new and old data/pages coexist?
