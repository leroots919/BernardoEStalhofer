-- Enable Row Level Security (RLS) on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE process_files ENABLE ROW LEVEL SECURITY;

-- Create helper function to check if user is admin
-- SECURITY DEFINER bypasses RLS for the function's own queries, preventing infinite recursion
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    SELECT type = 'admin'
    FROM profiles
    WHERE id = auth.uid()
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Profiles Policies
CREATE POLICY "Users can read their own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Admins can read all profiles" ON profiles
  FOR SELECT USING (is_admin());

CREATE POLICY "Admins can update all profiles" ON profiles
  FOR UPDATE USING (is_admin());

-- Services Policies
CREATE POLICY "Authenticated users can read services" ON services
  FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Admins can insert services" ON services
  FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "Admins can update services" ON services
  FOR UPDATE USING (is_admin());

CREATE POLICY "Admins can delete services" ON services
  FOR DELETE USING (is_admin());

-- Client Cases Policies
CREATE POLICY "Users can read their own cases" ON client_cases
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can update their own cases" ON client_cases
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Admins can read all cases" ON client_cases
  FOR SELECT USING (is_admin());

CREATE POLICY "Admins can update all cases" ON client_cases
  FOR UPDATE USING (is_admin());

CREATE POLICY "Admins can insert all cases" ON client_cases
  FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "Admins can delete all cases" ON client_cases
  FOR DELETE USING (is_admin());

-- Favorites Policies
CREATE POLICY "Users can read their own favorites" ON favorites
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own favorites" ON favorites
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete their own favorites" ON favorites
  FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Admins can read all favorites" ON favorites
  FOR SELECT USING (is_admin());

-- Consultations Policies
CREATE POLICY "Users can read their own consultations" ON consultations
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can update their own consultations" ON consultations
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Admins can read all consultations" ON consultations
  FOR SELECT USING (is_admin());

CREATE POLICY "Admins can update all consultations" ON consultations
  FOR UPDATE USING (is_admin());

CREATE POLICY "Admins can insert all consultations" ON consultations
  FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "Admins can delete all consultations" ON consultations
  FOR DELETE USING (is_admin());

-- Process Files Policies
CREATE POLICY "Users can read their own files" ON process_files
  FOR SELECT USING (
    user_id = auth.uid()
    OR case_id IN (SELECT id FROM client_cases WHERE user_id = auth.uid())
  );

CREATE POLICY "Users can upload their own files" ON process_files
  FOR INSERT WITH CHECK (
    user_id = auth.uid()
    AND case_id IN (SELECT id FROM client_cases WHERE user_id = auth.uid())
  );

CREATE POLICY "Admins can read all files" ON process_files
  FOR SELECT USING (is_admin());

CREATE POLICY "Admins can upload all files" ON process_files
  FOR INSERT WITH CHECK (is_admin());

CREATE POLICY "Admins can update all files" ON process_files
  FOR UPDATE USING (is_admin());

CREATE POLICY "Admins can delete all files" ON process_files
  FOR DELETE USING (is_admin());
