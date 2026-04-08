# Traffic Lawyer MVP Migration Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate the current Traffic Lawyer system from a decoupled React + FastAPI + MySQL architecture to a unified Next.js + Supabase + PostgreSQL architecture for zero cost and maximum simplicity.

**Architecture:** Unified Next.js (App Router) application. Backend logic moved to Next.js Server Actions/API Routes. Database, Auth, and File Storage handled by Supabase.

**Tech Stack:** Next.js 15, TypeScript, Tailwind CSS, Supabase (PostgreSQL, Auth, Storage), Vercel.

---

## Phase 1: Infrastructure Setup

### Task 1: Initialize Next.js Project
**Files:**
- Root directory: `.worktrees/migration-nextjs-supabase/`

**Step 1: Run create-next-app**
Run: `npx create-next-app@latest . --ts --tailwind --eslint --app --src-dir --import-alias "@/*"`
Expected: Project scaffolded in current directory.

**Step 2: Verify installation**
Run: `npm run dev`
Expected: App running at http://localhost:3000

**Step 3: Commit**
Run: `git add . && git commit -m "chore: initialize next.js project"`

### Task 2: Supabase Project Connection
**Files:**
- Create: `.env.local`

**Step 1: Add Supabase environment variables**
Add to `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

**Step 2: Install Supabase client**
Run: `npm install @supabase/supabase-js @supabase/ssr`

**Step 3: Create Supabase client utility**
Create: `src/lib/supabase.ts`
```typescript
import { createBrowserClient } from '@supabase/ssr'

export const createClient = () => createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

**Step 4: Commit**
Run: `git add . && git commit -m "chore: setup supabase client"`

---

## Phase 2: Database & Security (Supabase)

### Task 3: Schema Migration (MySQL to PostgreSQL)
**Reference:** `database_schema.sql` from old project.

**Step 1: Create 'profiles' table**
Run SQL in Supabase Dashboard:
```sql
create table profiles (
  id uuid references auth.users on delete cascade primary key,
  full_name text,
  role text check (role in ('lawyer', 'client')),
  updated_at timestamp with time zone
);
```

**Step 2: Create 'cases' table (Processos)**
Run SQL in Supabase Dashboard:
```sql
create table cases (
  id uuid default gen_random_uuid() primary key,
  client_id uuid references profiles(id),
  description text,
  status text default 'pending',
  created_at timestamp with time zone default now()
);
```

**Step 3: Create 'documents' table**
Run SQL in Supabase Dashboard:
```sql
create table documents (
  id uuid default gen_random_uuid() primary key,
  case_id uuid references cases(id),
  file_path text,
  uploaded_by uuid references profiles(id),
  created_at timestamp with time zone default now()
);
```

**Step 4: Commit schema changes (via migration file if using Supabase CLI, otherwise doc)**
Create: `docs/plans/database-schema-supabase.sql` with the above SQL.
Run: `git add docs/plans/database-schema-supabase.sql && git commit -m "feat: define supabase schema"`

### Task 4: Enable Row Level Security (RLS)
**Goal:** Ensure clients only see their own data.

**Step 1: Enable RLS on cases**
Run: `alter table cases enable row level security;`

**Step 2: Create policy for clients**
Run: 
```sql
create policy "Clients can view their own cases" 
on cases for select 
using (auth.uid() = client_id);
```

**Step 3: Create policy for lawyers**
Run:
```sql
create policy "Lawyers can view all cases" 
on cases for all 
using (
  exists (
    select 1 from profiles 
    where id = auth.uid() and role = 'lawyer'
  )
);
```

**Step 4: Commit**
Run: `git add . && git commit -m "feat: setup RLS policies"`

---

## Phase 3: Core Functionality (TDD Approach)

### Task 5: Auth Flow (Login/Register)
**Files:**
- Create: `src/app/login/page.tsx`
- Test: `tests/auth/login.test.ts`

**Step 1: Write failing test for login**
Create `tests/auth/login.test.ts`:
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import LoginPage from '@/app/login/page'

test('renders login form and submits', async () => {
  render(<LoginPage />)
  fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@test.com' }})
  fireEvent.click(screen.getByText(/login/i))
  // expect result...
})
```

**Step 2: Run test to verify failure**
Run: `npm test tests/auth/login.test.ts`
Expected: FAIL (LoginPage not implemented)

**Step 3: Implement Login Page**
Create `src/app/login/page.tsx` using Supabase `signInWithPassword`.

**Step 4: Run test to verify pass**
Run: `npm test tests/auth/login.test.ts`
Expected: PASS

**Step 5: Commit**
Run: `git add . && git commit -m "feat: implement auth login with TDD"`

### Task 6: File Upload/Download (Storage)
**Files:**
- Create: `src/components/FileUpload.tsx`
- Create: `src/app/api/upload/route.ts`
- Test: `tests/storage/upload.test.ts`

**Step 1: Write failing test for file upload**
Create `tests/storage/upload.test.ts` to mock Supabase Storage upload.

**Step 2: Implement Upload Component**
Create `src/components/FileUpload.tsx` utilizing `supabase.storage.from('documents').upload()`.

**Step 3: Implement Backend Link**
Create `src/app/api/upload/route.ts` to save file reference in `documents` table.

**Step 4: Verify and Commit**
Run tests $\rightarrow$ Pass $\rightarrow$ Commit.

---

## Phase 4: Frontend Migration (Reusing Assets)

### Task 7: Migrate Landing Page
**Files:**
- Modify: `src/app/page.tsx`
- Reference: `advBS/src/components/LandingPage.js` and `LandingPage.css`

**Step 1: Copy HTML/JSX structure** from `LandingPage.js` to `page.tsx`.
**Step 2: Port CSS styles** to Tailwind classes.
**Step 3: Verify responsiveness** and commit.

### Task 8: Migrate Lawyer Dashboard
**Files:**
- Create: `src/app/admin/dashboard/page.tsx`
- Reference: `advBS/src/components/admin/Dashboard.js`

**Step 1: Implement Case List** using Supabase `select` from `cases`.
**Step 2: Implement Status Update** using Supabase `update`.
**Step 3: Verify and commit.**

---

## Phase 5: Integration & Polish

### Task 9: WhatsApp Notifications
**Files:**
- Create: `src/app/api/whatsapp/route.ts`
- Reference: `advBS-backend/poker_academy_api/src/routes/whatsapp_routes.py`

**Step 1: Port Python logic to TypeScript.**
**Step 2: Trigger notification on case status change.**
**Step 3: Verify with real API and commit.**

### Task 10: Final Deployment
**Step 1: Connect GitHub to Vercel.**
**Step 2: Configure Environment Variables.**
**Step 3: Run production build and verify.**
