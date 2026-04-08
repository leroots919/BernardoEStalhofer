-- Create Custom Enum Types
CREATE TYPE user_type AS ENUM ('admin', 'cliente');
CREATE TYPE service_category AS ENUM ('multas', 'cnh', 'acidentes', 'consultoria', 'recursos');
CREATE TYPE case_status AS ENUM ('pendente', 'em_andamento', 'concluido', 'arquivado');

-- Profiles Table (Linked to Supabase Auth)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users ON DELETE CASCADE,
  name TEXT NOT NULL,
  username TEXT UNIQUE,
  email TEXT NOT NULL UNIQUE,
  type user_type NOT NULL DEFAULT 'cliente',
  cpf TEXT,
  phone TEXT,
  address TEXT,
  city TEXT,
  state VARCHAR(2),
  zip_code TEXT,
  register_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_login TIMESTAMPTZ
);

-- Services Table
CREATE TABLE services (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  category service_category NOT NULL,
  price DECIMAL(10, 2),
  duration_days INT,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Client Cases Table
CREATE TABLE client_cases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  status case_status NOT NULL DEFAULT 'pendente',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Favorites Table
CREATE TABLE favorites (
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  service_id UUID REFERENCES services(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, service_id)
);

-- Consultations Table
CREATE TABLE consultations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
  scheduled_date TIMESTAMPTZ NOT NULL,
  status case_status NOT NULL DEFAULT 'pendente',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Process Files Table
CREATE TABLE process_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  case_id UUID REFERENCES client_cases(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  original_filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for foreign keys to improve performance
CREATE INDEX idx_client_cases_user_id ON client_cases(user_id);
CREATE INDEX idx_client_cases_service_id ON client_cases(service_id);
CREATE INDEX idx_consultations_user_id ON consultations(user_id);
CREATE INDEX idx_consultations_service_id ON consultations(service_id);
CREATE INDEX idx_process_files_case_id ON process_files(case_id);

